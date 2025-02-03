import logging
from urllib import request
from urllib.request import Request, ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, urlopen
from urllib.error import HTTPError, URLError
from PySide6 import QtGui, QtCore

from proxy import Proxy

class ResourceFetcher:
    def __init__(self, url, proxy: Proxy):
        super(ResourceFetcher, self).__init__()
        self.proxy = proxy

        try:
            if self.proxy.usesProxy():
                proxy_handler = ProxyHandler(self.proxy.getProxyDict())
                proxy_auth_handler = HTTPBasicAuthHandler()
                opener = request.build_opener(proxy_handler, proxy_auth_handler, HTTPHandler)

                # This installs it globally, so it can be used with urlopen().
                request.install_opener(opener)

            self.request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'})
            self.data = urlopen(self.request).read()

        except URLError as e:
            if hasattr(e, 'reason'):
                errMsg = "Could not connect to server when fetching: {}: {}".format(url, e.reason)
            elif hasattr(e, 'code'):
                errMsg = "Could not fulfill request when fetching: {}: {}".format(url, e.errno)
            else:
                errMsg = "Unknown URL Exception."

            logging.error(errMsg)

            self.data = None
        except ValueError as e:
            errMsg = "ValueError exception when fetching image: {}: {}".format(url, e)
            logging.error(errMsg)
            self.data = None
        except Exception as inst:
            errMsg = "Exception when fetching {}: {}".format(url, inst)
            logging.error(errMsg)
            self.data = None

    def getData(self):
        return self.data

    def getDataAsPixmap(self):
        """ Returns the data as a pixmap. """
        pixmap = QtGui.QPixmap()

        if self.data is not None:
            pixmap.loadFromData(self.data)

        return pixmap

    def createNullImage(self):
        nullImage = QtGui.QImage()
        byteArray = QtCore.QByteArray()
        buffer = QtCore.QBuffer(byteArray)
        buffer.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)
        nullImage.save(buffer, "PNG")
        return byteArray
