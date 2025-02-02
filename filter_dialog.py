from PySide6 import QtCore, QtWidgets
from feed_item_filter import FeedItemFilter
from ui_filter_dialog import Ui_FilterDialog


class FilterDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(FilterDialog, self).__init__(parent)

        self.ui = Ui_FilterDialog()
        self.ui.setupUi(self)

        self.filterId = 0

    def setFilter(self, filter):
        # Filter ID
        self.filterId = filter.m_filterId

        #Field ID
        self.ui.fieldCombo.setCurrentIndex(filter.m_fieldId - 1)

        # Verb
        self.ui.verbCombo.setCurrentIndex(filter.m_verb - 1)

        # Query string
        self.ui.queryStrEdit.setText(filter.m_queryStr)

        # Action
        self.ui.actionCombo.setCurrentIndex(filter.m_action - 1)

    def getFilter(self):
        filter = FeedItemFilter()

        # Filter ID
        filter.m_filterId = self.filterId

        # Field ID
        filter.m_fieldId = self.ui.fieldCombo.currentIndex() + 1

        # Verb
        filter.m_verb = self.ui.verbCombo.currentIndex() + 1

        # Query string
        filter.m_queryStr = self.ui.queryStrEdit.text()

        # Action
        filter.m_action = self.ui.actionCombo.currentIndex() + 1

        return filter
