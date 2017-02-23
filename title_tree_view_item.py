from PyQt5 import QtCore, QtWidgets, QtGui

kEnclosureColumn = 0
kTitleColumn = 1
kDateColumn = 2
kCreatorColumn = 3
kTagsColumn = 4

# This must be updated to indicate the number of columns
kNumColumns = 5

class TitleTreeViewItem(QtGui.QStandardItem):
    def __init__(self, itemText, bRead, feedId, guid):
        QtGui.QStandardItem.__init__(self)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsUserCheckable)

        self.m_feedId = feedId
        self.m_guid = guid
        self.setText(itemText)
        self.m_bRead = bRead

        self.setReadState(self.m_bRead)

    def setReadState(self, isRead):
        self.m_bRead = isRead

        itemFont = self.font()
        itemFont.setBold(not isRead)
        self.setFont(itemFont)

    def guid(self):
        return self.m_guid

    def feedId(self):
        return self.m_feedId
