from PyQt5 import QtGui, QtCore
from title_tree_view_item import TitleTreeViewItem
from utility import getResourceFileIcon

kEnclosureIconName = "Audio Enclosure.png"


class TitleTreeEnclosureItem(TitleTreeViewItem):
    def __init__(self, enclosureUrl, bRead, feedId, guid):
        """ hasEnclosure is a boolean indicating whether this feed has an enclosure. """
        TitleTreeViewItem.__init__(self, "", bRead, feedId, guid)

        self.enclosureUrl = enclosureUrl
        self.enclosureIcon = getResourceFileIcon(kEnclosureIconName)
        self.updateEnclosureVisibility()
        self.setTextAlignment(QtCore.Qt.AlignLeft)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsUserCheckable)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsEditable)

    def setEnclosureUrl(self, enclosureUrl):
        self.enclosureUrl = enclosureUrl

    def getEnclosureUrl(self):
        return self.enclosureUrl

    def updateEnclosureVisibility(self):
        if len(self.enclosureUrl) > 0:
            self.setIcon(self.enclosureIcon)
        else:
            self.setIcon(QtGui.QIcon())
