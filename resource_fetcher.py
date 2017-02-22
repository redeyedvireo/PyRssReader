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
                proxy_handler = ProxyHandler({'http': 'http://{}:{}@{}:{}'.format(self.proxy.proxyUser, self.proxy.proxyPassword, self.proxy.proxyUrl, self.proxy.proxyPort),
                                              'https': 'https://{}:{}@{}:{}'.format(self.proxy.proxyUser, self.proxy.proxyPassword, self.proxy.proxyUrl, self.proxy.proxyPort)})
                proxy_auth_handler = HTTPBasicAuthHandler()
                opener = request.build_opener(proxy_handler, proxy_auth_handler, HTTPHandler)

                # This installs it globally, so it can be used with urlopen().
                request.install_opener(opener)

            self.request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            self.data = urlopen(self.request).read()

        except URLError as e:
            if hasattr(e, 'reason'):
                errMsg = "Could not connect to server when fetching: {}: {}".format(url, e.reason)
            elif hasattr(e, 'code'):
                errMsg = "Could not fulfill request when fetching: {}: {}".format(url, e.code)

            print(errMsg)
            logging.error(errMsg)

            self.data = self.createNullImage()

    def getData(self):
        return self.data

    def createNullImage(self):
        nullImage = QtGui.QImage()
        byteArray = QtCore.QByteArray()
        buffer = QtCore.QBuffer(byteArray)
        buffer.open(QtCore.QIODevice.WriteOnly)
        nullImage.save(buffer, "PNG")
        return byteArray
