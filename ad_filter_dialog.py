from PyQt5 import uic, QtCore, QtWidgets

class AdFilterDialog(QtWidgets.QDialog):
    def __init__(self, parent, db):
        super(AdFilterDialog, self).__init__(parent)
        uic.loadUi('ad_filter_dialog.ui', self)
        self.db = db
        self.adWords = []
        self.newAdWords = []
        self.removedAdWords = []

        self.buttonBox.accepted.connect(self.onAccepted)

        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.adWords = self.db.getAdFilters()
        for word in self.adWords:
            self.listWidget.addItem(word)

    @QtCore.pyqtSlot()
    def onAccepted(self):
        self.db.deleteAdFilters(self.removedAdWords)
        self.db.addAdFilters(self.newAdWords)
        self.accept()

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        newWord = self.addWordEdit.text()
        self.addWordEdit.clear()

        # Make sure it does not already exist, and has not already been added in this session
        if newWord not in self.adWords and newWord not in self.newAdWords:
            self.newAdWords.append(newWord)
            self.listWidget.addItem(newWord)

            # In case this word had been marked to be deleted, remove it from the deleted words list
            if newWord in self.removedAdWords:
                self.removedAdWords.remove(newWord)

    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        item = self.listWidget.currentItem()

        if item is not None:
            wordToDelete = item.text()
            self.listWidget.takeItem(self.listWidget.currentRow())

            if wordToDelete in self.newAdWords:
                # This is a new filtered word.  Just remove it from the new word list
                self.newAdWords.remove(wordToDelete)
            elif wordToDelete not in self.removedAdWords:
                self.removedAdWords.append(wordToDelete)

