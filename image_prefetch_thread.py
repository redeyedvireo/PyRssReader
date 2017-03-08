from PyQt5 import QtCore, QtGui
from img_finder import ImgFinder
from resource_fetcher import ResourceFetcher

class ImagePrefetchThread(QtCore.QThread):
    # Indicates an image has been fetched.  The parameter is a tuple of the form: (url, pixmap).
    imageReadySignal = QtCore.pyqtSignal(tuple)

    def __init__(self, feedItemList, proxy):
        super(ImagePrefetchThread, self).__init__()
        self.feedItemList = feedItemList
        self.proxy = proxy
        self.outputList = []

    def run(self):
        imageUrlList = []
        for feedItem in self.feedItemList:
            imgFinder = ImgFinder(feedItem.getFeedItemText())
            if imgFinder.hasImages():
                imageUrlList.extend(imgFinder.getImages())

        for url in imageUrlList:
            resourceFetcher = ResourceFetcher(url, self.proxy)
            image = resourceFetcher.getData()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image)
            self.outputList.append( (url, pixmap) )
            self.imageReadySignal.emit((url, pixmap))
