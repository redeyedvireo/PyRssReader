import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from language_filter import LanguageFilter
from prefetch_controller import PrefetchController
from title_tree_view_item import TitleTreeViewItem, kEnclosureColumn, kTitleColumn, kDateColumn, kCreatorColumn, kTagsColumn, kNumColumns
from title_tree_date_item import TitleTreeDateItem
from title_tree_title_item import TitleTreeTitleItem
from title_tree_categories_item import TitleTreeCategoriesItem

kRowHeight = 17
kEnclosureColumnWidth = 40

class TitleTree(QtCore.QObject):
    # Signal emitted when a feed item is selected in the title tree.  Parameters are: feed ID, guid.
    feedItemSelectedSignal = QtCore.pyqtSignal(int, str)

    # Signal emitted when feed item images should be preselected.  The list is a list of tuples of the form:
    # (feedId, guids).
    prefetchImagesSignal = QtCore.pyqtSignal(list)

    movementKeys = [ QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown ]

    def __init__(self, treeView, languageFilter, keyboardHandler, imagePrefetcher):
        super(TitleTree, self).__init__()

        self.languageFilter = languageFilter
        self.titleTreeView = treeView
        self.keyboardHandler = keyboardHandler
        self.imagePrefetcher = imagePrefetcher
        self.sortColumn = kDateColumn
        self.feedItemGuid = ""
        self.sortOrder = QtCore.Qt.DescendingOrder
        self.configureTree()
        self.titleTreeView.header().sortIndicatorChanged.connect(self.onSortIndicatorChanged)
        self.enableUserActions()
        self.m_Grouper = None
        self.titleTreeView.installEventFilter(self)

        # Prefetch control
        self.prefetchController = PrefetchController()

        self.keyboardHandler.nextFeedItemSignal.connect(self.gotoNextFeedItem)
        self.keyboardHandler.previousFeedItemSignal.connect(self.gotoPreviousFeedItem)

    def configureTree(self):
        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(kNumColumns)
        self.model.setHorizontalHeaderLabels(["Enclosure", "Title", "Date", "Creator", "Categories"])
        self.titleTreeView.setModel(self.model)
        self.titleTreeView.setSortingEnabled(True)
        self.titleTreeView.sortByColumn(self.sortColumn, self.sortOrder)
        self.titleTreeView.setUniformRowHeights(True)

    def enableUserActions(self):
        """ Enables the tree to respond to user actions. """
        self.titleTreeView.clicked.connect(self.onItemChanged)
        self.titleTreeView.activated.connect(self.onItemChanged)

    def disableUserActions(self):
        """ Disables the tree to respond to user actions. """
        self.titleTreeView.clicked.disconnect()
        self.titleTreeView.activated.disconnect()

    def eventFilter(self, obj, event):
        if obj == self.titleTreeView:
            if event.type() == QtCore.QEvent.KeyRelease:
                keyCode = event.key()
                print("key: {}".format(keyCode))
                if not self.keyboardHandler.handleKey(keyCode):
                    self.handleKeyRelease(keyCode)
                return False

        return QtWidgets.QTreeView.eventFilter(self.titleTreeView, obj, event)

    def handleKeyRelease(self, keyName):
        if keyName in self.movementKeys:
            # Qt takes care of moving the selected item.  All we need to do is update the content view.
            self.onItemChanged(self.titleTreeView.currentIndex())

    def gotoNextFeedItem(self):
        currentRow = self.titleTreeView.currentIndex().row()
        if currentRow < self.model.rowCount() - 1:
            self.selectRow(currentRow + 1)

    def gotoPreviousFeedItem(self):
        currentRow = self.titleTreeView.currentIndex().row()
        if currentRow > 0:
            self.selectRow(currentRow - 1)

    def reselectFeedItem(self):
        """ Causes the feedItemSelectedSignal to be emitted for the current feed item.
            This is usually needed to reread a feed item after the language filter, or ad filter,
            has been changed.  At this point, the language filter has already been updated with new filter strings. """
        self.feedItemSelectedSignal.emit(self.feedId, self.feedItemGuid)

        # Rerun the language filter on the feed item's title, so it is updated in the title tree
        row = self.findFeedItem(self.feedItemGuid)
        item = self.model.item(row, kTitleColumn)
        currentText = item.text()
        item.setDisplayText(self.languageFilter.filterString(currentText))

    def onItemChanged(self, index):
        item = self.model.item(index.row(), kTitleColumn)
        self.feedItemGuid = item.guid()
        self.feedId = item.feedId()
        print("Row clicked: {}, Feed ID: {} GUID: {}".format(item.row(), self.feedId, self.feedItemGuid))
        self.feedItemSelectedSignal.emit(self.feedId, self.feedItemGuid)
        self.markRowAsRead(item.row())
        self.prefetchController.rowSelected(item.row())
        if (self.prefetchController.prefetchNeeded()):
            self.prefetchImages()

    def onSortIndicatorChanged(self, logicalIndex, order):
        self.sortColumn = logicalIndex
        self.sortOrder = order

    def addFeedItem(self, feedItem):
        bRead = feedItem.m_bRead
        guid = feedItem.m_guid
        feedId = feedItem.m_parentFeedId
        itemList = []

        # Enclosure
        enclosureItem = TitleTreeViewItem("", bRead, feedId, guid)
        itemList.append(enclosureItem)

        # Title
        displayText = self.languageFilter.filterString(feedItem.m_title)
        titleItem = TitleTreeTitleItem(feedItem.m_title, displayText, bRead, feedId, guid)
        itemList.append(titleItem)

        # Date
        dateItem = TitleTreeDateItem(feedItem.m_publicationDatetime, bRead, feedId, guid)
        itemList.append(dateItem)

        # Creator
        creatorItem = TitleTreeViewItem(feedItem.m_author, bRead, feedId, guid)
        itemList.append(creatorItem)

        # Categories
        categoriesItem = TitleTreeCategoriesItem(feedItem.m_categories, bRead, feedId, guid)
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

    def addFeedItems(self, feedItemList, sameFeed=False):
        """ Removes existing feed items from the tree, if any, and adds the given feed item list.
            If sameFeed is True, the feed items are from the same feed as the tree was already
            displaying.  In that case, an attempt is made to keep the same feed item selected. """
        self.disableUserActions()

        numRows = self.model.rowCount()
        if numRows > 0:
            self.model.removeRows(0, numRows)

        if len(feedItemList) > 0:
            for feedItem in feedItemList:
                self.addFeedItem(feedItem)

            self.titleTreeView.sortByColumn(self.sortColumn, self.sortOrder)
            self.model.sort(self.sortColumn, self.sortOrder)

            rowToSelect = 0
            if sameFeed and self.feedItemGuid:
                currentFeedItemRow = self.findFeedItem(self.feedItemGuid)
                rowToSelect = currentFeedItemRow if currentFeedItemRow >= 0 else 0

            self.selectRow(rowToSelect)

            self.prefetchController.setNumRows(len(feedItemList))
            self.prefetchImages()

        self.enableUserActions()

    def findFeedItem(self, guid):
        """ Returns the row containing the given GUID, or -1 if not found. """
        foundRow = -1
        numRows = self.model.rowCount()
        for row in range(numRows):
            if guid == self.getGuidForRow(row):
                return row
        return foundRow

    def getGuidForRow(self, row):
        item = self.model.item(row, kTitleColumn)
        return item.guid()

    def getFeedIdForRow(self, row):
        item = self.model.item(row, kTitleColumn)
        return item.feedId()

    def selectRow(self, row):
        index = self.model.index(row, 0)
        self.titleTreeView.setCurrentIndex(index)
        self.onItemChanged(index)

    def markRowAsRead(self, row):
        """ Marks all tree items in the given row as read. """
        for column in range(0, kNumColumns):
            item = self.model.item(row, column)
            item.setReadState(True)

    def prefetchImages(self):
        """ Prefetches images for the next few feeds. """
        fetchList = []
        for row in self.prefetchController.prefetchList():
            feedId = self.getFeedIdForRow(row)
            guid = self.getGuidForRow(row)
            fetchList.append( (feedId, guid) )
        self.imagePrefetcher.prefetchImages(fetchList)

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

    def getSortColumn(self):
        return self.sortColumn

    def setSortColumn(self, column):
        self.sortColumn = column

    def getSortOrder(self):
        return self.sortOrder

    def setSortOrder(self, order):
        self.sortOrder = order
