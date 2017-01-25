import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from title_tree_view_item import TitleTreeViewItem, kEnclosureColumn, kTitleColumn, kDateColumn, kCreatorColumn, kTagsColumn, kNumColumns
from title_tree_date_item import TitleTreeDateItem
from title_tree_title_item import TitleTreeTitleItem
from title_tree_categories_item import TitleTreeCategoriesItem

kRowHeight = 17
kEnclosureColumnWidth = 40

class TitleTree(QtCore.QObject):
    feedItemSelectedSignal = QtCore.pyqtSignal(str)

    def __init__(self, treeView):
        super(TitleTree, self).__init__()

        self.titleTreeView = treeView
        self.configureTree()
        self.titleTreeView.clicked.connect(self.onItemChanged)
        self.m_Grouper = None

    def configureTree(self):
        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(kNumColumns)
        self.model.setHorizontalHeaderLabels(["Enclosure", "Title", "Date", "Creator", "Categories"])
        self.titleTreeView.setModel(self.model)

    def onItemChanged(self, index):
        item = self.model.item(index.row(), kTitleColumn)
        feedItemGuid = item.guid()
        print("Row clicked: {}, GUID: {}".format(index.row(), feedItemGuid))
        self.feedItemSelectedSignal.emit(feedItemGuid)

    def addFeedItem(self, feedItem):
        bRead = feedItem.m_bRead
        guid = feedItem.m_guid
        itemList = []

        # Enclosure
        enclosureItem = TitleTreeViewItem("", bRead, guid)
        itemList.append(enclosureItem)

        # Title
        displayText = feedItem.m_title      # TODO: Put through the language filter first
        titleItem = TitleTreeTitleItem(feedItem.m_title, displayText, bRead, guid)
        itemList.append(titleItem)

        # Date
        dateItem = TitleTreeDateItem(feedItem.m_publicationDatetime, bRead, guid)
        itemList.append(dateItem)

        # Creator
        creatorItem = TitleTreeViewItem(feedItem.m_author, bRead, guid)
        itemList.append(creatorItem)

        # Categories
        categoriesItem = TitleTreeCategoriesItem(feedItem.m_categories, bRead, guid)
        itemList.append(categoriesItem)

        if self.m_Grouper is not None:
            #m_Grouper.AddItem(pTreeItem)
            pass
        else:
            self.model.appendRow(itemList)
            self.setRowHeight(self.model.rowCount()-1)

    def setRowHeight(self, row):
        """ Sets the height of all items in the given row. """
        for column in range(kNumColumns):
            item = self.model.item(row, column)
            sizeHint = item.sizeHint()
            sizeHint.setHeight(kRowHeight)
            item.setSizeHint(sizeHint)

    def addFeedItems(self, feedItemList):
        self.titleTreeView.clicked.disconnect()

        numRows = self.model.rowCount()
        if numRows > 0:
            self.model.removeRows(0, numRows)

        for feedItem in feedItemList:
            self.addFeedItem(feedItem)

        self.titleTreeView.clicked.connect(self.onItemChanged)

    def GetColumnWidths(self):
        """ Returns the widths of all columns """
        columnList = []
        for i in range(kNumColumns):
            columnList.append(self.titleTreeView.columnWidth(i))

        return columnList

    def SetColumnWidths(self, columnList):
        """ Sets all column widths """
        for index, item in enumerate(columnList, start=0):
            self.titleTreeView.setColumnWidth(index, int(item))
