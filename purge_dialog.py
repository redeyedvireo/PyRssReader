from PySide6 import QtWidgets
from ui_PurgeDlg import Ui_PurgeDlg

class PurgeDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(PurgeDialog, self).__init__(parent)

        self.ui = Ui_PurgeDlg()
        self.ui.setupUi(self)

    def getDays(self):
        return self.ui.daysSpin.value()

    def purgeUnreadItems(self):
        return True if self.ui.deleteReadAndUnreadButton.isChecked() else False
