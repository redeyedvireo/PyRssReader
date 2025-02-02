from PySide6 import QtCore, QtWidgets
from ui_ad_filter_dialog import Ui_EditAdFilterDlg

class AdFilterDialog(QtWidgets.QDialog):
    def __init__(self, parent, db):
        super(AdFilterDialog, self).__init__(parent)

        self.ui = Ui_EditAdFilterDlg()
        self.ui.setupUi(self)

        self.db = db
        self.adWords = []
        self.newAdWords = []
        self.removedAdWords = []

        self.ui.buttonBox.accepted.connect(self.onAccepted)

        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.adWords = self.db.getAdFilters()
        for word in self.adWords:
            self.ui.listWidget.addItem(word)

    @QtCore.Slot()
    def onAccepted(self):
        self.db.deleteAdFilters(self.removedAdWords)
        self.db.addAdFilters(self.newAdWords)
        self.accept()

    @QtCore.Slot()
    def on_addButton_clicked(self):
        newWord = self.ui.addWordEdit.text()
        self.ui.addWordEdit.clear()

        # Make sure it does not already exist, and has not already been added in this session
        if newWord not in self.adWords and newWord not in self.newAdWords:
            self.newAdWords.append(newWord)
            self.ui.listWidget.addItem(newWord)

            # In case this word had been marked to be deleted, remove it from the deleted words list
            if newWord in self.removedAdWords:
                self.removedAdWords.remove(newWord)

    @QtCore.Slot()
    def on_deleteButton_clicked(self):
        item = self.ui.listWidget.currentItem()

        if item is not None:
            wordToDelete = item.text()
            self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())

            if wordToDelete in self.newAdWords:
                # This is a new filtered word.  Just remove it from the new word list
                self.newAdWords.remove(wordToDelete)
            elif wordToDelete not in self.removedAdWords:
                self.removedAdWords.append(wordToDelete)

