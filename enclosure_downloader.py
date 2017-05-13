from PyQt5 import QtCore
from urllib.parse import urlparse
import os.path
from resource_fetcher import ResourceFetcher


class EnclosureDownloader(QtCore.QThread):
    enclosureDownloadedSignal = QtCore.pyqtSignal(str)

    def __init__(self, url, downloadDirectory, proxy):
        super(EnclosureDownloader, self).__init__()
        self.enclosureUrl = url
        self.downloadDirectory = downloadDirectory
        self.proxy = proxy

        # Extract file name from URL
        parsedUrl = urlparse(self.enclosureUrl)
        self.filename = os.path.basename(parsedUrl.path)
        self.enclosurePath = os.path.join(self.downloadDirectory, self.filename)

    def run(self):
        if self.downloadDirectory:
            resourceFetcher = ResourceFetcher(self.enclosureUrl, self.proxy)
            enclosureData = resourceFetcher.getData()

            # Save data to file
            if os.path.exists(self.downloadDirectory):
                fileObj = open(self.enclosurePath, 'wb')
                fileObj.write(enclosureData)
                fileObj.close()

        self.enclosureDownloadedSignal.emit(self.filename)
