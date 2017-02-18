from PyQt5 import QtCore
from feed_item_parser import parseFeed
from feed_item_debugger import debugParseFeed
from resource_fetcher import ResourceFetcher

# Use DEBUG = True to invoke feed parse debugging
#DEBUG = True
DEBUG = False


class FeedUpdateThread(QtCore.QThread):
    feedUpdateDoneSignal = QtCore.pyqtSignal(list)

    def __init__(self, feedUrl, existingGuids, proxy):
        super(FeedUpdateThread, self).__init__()
        self.feedUrl = feedUrl
        self.existingGuids = existingGuids
        self.proxy = proxy

    def run(self):
        # This is the guts of the fetch operation
        resourceFetcher = ResourceFetcher(self.feedUrl, self.proxy)
        feedText = resourceFetcher.getData()

        if DEBUG:
            debugParseFeed(feedText)
            return
        else:
            feedItemList = parseFeed(feedText)

        noDuplicatesList = []

        for feedItem in feedItemList:
            if feedItem.m_guid not in self.existingGuids:
                noDuplicatesList.append(feedItem)
            #else:
            #    print("GUID: {} already exists".format(feedItem.m_guid))

        self.feedUpdateDoneSignal.emit(noDuplicatesList)
