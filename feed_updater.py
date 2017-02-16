from feed_update_thread import FeedUpdateThread
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

    def updateFeed(self, feedId):
        """ Updates the given feed. """
        self.feedId = feedId
        feed = self.db.getFeed(feedId)
        guids = self.db.getFeedItemGuids(feedId)

        updateMessage = "Updating {}".format(feed.m_feedTitle)
        self.feedUpdateMessageSignal.emit(updateMessage, kMessageTimeout)

        self.feedUpdateThread = FeedUpdateThread(feed.m_feedUrl, guids)
        self.feedUpdateThread.feedUpdateDoneSignal.connect(self.onFeedUpdateDone)
        self.feedUpdateThread.start()

    @QtCore.pyqtSlot(list)
    def onFeedUpdateDone(self, feedItemList):
        # Pass this on up to the main window
        self.feedItemUpdateSignal.emit(self.feedId, feedItemList)
