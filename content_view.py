import logging
import webbrowser
from resource_fetcher import ResourceFetcher
from PyQt5 import QtCore, QtGui, QtWidgets
from img_finder import ImgFinder
from utility import getResourceFileText


class RssContentView(QtCore.QObject):
    def __init__(self, textBrowser, languageFilter):
        super(RssContentView, self).__init__()

        self.languageFilter = languageFilter
        self.m_css = ""
        self.m_feedHeaderHtml = ""
        self.m_processedFeedContents = ""
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

        # InitAdBlockList()

    # TODO: Implement this: when mouse over a URL, emit a urlHovered signal
    def eventFilter(self, obj, event):
        if obj == self.textBrowser:
            #print("Event type: {}".format(event.type()))
            #if isinstance(event, QtGui.QMouseEvent):
            if event.type() == QtCore.QEvent.MouseMove:
                #print("pos: {}".format(event.pos()))
                #linkStr = PointOverLink(ev->pos())
                return False

        return QtWidgets.QTextBrowser.eventFilter(self.textBrowser, obj, event)

    def setContents(self, feedItem):
        """ Sets a feed item's HTML into the text browser. """
        # Title
        filteredTitle = self.languageFilter.filterString(feedItem.m_title)
        strTitleLink = self.m_feedHeaderHtml.replace("%1", feedItem.m_link).replace("%2", filteredTitle)

        htmlBody = ""
        if feedItem.m_encodedContent:
            htmlBody = self.languageFilter.filterHtml(feedItem.m_encodedContent)
        else:
            htmlBody = self.languageFilter.filterHtml(feedItem.m_description)

        # Find image names, within <img> tags
        self.m_processedFeedContents = "{}<body>{}</body>".format(strTitleLink, htmlBody)
        imgFinder = ImgFinder(self.m_processedFeedContents)
        if imgFinder.hasImages():
            self.imageList = imgFinder.getImages()
            print("Images: {}".format(self.imageList))
            self.fetchImages()

        # TODO: might need to set some image placeholders before setting the HTML contents into the text browser
        # With the placeholders in place, the text browser can lay out the entire document.  The images can
        # be added later (I hope).
        self.textBrowser.setHtml(self.m_processedFeedContents)

    # TODO: This should be done in a thread.
    def fetchImages(self):
        """ Fetches all images. """
        # TODO: Maybe this should be in a separate file or class
        # This should be done with a ThreadPoolExecutor.  Use the as_completed() function to add images to the
        # document as they come in.
        document = self.textBrowser.document()
        for imgUrl in self.imageList:
            resourceFetcher = ResourceFetcher(imgUrl)
            image = resourceFetcher.getData()
            print("Image downloaded: {}".format(imgUrl))
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image)
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imgUrl), pixmap)

    def linkClicked(self, url):
        print("Link clicked: {}".format(url))
        webbrowser.open(url.toString())
