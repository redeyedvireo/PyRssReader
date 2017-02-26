from PyQt5 import uic, QtWidgets

class PurgeDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(PurgeDialog, self).__init__(parent)
        uic.loadUi('PurgeDlg.ui', self)

    def getDays(self):
        return self.daysSpin.value()

    def purgeUnreadItems(self):
        return True if self.deleteReadAndUnreadButton.isChecked() else False
