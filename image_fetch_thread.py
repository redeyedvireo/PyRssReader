from PyQt5 import QtCore, QtGui
from resource_fetcher import ResourceFetcher

class ImageFetchThread(QtCore.QThread):
    # imageFetchDoneSignal is emitted when all images have been downloaded.  The parameter is a list
    # consisting of tuples of the form: (url, pixmap).
    imageFetchDoneSignal = QtCore.pyqtSignal(list)

    def __init__(self, urlList, proxy):
        super(ImageFetchThread, self).__init__()
        self.urlList = urlList
        self.proxy = proxy
        self.outputList = []


    def run(self):
        for url in self.urlList:
            resourceFetcher = ResourceFetcher(url, self.proxy)
            image = resourceFetcher.getData()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image)
            self.outputList.append( (url, pixmap) )

        self.imageFetchDoneSignal.emit(self.outputList)
