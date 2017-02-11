import logging
from PyQt5 import QtCore, QtGui, QtWidgets


kRowHeight = 20

class FeedTree(QtCore.QObject):
    feedSelectedSignal = QtCore.pyqtSignal(int)
    feedUpdateRequestedSignal = QtCore.pyqtSignal(int)

    def __init__(self, treeWidget):
        super(FeedTree, self).__init__()
        self.feedTree = treeWidget
        self.lastClickedFeedId = -1     # ID of feed item that was most-recently clicked
        self.feedTree.currentItemChanged.connect(self.onItemActivated)
        self.feedTree.customContextMenuRequested.connect(self.onContextMenu)
        self.InitializeContextMenu()

    def InitializeContextMenu(self):
        self.m_contextMenu = QtWidgets.QMenu()

        self.m_actionUpdate = QtWidgets.QAction("Update Feed")
        self.m_actionMarkRead = QtWidgets.QAction("Mark Feed As Read")
        self.m_actionMarkUnread = QtWidgets.QAction("Mark Feed As Unread")
        self.m_actionPurge = QtWidgets.QAction("Purge Feed")
        self.m_actionDeleteFeed = QtWidgets.QAction("Delete Feed")
        self.m_feedProperties = QtWidgets.QAction("Feed Properties")

        self.m_actionUpdate.triggered.connect(self.onActionUpdate)

        self.m_contextMenu.addAction(self.m_actionUpdate)
        self.m_contextMenu.addAction(self.m_actionMarkRead)
        self.m_contextMenu.addAction(self.m_actionMarkUnread)
        self.m_contextMenu.addAction(self.m_actionPurge)
        self.m_contextMenu.addAction(self.m_actionDeleteFeed)
        self.m_contextMenu.addSeparator()
        self.m_contextMenu.addAction(self.m_feedProperties)

    def addFeeds(self, feedList):
        self.feedTree.currentItemChanged.disconnect(self.onItemActivated)
        for feed in feedList:
            self.addFeedToTopLevel(feed)
        self.feedTree.currentItemChanged.connect(self.onItemActivated)

    def addFeedToTopLevel(self, feed):
        feedIcon = QtGui.QIcon(feed.m_feedFavicon)
        pNewItem = QtWidgets.QTreeWidgetItem()

        if feed.m_feedName:
            pNewItem.setText(0, feed.m_feedName)
            pNewItem.setData(0, QtCore.Qt.UserRole, feed.m_feedId)

            if not feedIcon.isNull():
                pNewItem.setIcon(0, feedIcon)

            curSizeHint = pNewItem.sizeHint(0)
            curSizeHint.setHeight(kRowHeight)

            pNewItem.setSizeHint(0, curSizeHint)

            self.feedTree.addTopLevelItem(pNewItem)
            self.feedTree.setCurrentItem(pNewItem)

    def onItemActivated(self, current, previous):
        feedId = current.data(0, QtCore.Qt.UserRole)
        self.lastClickedFeedId = feedId
        print("Item clicked: {}, feed ID: {}".format(current.text(0), feedId))
        #logging.info("Item clicked: {}".format(item.text(column)))
        self.feedSelectedSignal.emit(feedId)

    def onContextMenu(self, pos):
        item = self.feedTree.itemAt(pos)

        # For now, don 't support a context menu on the Items of Interest feed
        globalPos = self.feedTree.mapToGlobal(pos)

        self.m_contextMenu.popup(globalPos)

    def onActionUpdate(self, checked):
        self.feedUpdateRequestedSignal.emit(self.lastClickedFeedId)
