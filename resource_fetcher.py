import logging
from urllib import request
from urllib.request import Request, ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, urlopen, HTTPError, URLError
from PyQt5 import QtGui, QtCore

class ResourceFetcher(object):
    def __init__(self, url, proxy):
        super(ResourceFetcher, self).__init__()
        self.proxy = proxy

        try:
            if self.proxy.usesProxy():
                proxyAndPortStr = 'http://{}:{}@{}:{}'.format(self.proxy.proxyUser, self.proxy.proxyPassword, self.proxy.proxyUrl, self.proxy.proxyPort)
                proxy_handler = ProxyHandler({'http': 'http://{}:{}@{}:{}'.format(self.proxy.proxyUser, self.proxy.proxyPassword, self.proxy.proxyUrl, self.proxy.proxyPort),
                                              'https': 'https://{}:{}@{}:{}'.format(self.proxy.proxyUser, self.proxy.proxyPassword, self.proxy.proxyUrl, self.proxy.proxyPort)})
                proxy_auth_handler = HTTPBasicAuthHandler()
                #proxy_auth_handler.add_password('realm', self.proxy.proxyUrl, self.proxy.proxyUser, self.proxy.proxyPassword)
                opener = request.build_opener(proxy_handler, proxy_auth_handler, HTTPHandler)

                # This installs it globally, so it can be used with urlopen().
                request.install_opener(opener)

            self.request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            self.data = urlopen(self.request).read()
        except HTTPError as e:
            errMsg = "HTTP error fetching: {}: {}".format(url, e.code)
            print(errMsg)
            logging.error(errMsg)

            # Set a NULL image to data
            nullImage = QtGui.QImage()
            byteArray = QtCore.QByteArray()
            buffer =  QtCore.QBuffer(byteArray)
            buffer.open(QtCore.QIODevice.WriteOnly)
            nullImage.save(buffer, "PNG")
            self.data = byteArray
        except URLError as e:
            errMsg = "URL Error fetching: {}: {}".format(url, e.reason)
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
