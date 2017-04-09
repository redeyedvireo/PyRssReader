from PyQt5 import QtCore, QtGui
from img_finder import ImgFinder
from resource_fetcher import ResourceFetcher

class ImagePrefetchThread(QtCore.QThread):
    # Indicates an image has been fetched.  The parameter is a tuple of the form: (url, pixmap).
    imageReadySignal = QtCore.pyqtSignal(tuple)

    def __init__(self, feedItemList, feed, proxy):
        super(ImagePrefetchThread, self).__init__()
        self.feedItemList = feedItemList
        self.feed = feed
        self.proxy = proxy
        self.outputList = []
        self.stopFlag = False           # Used to abort fetching

    def run(self):
        imageUrlList = []
        for feedItem in self.feedItemList:
            imgFinder = ImgFinder(feedItem.getFeedItemText())
            if imgFinder.hasImages():
                imageUrlList.extend(imgFinder.getImages())

        self.stopFlag = False
        for url in imageUrlList:
            if self.stopFlag:
                break       # Abort fetching

            # If the image URL doesn't begin with 'http' or 'https', prepend the feed's web page link
            imageUrl = url
            if not url.startswith("http"):
                if url.startswith("//"):
                    # In this case, we just need to add "https:"
                    imageUrl = "https:{}".format(url)
                else:
                    imageUrl = "{}{}".format(self.feed.m_feedWebPageLink, url)

            resourceFetcher = ResourceFetcher(imageUrl, self.proxy)
            pixmap = resourceFetcher.getDataAsPixmap()

            # Note: if the feed's web page link needed to be added, the original url (without the web page link)
            # is what will be used as the key in the image cache, since the HTML will contain only the urls
            # without the web page link prepended.
            self.outputList.append( (url, pixmap) )
            self.imageReadySignal.emit((url, pixmap))

    def abortFetching(self):
        self.stopFlag = True
