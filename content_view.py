import logging
import webbrowser
from resource_fetcher import ResourceFetcher
from PyQt5 import QtCore, QtGui, QtWidgets
from img_finder import ImgFinder
from image_fetch_thread import ImageFetchThread
from utility import getResourceFileText, getResourceFilePixmap


class RssContentView(QtCore.QObject):
    def __init__(self, textBrowser, languageFilter, adFilter, keyboardHandler, proxy):
        super(RssContentView, self).__init__()

        self.languageFilter = languageFilter
        self.adFilter = adFilter
        self.keyboardHandler = keyboardHandler
        self.proxy = proxy
        self.m_css = ""
        self.m_feedHeaderHtml = ""
        self.m_processedFeedContents = ""
        self.dummyImage = QtGui.QPixmap()
        self.imageList = []

        self.textBrowser = textBrowser
        self.textBrowser.setMouseTracking(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.installEventFilter(self)
        self.textBrowser.anchorClicked.connect(self.linkClicked)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        self.m_css = getResourceFileText("pagestyle.css")
        self.m_feedHeaderHtml = getResourceFileText("feedHeader.html")

        # Replace carriage returns and line feeds with spaces
        self.m_css = self.m_css.replace("\r", "").replace("\n", "")
        self.m_feedHeaderHtml = self.m_feedHeaderHtml.replace("\r", "").replace("\n", "")

        doc = self.textBrowser.document().setDefaultStyleSheet(self.m_css)

        self.dummyImage = getResourceFilePixmap("hourglass.png")
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
        print("Setting contents...")

        # Title
        filteredTitle = self.languageFilter.filterString(feedItem.m_title)
        strTitleLink = self.m_feedHeaderHtml.replace("%1", feedItem.m_link).replace("%2", filteredTitle)

        htmlBody = ""
        if feedItem.m_encodedContent:
            htmlBody = self.languageFilter.filterHtml(feedItem.m_encodedContent)
        else:
            htmlBody = self.languageFilter.filterHtml(feedItem.m_description)

        # Find image source URLs, within <img> tags.  The image source URLs will be used as the image "names"
        # in the content view document.
        self.m_processedFeedContents = "{}<body>{}</body>".format(strTitleLink, htmlBody)
        imgFinder = ImgFinder(self.m_processedFeedContents)
        if imgFinder.hasImages():
            self.imageList = imgFinder.getImages()
            self.setDummyImages()
            self.fetchImages()

        self.m_processedFeedContents = self.adFilter.filterHtml(self.m_processedFeedContents)

        # TODO: might need to set some image placeholders before setting the HTML contents into the text browser
        # With the placeholders in place, the text browser can lay out the entire document.  The images can
        # be added later (I hope).
        self.textBrowser.setHtml(self.m_processedFeedContents)

        # Set focus onto the content view, so that arrow keys will scroll the content view
        self.textBrowser.setFocus()

    def setDummyImages(self):
        """ Sets all embedded images to a dummy image, so that the document will be ready to view quickly.
            The actual images will be downloaded in a thread, so the user can start reading the document
            while the images download. """
        print("Setting dummy images...")
        document = self.textBrowser.document()
        for imgUrl in self.imageList:
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imgUrl), self.dummyImage)

    @QtCore.pyqtSlot()
    def changeImages(self):
        print("Changing images...")
        document = self.textBrowser.document()
        for imgUrl in self.imageList:
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imgUrl), self.starImageForDebugging)
        self.textBrowser.reload()
        self.textBrowser.repaint()

    @QtCore.pyqtSlot()
    def fetchImages(self):
        """ Fetches all images. """
        print("Fetching images...")

        self.imageFetchThread = ImageFetchThread(self.imageList, self.proxy)
        self.imageFetchThread.imageFetchDoneSignal.connect(self.onImageFetchDone)
        self.imageFetchThread.start()

    def onImageFetchDone(self, imageList):
        """ Called when image fetching from the thread has finished. """
        document = self.textBrowser.document()
        for imageTuple in imageList:
            url = imageTuple[0]
            pixmap = imageTuple[1]
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(url), pixmap)
        self.textBrowser.setHtml(self.m_processedFeedContents)

    def linkClicked(self, url):
        print("Link clicked: {}".format(url))
        webbrowser.open(url.toString())
