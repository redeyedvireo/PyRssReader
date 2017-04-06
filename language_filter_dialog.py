from PyQt5 import uic, QtCore, QtWidgets


class LanguageFilterDialog(QtWidgets.QDialog):
    def __init__(self, parent, db):
        super(LanguageFilterDialog, self).__init__(parent)
        uic.loadUi('language_filter_dialog.ui', self)
        self.db = db
        self.filteredWords = []
        self.newFilteredWords = []      # New filtered words, added through this dialog
        self.removedFilteredWords = []  # Filtered words removed from the original list

        self.buttonBox.accepted.connect(self.onAccepted)

        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.filteredWords = self.db.getFilteredWords()
        for word in self.filteredWords:
            self.listWidget.addItem(word)

    @QtCore.pyqtSlot()
    def onAccepted(self):
        self.db.deleteFilteredWords(self.removedFilteredWords)
        self.db.addFilteredWords(self.newFilteredWords)
        self.accept()


    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        newWord = self.addWordEdit.text()
        self.addWordEdit.clear()

        # Make sure it does not already exist, and has not already been added in this session
        if newWord not in self.filteredWords and newWord not in self.newFilteredWords:
            self.newFilteredWords.append(newWord)
            self.listWidget.addItem(newWord)

            # In case this word had been marked to be deleted, remove it from the deleted words list
            if newWord in self.removedFilteredWords:
                self.removedFilteredWords.remove(newWord)

    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        item = self.listWidget.currentItem()
        if item is not None:
            wordToDelete = item.text()
            self.listWidget.takeItem(self.listWidget.currentRow())

            if wordToDelete in self.newFilteredWords:
                # This is a new filtered word.  Just remove it from the new word list
                self.newFilteredWords.remove(wordToDelete)
            elif wordToDelete not in self.removedFilteredWords:
                self.removedFilteredWords.append(wordToDelete)

