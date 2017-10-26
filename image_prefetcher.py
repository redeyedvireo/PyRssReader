from PyQt5 import QtCore
from image_prefetch_thread import ImagePrefetchThread


class ImagePrefetcher(QtCore.QObject):
    # Signal emitted when image prefetching is starting.
    imagePrefetchStartingSignal =  QtCore.pyqtSignal()

    # Signal emitted when all images have been fetched.
    imagePrefetchDoneSignal = QtCore.pyqtSignal()

    def __init__(self, db, imageCache, proxy):
        super(ImagePrefetcher, self).__init__()
        self.db = db
        self.proxy = proxy
        self.imageCache = imageCache
        self.imagePrefetchThread = None
        self.feedItemList = None
        self.feed = None

    def prefetchImages(self, feedItemList, feed):
        """ Prefetches images from the given feed items.  feedItemList is a list of tuples of the
            form: (feedId, guid). """
        self.feedItemList = feedItemList
        self.feed = feed

        # If prefetching is ongoing, terminate it before starting a new fetch
        if self.imagePrefetchThread is not None:
            # The thread's finished() signal will trigger the onPrefetchDone slot to be called,
            # which will start the next request.
            self.imagePrefetchThread.abortFetching()
        else:
            self.startPrefetchThread()

    def startPrefetchThread(self):
        feedItems = self.db.getFeedItemsFromList(self.feedItemList)

        self.imagePrefetchThread = ImagePrefetchThread(feedItems, self.feed, self.proxy)
        self.imagePrefetchThread.imageReadySignal.connect(self.onImagePrefetched)
        self.imagePrefetchThread.finished.connect(self.onPrefetchDone)

        self.imagePrefetchStartingSignal.emit()

        # Remove prefetch request from members, to indicate that there is not a prefetch request pending
        self.feedItemList = None
        self.feed = None
        self.imagePrefetchThread.start()

    @QtCore.pyqtSlot(tuple)
    def onImagePrefetched(self, imageTuple):
        """ Called when an image has been fetched. """
        url = imageTuple[0]
        image = imageTuple[1]
        self.imageCache.addImage(url, image)
        #print("Just added image: {} (cache length: {})".format(url, self.imageCache.cacheSize()))

    @QtCore.pyqtSlot()
    def onPrefetchDone(self):
        if self.feedItemList is not None:
            # There is a prefetch request pending
            self.startPrefetchThread()
        else:
            self.imagePrefetchThread = None
            self.imagePrefetchDoneSignal.emit()
