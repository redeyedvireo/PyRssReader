from PyQt5 import QtCore
from image_prefetch_thread import ImagePrefetchThread


class ImagePrefetcher(QtCore.QObject):
    # Signal emitted when all images have been fetched.  Its parameter is a tuple of the form: (url, image).
    imagePrefetchDoneSignal = QtCore.pyqtSignal(list)

    def __init__(self, db, imageCache, proxy):
        super(ImagePrefetcher, self).__init__()
        self.db = db
        self.proxy = proxy
        self.imageCache = imageCache

    def prefetchImages(self, feedItemList):
        """ Prefetches images from the given feed items.  feedItemList is a list of tuples of the
            form: (feedId, guid). """
        feedItems = self.db.getFeedItemsFromList(feedItemList)

        self.imagePrefetchThread = ImagePrefetchThread(feedItems, self.proxy)
        self.imagePrefetchThread.imageReadySignal.connect(self.onImagePrefetched)
        self.imagePrefetchThread.start()

    @QtCore.pyqtSlot(tuple)
    def onImagePrefetched(self, imageTuple):
        """ Called when an image has been fetched. """
        url = imageTuple[0]
        image = imageTuple[1]
        self.imageCache.addImage(url, image)
        print("Just added image: {} (cache length: {})".format(url, self.imageCache.cacheSize()))
