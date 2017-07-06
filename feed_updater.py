import datetime
from feed_update_thread import FeedUpdateThread
from proxy import Proxy
from PyQt5 import QtCore

# Show feed update messages for 10 seconds
kMessageTimeout = 10000

class FeedUpdater(QtCore.QObject):
    # Emitted when feed items are available to be stored into the database.
    # Parameters: feedID, list of feed items
    feedItemUpdateSignal = QtCore.pyqtSignal(int, list)
    feedUpdateMessageSignal = QtCore.pyqtSignal(str, int)

    def __init__(self, db):
        super(FeedUpdater, self).__init__()
        self.db = db
        self.proxy = Proxy()
        self.lastUpdatedDate = datetime.datetime.today()

    def updateFeed(self, feedId, proxy):
        """ Updates the given feed. """
        self.feedId = feedId
        feed = self.db.getFeed(feedId)
        self.lastUpdatedDate = feed.m_feedLastUpdated
        self.lastPurgedDate = feed.m_feedLastPurged
        guids = self.db.getFeedItemGuids(feedId)
        self.proxy = proxy

        updateMessage = "Updating {}".format(feed.m_feedTitle)
        self.feedUpdateMessageSignal.emit(updateMessage, kMessageTimeout)

        self.feedUpdateThread = FeedUpdateThread(feed.m_feedUrl, guids, self.proxy)
        self.feedUpdateThread.feedUpdateDoneSignal.connect(self.onFeedUpdateDone)
        self.feedUpdateThread.start()

    @QtCore.pyqtSlot(list)
    def onFeedUpdateDone(self, feedItemList):
        self.db.updateFeedLastUpdatedField(self.feedId, datetime.datetime.today())

        finalFeedItemList = []
        for feedItem in feedItemList:
            if feedItem.m_publicationDatetime >= self.lastUpdatedDate and \
                feedItem.m_publicationDatetime >= self.lastPurgedDate:
                finalFeedItemList.append(feedItem)

        # Pass this on up to the main window
        self.feedItemUpdateSignal.emit(self.feedId, finalFeedItemList)
