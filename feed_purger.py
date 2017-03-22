from PyQt5 import QtCore, QtWidgets
import datetime
import time
from dateutil.relativedelta import *

class FeedPurger(QtCore.QObject):

    # Emitted when a feed has been purged.  The parameter is the feed ID
    feedPurgedSignal = QtCore.pyqtSignal(int)
    messageSignal = QtCore.pyqtSignal(str, int)

    def __init__(self, db, parent):
        super(FeedPurger, self).__init__(parent)
        self.parent = parent
        self.db = db

    def purgeAllFeeds(self, priorDays, purgeUnreadItems):
        feedList = self.db.getFeeds()
        numFeeds = len(feedList)
        targetDate = datetime.date.today() + relativedelta(days=-priorDays)
        print("Today: {}, target date: {}".format(datetime.date.today(), targetDate))

        if numFeeds == 0:
            return

        self.progressDialog = QtWidgets.QProgressDialog("Purging Feeds", "Abort", 0, numFeeds-1, self.parent)
        self.progressDialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progressDialog.setWindowTitle("Purge Feeds")

        for index, feed in enumerate(feedList):
            self.progressDialog.setLabelText("Purging: {}".format(feed.m_feedTitle))
            self.progressDialog.setValue(index)
            if self.progressDialog.wasCanceled():
                return

            self.db.deleteFeedItemsByDate(feed.m_feedId, targetDate, purgeUnreadItems)
            self.db.updateFeedLastPurgedField(feed.m_feedId, targetDate)
            self.feedPurgedSignal.emit(feed.m_feedId)

        self.progressDialog.setValue(numFeeds-1)
        self.removeDeletedItems()
        self.db.vacuumDatabase()
        self.messageSignal.emit("Feeds purged.", 10000)

    def purgeSingleFeed(self, feedId, priorDays, purgeUnreadItems):
        """ Purges a single feed. """
        feed = self.db.getFeed(feedId)

        targetDate = datetime.date.today() + relativedelta(days=-priorDays)
        print("Today: {}, target date: {}".format(datetime.date.today(), targetDate))

        self.db.deleteFeedItemsByDate(feedId, targetDate, purgeUnreadItems)
        self.db.updateFeedLastPurgedField(feedId, targetDate)
        self.feedPurgedSignal.emit(feedId)

        self.removeDeletedItems()
        self.db.vacuumDatabase()
        self.messageSignal.emit("{} purged.".format(feed.m_feedTitle), 10000)

    def removeDeletedItems(self):
        """ Removes deleted items from the Items of Interest feed."""
        self.db.beginTransaction()

        ioiList = self.db.getItemsOfInterest()

        for itemOfInterestTuple in ioiList:
            feedId = itemOfInterestTuple[0]
            guid = itemOfInterestTuple[1]
            itemExists = self.db.feedItemExists(feedId, guid)
            if not itemExists:
                self.db.deleteItemOfInterest(feedId, guid)

        self.db.endTransaction()
