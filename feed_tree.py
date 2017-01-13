import logging
from PyQt5 import QtCore, QtNetwork, QtWidgets


kRowHeight = 20

class FeedTree(object):
    def __init__(self, treeWidget):
        super(FeedTree).__init__()
        self.feedTree = treeWidget
        self.feedTree.itemClicked.connect(self.onItemClicked)

    def addFeedToTopLevel(self, feedName, feedId, feedIcon):
        pNewItem = QtWidgets.QTreeWidgetItem()

        if feedName:
            pNewItem.setText(0, feedName)
            pNewItem.setData(0, QtCore.Qt.UserRole, feedId)

            if not feedIcon.isNull():
                pNewItem.setIcon(0, feedIcon)

            curSizeHint = pNewItem.sizeHint(0)
            curSizeHint.setHeight(kRowHeight)

            pNewItem.setSizeHint(0, curSizeHint)

            self.feedTree.addTopLevelItem(pNewItem)
            self.feedTree.setCurrentItem(pNewItem)

    def onItemClicked(self, item, column):
        print("Item clicked: {}".format(item.text(column)))
        #logging.info("Item clicked: {}".format(item.text(column)))
