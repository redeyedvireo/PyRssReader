from PyQt5 import QtCore, QtWidgets, QtGui
from title_tree_view_item import TitleTreeViewItem

class TitleTreeDateItem(TitleTreeViewItem):
    def __init__(self, date, bRead, feedId, guid):
        dateText = "{}".format(date.strftime("%Y-%m-%d %H:%M:%S"))
        TitleTreeViewItem.__init__(self, dateText, bRead, feedId, guid)
