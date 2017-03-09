from PyQt5 import QtGui
from cachetools import LRUCache


class ImageCache:
    def __init__(self, maxSize):
        super(ImageCache, self).__init__()

        self.cache = LRUCache(maxSize)

    def addImage(self, url, image):
        self.cache[url] = image

    def contains(self, url):
        return url in self.cache

    def getImage(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            return QtGui.QPixmap()

    def cacheSize(self):
        return len(self.cache)
