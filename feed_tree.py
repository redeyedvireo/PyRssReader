import logging
from PyQt5 import QtCore, QtGui, QtWidgets


kRowHeight = 20

class FeedTree(QtCore.QObject):
    feedSelectedSignal = QtCore.pyqtSignal(int)

    def __init__(self, treeWidget):
        super(FeedTree, self).__init__()
        self.feedTree = treeWidget
        self.feedTree.currentItemChanged.connect(self.onItemActivated)

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
        print("Item clicked: {}, feed ID: {}".format(current.text(0), feedId))
        #logging.info("Item clicked: {}".format(item.text(column)))
        self.feedSelectedSignal.emit(feedId)
