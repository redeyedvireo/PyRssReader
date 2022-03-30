from PyQt5 import QtCore
from feed_item_parser import parseFeed
from feed_item_debugger import debugParseFeed
from resource_fetcher import ResourceFetcher

# Use DEBUG = True to invoke feed parse debugging
#DEBUG = True
DEBUG = False


class FeedUpdateThreadDebug(QtCore.QObject):
    feedUpdateDoneSignal = QtCore.pyqtSignal(list)

    def __init__(self, feedUrl, existingGuids, proxy):
        super(FeedUpdateThreadDebug, self).__init__()
        self.feedUrl = feedUrl
        self.existingGuids = existingGuids
        self.proxy = proxy

    def start(self):
        # This is the guts of the fetch operation
        resourceFetcher = ResourceFetcher(self.feedUrl, self.proxy)
        feedText = resourceFetcher.getData()

        if feedText is None:
            self.feedUpdateDoneSignal.emit([])
            return

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
