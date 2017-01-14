import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from title_tree_widget_item import TitleTreeWidgetItem, kTitleColumn

kRowHeight = 17
kEnclosureColumnWidth = 40


class TitleTree(QtCore.QObject):
    def __init__(self, treeWidget):
        super(TitleTree, self).__init__()

        self.titleTreeWidget = treeWidget
        self.titleTreeWidget.currentItemChanged.connect(self.onItemChanged)
        self.m_Grouper = None

    def onItemChanged(self, current, previous):
        pass

    def addFeedItem(self, feedItem):
        treeWidgetItem = TitleTreeWidgetItem(feedItem, self.titleTreeWidget)

        curSizeHint = treeWidgetItem.sizeHint(kTitleColumn)
        curSizeHint.setHeight(kRowHeight)

        treeWidgetItem.setSizeHint(kTitleColumn, curSizeHint)

        if self.m_Grouper is not None:
            #m_Grouper.AddItem(pTreeItem)
            pass
        else:
            self.titleTreeWidget.addTopLevelItem(treeWidgetItem)

    def addFeedItems(self, feedItemList):
        self.titleTreeWidget.currentItemChanged.disconnect()

        self.titleTreeWidget.clear()

        for feedItem in feedItemList:
            self.addFeedItem(feedItem)

        self.titleTreeWidget.currentItemChanged.connect(self.onItemChanged)
