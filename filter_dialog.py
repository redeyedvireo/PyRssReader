from PyQt5 import uic, QtCore, QtWidgets
from feed_item_filter import FeedItemFilter


class FilterDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(FilterDialog, self).__init__(parent)
        uic.loadUi('filter_dialog.ui', self)
        self.filterId = 0

    def setFilter(self, filter):
        # Filter ID
        self.filterId = filter.m_filterId

        #Field ID
        self.fieldCombo.setCurrentIndex(filter.m_fieldId - 1)

        # Verb
        self.verbCombo.setCurrentIndex(filter.m_verb - 1)

        # Query string
        self.queryStrEdit.setText(filter.m_queryStr)

        # Action
        self.actionCombo.setCurrentIndex(filter.m_action - 1)

    def getFilter(self):
        filter = FeedItemFilter()

        # Filter ID
        filter.m_filterId = self.filterId

        # Field ID
        filter.m_fieldId = self.fieldCombo.currentIndex() + 1

        # Verb
        filter.m_verb = self.verbCombo.currentIndex() + 1

        # Query string
        filter.m_queryStr = self.queryStrEdit.text()

        # Action
        filter.m_action = self.actionCombo.currentIndex() + 1

        return filter
