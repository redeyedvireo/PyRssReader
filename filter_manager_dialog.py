from PyQt5 import uic, QtCore, QtWidgets
from filter_dialog import FilterDialog
from feed_item_filter import FeedItemFilter


kGlobalFeedItemFilter = 0

class FilterManagerDialog(QtWidgets.QDialog):
    def __init__(self, parent, db):
        super(FilterManagerDialog, self).__init__(parent)
        uic.loadUi('filter_manager_dialog.ui', self)
        self.db = db
        self.itemFilterList = []
        self.itemFilterMap = {}
        self.newFilterMap = {}              # Map of filters that were added
        self.deletedFilterIdList = []       # List of filter IDs that were deleted
        self.editedFilterIdList = []        # List of filter IDs that were edited
        self.addedFilterList = []           # List of filters that were added
        self.nextFilterId = -1              # Temporary values to use for the IDs of newly-created filters

        self.buttonBox.accepted.connect(self.onAccepted)

        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.getFiltersFromDatabase()

        for filter in self.itemFilterList:
            self.addFilter(filter)

    def addFilter(self, filter):
        """ Adds a filter to the list widget. """
        filterStr = FeedItemFilter.StringifyFilter(filter)
        listWidgetItem = QtWidgets.QListWidgetItem(filterStr)
        listWidgetItem.setData(QtCore.Qt.UserRole, filter.m_filterId)
        self.filterList.addItem(listWidgetItem)

    def getFiltersFromDatabase(self):
        self.itemFilterList = self.db.getFeedItemFilters()

        # Create the item filter map to make finding filters by ID quick
        for filter in self.itemFilterList:
            self.itemFilterMap[filter.m_filterId] = filter

    def getCurrentFilterId(self):
        currentRow = self.filterList.currentRow()
        if currentRow < 0:
            currentRow = 0

        pItem = self.filterList.item(currentRow)
        return pItem.data(QtCore.Qt.UserRole)

    def getFilter(self, filterId):
        """ Returns the filter with the given ID.  This is obtained from the itemFilterMap. """
        if filterId in self.itemFilterMap.keys():
            return self.itemFilterMap[filterId]
        elif filterId in self.newFilterMap.keys():
            return self.newFilterMap[filterId]
        else:
            return None

    def replaceFilter(self, filter):
        """ Replaces a filter with a new one.  The filter can be in either the itemFilterMap, or the newFilterMap. """
        filterId = filter.m_filterId
        if filterId in self.itemFilterMap.keys():
            self.itemFilterMap[filterId] = filter
        elif filterId in self.newFilterMap.keys():
            self.newFilterMap[filterId] = filter

    def getNewFiltersAsList(self):
        """ Returns a list of all new filters added. """
        return list(self.newFilterMap.values())

    def getEditedFiltersAsList(self):
        """ Returns a list of all edited filters. """
        filterList = []
        for filterId in self.editedFilterIdList:
            filterList.append(self.itemFilterMap[filterId])
        return filterList

    def takeNextFilterId(self):
        """ Returns the next filter ID to use for new filters, and updates the filter ID counter, so that the
            updated value will be returned the next time this function is called. """
        value = self.nextFilterId
        self.nextFilterId -= 1      # Update the value for next time
        return value

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        filterDlg = FilterDialog(self)
        if filterDlg.exec() == QtWidgets.QDialog.Accepted:
            newFilter = filterDlg.getFilter()
            id = self.takeNextFilterId()
            newFilter.m_filterId = id
            print("New filter: {}".format(newFilter))
            self.addFilter(newFilter)
            self.newFilterMap[id] = newFilter

    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        #  Get selected filter
        filterId = self.getCurrentFilterId()

        # Determine whether this filter is a newly-added filter, or pre-existing one
        if filterId < 0:
            # Newly-added.  Remove from the new filter map
            if filterId in self.newFilterMap.keys():
                self.newFilterMap.pop(filterId)
        else:
            # Pre-existing.  Add to the delete list
            self.deletedFilterIdList.append(filterId)

            # Remove from edited items, in case the user edited an item, and then later deleted it
            if filterId in self.editedFilterIdList:
                self.editedFilterIdList.remove(filterId)

        self.filterList.takeItem(self.filterList.currentRow())

    @QtCore.pyqtSlot()
    def on_editButton_clicked(self):
        filterId = self.getCurrentFilterId()
        filter = self.getFilter(filterId)
        filterDlg = FilterDialog(self)
        filterDlg.setFilter(filter)
        if filterDlg.exec() == QtWidgets.QDialog.Accepted:
            newFilter = filterDlg.getFilter()
            self.replaceFilter(newFilter)

            if filterId >= 0:
                # The edited filter list is only for pre-existing filters
                self.editedFilterIdList.append(filterId)

            # Update item in the list widget
            filterStr = FeedItemFilter.StringifyFilter(newFilter)
            item = self.filterList.currentItem()
            item.setText(filterStr)

    def onAccepted(self):
        print("Deleted items: {}".format(self.deletedFilterIdList))
        print("Edited items: {}".format(self.editedFilterIdList))
        print("New filters:")
        for filterId in self.newFilterMap:
            filter = self.newFilterMap[filterId]
            print(filter)

        self.db.updateFeedItemFilters(self.getEditedFiltersAsList())
        self.db.addFeedItemFilters(self.getNewFiltersAsList())
        self.db.deleteFeedItemFilters(self.deletedFilterIdList)

        self.accept()
