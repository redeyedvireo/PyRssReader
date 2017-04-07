from PyQt5 import QtCore, QtGui
from resource_fetcher import ResourceFetcher

class ImageFetchThread(QtCore.QThread):
    # imageFetchDoneSignal is emitted when all images have been downloaded.  The parameter is a list
    # consisting of tuples of the form: (url, pixmap).
    imageFetchDoneSignal = QtCore.pyqtSignal(list)

    def __init__(self, urlList, feed, proxy):
        super(ImageFetchThread, self).__init__()
        self.urlList = urlList
        self.feed = feed
        self.proxy = proxy
        self.outputList = []


    def run(self):
        for url in self.urlList:
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

        self.imageFetchDoneSignal.emit(self.outputList)
