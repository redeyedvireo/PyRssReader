import logging
import webbrowser
import re
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets
from img_finder import ImgFinder
from image_fetch_thread import ImageFetchThread
from utility import getResourceFileText, getResourceFilePixmap


class RssContentView(QtCore.QObject):
    # Emitted when the current feed item should be re-selected.  This is usually due to the language filter
    # being changed, which requires the current feed item to be re-read, and re-filtered.
    reselectFeedItemSignal = QtCore.pyqtSignal()

    def __init__(self, textBrowser, languageFilter, adFilter, imageCache, keyboardHandler, proxy):
        super(RssContentView, self).__init__()

        self.languageFilter = languageFilter
        self.adFilter = adFilter
        self.imageCache = imageCache
        self.keyboardHandler = keyboardHandler
        self.proxy = proxy
        self.m_css = ""
        self.m_feedHeaderHtml = ""
        self.m_processedFeedContents = ""
        self.rawFeedContents = ""
        self.dummyImage = QtGui.QPixmap()
        self.imageList = []
        self.currentFeedItem = None

        self.textBrowser = textBrowser
        self.textBrowser.setMouseTracking(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.installEventFilter(self)
        self.textBrowser.anchorClicked.connect(self.linkClicked)

        self.textBrowser.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.textBrowser.customContextMenuRequested.connect(self.onContextMenu)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        self.m_css = getResourceFileText("pagestyle.css")
        self.m_feedHeaderHtml = getResourceFileText("feedHeader.html")
        self.m_completeHtmlDocument = getResourceFileText("completeHtmlDocument.html")

        # Replace carriage returns and line feeds with spaces
        self.m_css = self.m_css.replace("\r", "").replace("\n", "")
        self.m_feedHeaderHtml = self.m_feedHeaderHtml.replace("\r", "").replace("\n", "")
        self.m_completeHtmlDocument = self.m_completeHtmlDocument.replace("\r", "").replace("\n", "")

        doc = self.textBrowser.document().setDefaultStyleSheet(self.m_css)

        self.dummyImage = QtGui.QPixmap(10, 10)
        self.dummyImage.fill()      # Fill it with white
        self.starImageForDebugging = getResourceFilePixmap("star.png")

    # TODO: Implement this: when mouse over a URL, emit a urlHovered signal
    def eventFilter(self, obj, event):
        if obj == self.textBrowser:
            #print("Event type: {}".format(event.type()))
            #if isinstance(event, QtGui.QMouseEvent):
            if event.type() == QtCore.QEvent.MouseMove:
                #print("pos: {}".format(event.pos()))
                #linkStr = PointOverLink(ev->pos())
                return False
            elif event.type() == QtCore.QEvent.KeyRelease:
                keyCode = event.key()
                self.keyboardHandler.handleKey(keyCode)
                return False

        return QtWidgets.QTextBrowser.eventFilter(self.textBrowser, obj, event)

    def setProxy(self, proxy):
        self.proxy = proxy

    def setContents(self, feedItem):
        """ Sets a feed item's HTML into the text browser. """
        self.currentFeedItem = feedItem

        # Title
        filteredTitle = self.languageFilter.filterString(feedItem.m_title)
        strTitleLink = self.m_feedHeaderHtml.replace("%1", feedItem.m_link).replace("%2", filteredTitle)

        htmlBody = feedItem.getFeedItemText()
        self.rawFeedContents = htmlBody

        # Create an HTML body
        if "<body>" not in htmlBody:
            newBody = self.m_completeHtmlDocument.format(strTitleLink, htmlBody)
            self.m_processedFeedContents = newBody
        else:
            logging.info("setContents: Error - feed item contained complete HTML.  GUID: {}".format(feedItem.m_guid))
            # TODO: Need to add the strTitleLink
            self.m_processedFeedContents = htmlBody

        # Find image source URLs, within <img> tags.  The image source URLs will be used as the image "names"
        # in the content view document.
        imgFinder = ImgFinder(self.m_processedFeedContents)
        if imgFinder.hasImages():
            self.imageList = imgFinder.getImages()
            self.setDummyImages()
            self.fetchImages()

        self.m_processedFeedContents = self.languageFilter.filterHtml(self.m_processedFeedContents)
        self.m_processedFeedContents = self.adFilter.filterHtml(self.m_processedFeedContents)
        self.m_processedFeedContents = self.fixHtml(self.m_processedFeedContents)

        self.textBrowser.setHtml(self.m_processedFeedContents)

        # This is currently not used, but I'm leaving this hook in here in case it is needed in the future.
        #self.fixDocument()

        # Set focus onto the content view, so that arrow keys will scroll the content view
        self.textBrowser.setFocus()

    def fixHtml(self, htmlText):
        """ Attempts to fix various readability issues caused by incompatible formatting contained in the
            feed item text, before setting the HTML to the document. """
        soup = BeautifulSoup(htmlText, 'html.parser')
        allParagraphs = soup.find_all("div")
        fixOccurred = False
        for paragraph in allParagraphs:
            if "style" in paragraph.attrs:
                styleAttr = paragraph.attrs["style"]
                if "line-height" in styleAttr:
                    newStyleAttr = re.sub(r'line-height:[^;]*;', '', styleAttr)
                    paragraph.attrs["style"] = newStyleAttr.strip()
                    fixOccurred = True

        if fixOccurred:
            logging.info("A fix in the HTML occurred.  GUID: {}".format(self.currentFeedItem))

        return soup.prettify()

    def fixDocument(self):
        """ Attempts to fix various readability issues caused by incompatible formatting contained in the
            feed item text. """
        # currentBlock = self.textBrowser.document().begin()
        # while currentBlock.isValid():
        #     blockFormat = currentBlock.blockFormat()
        #     currentLineHeight = blockFormat.lineHeight()
        #     blockFormat.setLineHeight(0.0, QtGui.QTextBlockFormat.SingleHeight)
        #     #currentBlock.setBlockFormat(blockFormat)
        #     currentBlock = currentBlock.next()

        # Select entire document
        selectionCursor = self.textBrowser.textCursor()
        selectionCursor.select(QtGui.QTextCursor.Document)

        selectionFormat = self.textBrowser.textCursor().blockFormat()
        selectionFormat.setLineHeight(0.0, QtGui.QTextBlockFormat.SingleHeight)
        selectionCursor.setBlockFormat(selectionFormat)


    def setDummyImages(self):
        """ Sets all embedded images to a dummy image, so that the document will be ready to view quickly.
            The actual images will be downloaded in a thread, so the user can start reading the document
            while the images download. """
        document = self.textBrowser.document()
        for imgUrl in self.imageList:
            if self.imageCache.contains(imgUrl):
                # Note that images that are found in the image cache are added to the resources here
                document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imgUrl), self.imageCache.getImage(imgUrl))
            else:
                document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imgUrl), self.dummyImage)

    @QtCore.pyqtSlot()
    def changeImages(self):
        document = self.textBrowser.document()
        for imgUrl in self.imageList:
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imgUrl), self.starImageForDebugging)
        self.textBrowser.reload()
        self.textBrowser.repaint()

    @QtCore.pyqtSlot()
    def fetchImages(self):
        """ Fetches all images. """
        imageFetchList = []
        for image in self.imageList:
            if not self.imageCache.contains(image):
                print("The image cache did not contain: {}".format(image))
                imageFetchList.append(image)

        self.imageFetchThread = ImageFetchThread(imageFetchList, self.proxy)
        self.imageFetchThread.imageFetchDoneSignal.connect(self.onImageFetchDone)
        self.imageFetchThread.start()

    def onImageFetchDone(self, imageList):
        """ Called when image fetching from the thread has finished. """
        document = self.textBrowser.document()
        for imageTuple in imageList:
            url = imageTuple[0]
            pixmap = imageTuple[1]
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(url), pixmap)

            # Add to the image cache
            self.imageCache.addImage(url, pixmap)

        self.textBrowser.setHtml(self.m_processedFeedContents)

    def linkClicked(self, url):
        webbrowser.open(url.toString())

    @QtCore.pyqtSlot('QPoint')
    def onContextMenu(self, point):
        print("Context menu requested")
        menu = self.textBrowser.createStandardContextMenu()
        menu.addSeparator()

        selText = self.textBrowser.textCursor().selectedText()
        if len(selText) > 0:
            menu.addAction("Add {} to language filter".format(selText), self.onAddToFilter)
            menu.addAction("Search for {} in Google".format(selText), self.onSearchGoogle)
            menu.addAction("Search for {} in Wikipedia".format(selText), self.onSearchWikipedia)

            menu.addSeparator()

        menu.addAction("Copy feed item source to clipboard", self.onCopyWebSource)
        menu.addAction("Copy raw feed item source to clipboard", self.onCopyRawFeedItemSource)
        menu.addAction("Rerun language filter", self.runLanguageFilter)

        menu.exec(self.textBrowser.mapToGlobal(point))

    def onAddToFilter(self):
        selText = self.textBrowser.textCursor().selectedText()

        if selText:
            self.languageFilter.addFilterWord(selText)
            self.reselectFeedItemSignal.emit()

    def onSearchGoogle(self):
        selText = self.textBrowser.textCursor().selectedText()

        if selText:
            urlStr = "http://www.google.com/search?q={}".format(selText.strip().replace(" ", "+"))
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlStr))

    def onSearchWikipedia(self):
        selText = self.textBrowser.textCursor().selectedText()

        if selText:
            urlStr = "http://en.wikipedia.org/wiki/{}".format(selText.strip().replace(" ", "_"))
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlStr))

    def onCopyWebSource(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.textBrowser.toHtml())

    def onCopyRawFeedItemSource(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.rawFeedContents)

    def runLanguageFilter(self):
        self.reselectFeedItemSignal.emit()
