import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from feed import Feed
from utility import getResourceFilePixmap
from feed import kItemsOfInterestFeedId
from FeedPropertiesDlg import FeedPropertiesDialog

kStarIcon = "star.png"

kRowHeight = 20

class FeedTree(QtCore.QObject):
    feedSelectedSignal = QtCore.pyqtSignal(int)
    feedUpdateRequestedSignal = QtCore.pyqtSignal(int)
    feedReadStateSignal = QtCore.pyqtSignal(int, bool)
    feedPurgeSignal = QtCore.pyqtSignal(int)
    feedDeleteSignal = QtCore.pyqtSignal(int)

    def __init__(self, treeWidget, db, keyboardHandler):
        super(FeedTree, self).__init__()

        self.feedTree = treeWidget
        self.db = db
        self.keyboardHandler = keyboardHandler
        self.lastClickedFeedId = -1     # ID of feed that was most-recently clicked
        self.feedTree.currentItemChanged.connect(self.onItemActivated)
        self.feedTree.customContextMenuRequested.connect(self.onContextMenu)
        self.InitializeContextMenu()
        self.feedTree.installEventFilter(self)

        self.keyboardHandler.nextFeedSignal.connect(self.onNextFeed)
        self.keyboardHandler.previousFeedSignal.connect(self.onPreviousFeed)

    def InitializeContextMenu(self):
        self.m_contextMenu = QtWidgets.QMenu()

        self.m_actionUpdate = QtWidgets.QAction("Update Feed")
        self.m_actionMarkRead = QtWidgets.QAction("Mark Feed As Read")
        self.m_actionMarkUnread = QtWidgets.QAction("Mark Feed As Unread")
        self.m_actionPurge = QtWidgets.QAction("Purge Feed")
        self.m_actionDeleteFeed = QtWidgets.QAction("Delete Feed")
        self.m_feedProperties = QtWidgets.QAction("Feed Properties")

        self.m_actionUpdate.triggered.connect(self.onActionUpdate)
        self.m_feedProperties.triggered.connect(self.onFeedProperties)
        self.m_actionMarkRead.triggered.connect(self.onMarkFeedAsRead)
        self.m_actionMarkUnread.triggered.connect(self.onMarkFeedAsUnread)
        self.m_actionPurge.triggered.connect(self.onPurgeFeed)
        self.m_actionDeleteFeed.triggered.connect(self.onDeleteFeed)

        self.m_contextMenu.addAction(self.m_actionUpdate)
        self.m_contextMenu.addAction(self.m_actionMarkRead)
        self.m_contextMenu.addAction(self.m_actionMarkUnread)
        self.m_contextMenu.addAction(self.m_actionPurge)
        self.m_contextMenu.addAction(self.m_actionDeleteFeed)
        self.m_contextMenu.addSeparator()
        self.m_contextMenu.addAction(self.m_feedProperties)

    def eventFilter(self, obj, event):
        if obj == self.feedTree:
            if event.type() == QtCore.QEvent.KeyRelease:
                keyCode = event.key()
                self.keyboardHandler.handleKey(keyCode)
                return False

        return QtWidgets.QTreeWidget.eventFilter(self.feedTree, obj, event)

    def addFeed(self, feed):
        """ Public function to use for adding a feed to the feed tree. """
        self.addFeedToTopLevel(feed)

    def addFeeds(self, feedList, feedOrderList):
        if len(feedList) != len(feedOrderList):
            logging.error("FeedTree: number of feeds does not equal the length of the feed order list.")
        self.feedTree.currentItemChanged.disconnect(self.onItemActivated)
        ioiFeed = self.createItemsOfInterestFeed()
        self.addFeedToTopLevel(ioiFeed)

        for feedId in feedOrderList:
            feed = self.findFeedInList(feedList, feedId)
            if feed is not None:
                self.addFeedToTopLevel(feed)
            else:
                logging.error("FeedTree: unknown feed ID in feed order list: {}".format(feedId))

        self.updateAllFeedCounts()
        self.feedTree.currentItemChanged.connect(self.onItemActivated)

    def findFeedInList(self, feedList, feedId):
        """ Finds the given feed in the given feed list."""
        for feed in feedList:
            if feed.m_feedId == feedId:
                return feed
        return None

    def createItemsOfInterestFeed(self):
        ioiFeed = Feed()
        ioiFeed.m_feedFavicon = getResourceFilePixmap(kStarIcon)
        ioiFeed.m_feedName = "Items of Interest"
        ioiFeed.m_feedId = kItemsOfInterestFeedId
        return ioiFeed

    def addFeedToTopLevel(self, feed):
        feedIcon = QtGui.QIcon(feed.getFeedIcon())
        pNewItem = QtWidgets.QTreeWidgetItem()

        if feed.feedName():
            pNewItem.setText(0, feed.feedName())
            pNewItem.setData(0, QtCore.Qt.UserRole, feed.m_feedId)
            pNewItem.setData(0, QtCore.Qt.UserRole+1, feed.feedName())

            if not feedIcon.isNull():
                pNewItem.setIcon(0, feedIcon)

            curSizeHint = pNewItem.sizeHint(0)
            curSizeHint.setHeight(kRowHeight)

            pNewItem.setSizeHint(0, curSizeHint)

            self.feedTree.addTopLevelItem(pNewItem)
            self.feedTree.setCurrentItem(pNewItem)

    def removeFeed(self, feedId):
        """ Removes a feed from the tree. """
        feedTreeItem = self.findFeed(feedId)

        if feedTreeItem is not None:
            rootItem = self.feedTree.invisibleRootItem()
            index = rootItem.indexOfChild(feedTreeItem)
            rootItem.takeChild(index)
        else:
            logging.error("FeedTree.removeFeed: feedId {} not found in tree.".format(feedId))

    def updateAllFeedCounts(self):
        curItem = self.feedTree.invisibleRootItem()
        curItem = curItem.child(0)

        while curItem is not None:
            curfeedId = self.feedIdForItem(curItem)
            self.updateFeedCountForItem(curItem, curfeedId)

            curItem = self.feedTree.itemBelow(curItem)

    def updateFeedCount(self, feedId):
        """ Updates the feed count for the given feed ID. """
        item = self.findFeed(feedId)
        if item is not None:
            self.updateFeedCountForItem(item, feedId)

            # Also update the Items of Interest feed
            item = self.findFeed(kItemsOfInterestFeedId)
            self.updateFeedCountForItem(item, kItemsOfInterestFeedId)

    def updateFeedCountForItem(self, treeWidgetItem, feedId):
        """ Updates the feed count for the given tree widget item. """
        feedName = self.feedNameForItem(treeWidgetItem)
        if feedId == kItemsOfInterestFeedId:
            unreadItems = self.db.getUnreadCountForItemsOfInterest()
        else:
            unreadItems = self.db.getFeedItemUnreadCount(feedId)

        itemFont = treeWidgetItem.font(0)
        itemFont.setBold(unreadItems > 0)
        treeWidgetItem.setFont(0, itemFont)
        if unreadItems > 0:
            treeWidgetItem.setText(0, "{} ({})".format(feedName, unreadItems))
        else:
            treeWidgetItem.setText(0, feedName)

    def setCurrentFeed(self, feedId):
        """ Sets the given feedId to be the currently-selected feed. """
        item = self.findFeed(feedId)
        if item is not None:
            self.feedTree.setCurrentItem(item)

    def findFeed(self, feedId):
        """ Finds the feed with the given feedId.  If not found, None is returned. """
        curItem = self.feedTree.invisibleRootItem()
        curItem = curItem.child(0)

        while curItem is not None:
            curfeedId = self.feedIdForItem(curItem)
            if curfeedId == feedId:
                return curItem
            curItem = self.feedTree.itemBelow(curItem)

        return None

    def feedIdForItem(self, item):
        """ Returns the feed ID for the given item. """
        return item.data(0, QtCore.Qt.UserRole)

    def feedNameForItem(self, item):
        """ Returns the feed name for the given item. """
        return item.data(0, QtCore.Qt.UserRole+1)

    def onItemActivated(self, current, previous):
        feedId = current.data(0, QtCore.Qt.UserRole)
        self.lastClickedFeedId = feedId
        print("Item clicked: {}, feed ID: {}".format(current.text(0), feedId))
        #logging.info("Item clicked: {}".format(item.text(column)))
        self.feedSelectedSignal.emit(feedId)

    def onContextMenu(self, pos):
        item = self.feedTree.itemAt(pos)

        # For now, don't support a context menu on the Items of Interest feed
        globalPos = self.feedTree.mapToGlobal(pos)

        self.m_contextMenu.popup(globalPos)

    def onActionUpdate(self, checked):
        self.feedUpdateRequestedSignal.emit(self.lastClickedFeedId)

    def onNextFeed(self):
        currentItem = self.feedTree.currentItem()
        nextItem = self.feedTree.itemBelow(currentItem)
        if nextItem is not None:
            self.feedTree.setCurrentItem(nextItem)

    def onPreviousFeed(self):
        currentItem = self.feedTree.currentItem()
        previousItem = self.feedTree.itemAbove(currentItem)
        if previousItem is not None:
            self.feedTree.setCurrentItem(previousItem)

    def onFeedProperties(self):
        dlg = FeedPropertiesDialog(self.feedTree, self.db, self.lastClickedFeedId)

        dlg.exec()

    def onMarkFeedAsRead(self):
        self.feedReadStateSignal.emit(self.lastClickedFeedId, True)
        self.updateFeedCount(self.lastClickedFeedId)

    def onMarkFeedAsUnread(self):
        self.feedReadStateSignal.emit(self.lastClickedFeedId, False)
        self.updateFeedCount(self.lastClickedFeedId)

    def onPurgeFeed(self):
        self.feedPurgeSignal.emit(self.lastClickedFeedId)
        self.updateFeedCount(self.lastClickedFeedId)

    def onDeleteFeed(self):
        self.feedDeleteSignal.emit(self.lastClickedFeedId)

        # Remove the feed from the feed tree
        self.removeFeed(self.lastClickedFeedId)

    def getFeedOrder(self):
        """ Generates a comma-separated list of feed IDs, used to store the feed order in the database. """
        feedIdList = []
        curItem = self.feedTree.invisibleRootItem()
        curItem = curItem.child(0)

        while curItem is not None:
            curfeedId = self.feedIdForItem(curItem)
            if curfeedId != kItemsOfInterestFeedId:
                feedIdList.append(str(curfeedId))
            curItem = self.feedTree.itemBelow(curItem)

        return feedIdList
