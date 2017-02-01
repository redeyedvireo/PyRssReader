import logging
from urllib.request import Request, urlopen, HTTPError
from PyQt5 import QtGui, QtCore

class ResourceFetcher(object):
    def __init__(self, url):
        super(ResourceFetcher, self).__init__()
        try:
            self.request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            self.data = urlopen(self.request).read()
        except HTTPError as e:
            errMsg = "HTTP error fetching: {}".format(url)
            print(errMsg)
            logging.error(errMsg)

            # Set a NULL image to data
            nullImage = QtGui.QImage()
            byteArray = QtCore.QByteArray()
            buffer =  QtCore.QBuffer(byteArray)
            buffer.open(QtCore.QIODevice.WriteOnly)
            nullImage.save(buffer, "PNG")
            self.data = byteArray

    def getData(self):
        return self.data
