from PySide6 import QtCore, QtWidgets
from ui_language_filter_dialog import Ui_LanguageFilterDlg


class LanguageFilterDialog(QtWidgets.QDialog):
    def __init__(self, parent, db):
        super(LanguageFilterDialog, self).__init__(parent)

        self.ui = Ui_LanguageFilterDlg()
        self.ui.setupUi(self)

        self.db = db
        self.filteredWords = []
        self.newFilteredWords = []      # New filtered words, added through this dialog
        self.removedFilteredWords = []  # Filtered words removed from the original list

        self.ui.buttonBox.accepted.connect(self.onAccepted)

        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.filteredWords = self.db.getFilteredWords()
        for word in self.filteredWords:
            self.ui.listWidget.addItem(word)

    @QtCore.Slot()
    def onAccepted(self):
        self.db.deleteFilteredWords(self.removedFilteredWords)
        self.db.addFilteredWords(self.newFilteredWords)
        self.accept()


    @QtCore.Slot()
    def on_addButton_clicked(self):
        newWord = self.ui.addWordEdit.text()
        self.ui.addWordEdit.clear()

        # Make sure it does not already exist, and has not already been added in this session
        if newWord not in self.filteredWords and newWord not in self.newFilteredWords:
            self.newFilteredWords.append(newWord)
            self.ui.listWidget.addItem(newWord)

            # In case this word had been marked to be deleted, remove it from the deleted words list
            if newWord in self.removedFilteredWords:
                self.removedFilteredWords.remove(newWord)

    @QtCore.Slot()
    def on_deleteButton_clicked(self):
        item = self.ui.listWidget.currentItem()
        if item is not None:
            wordToDelete = item.text()
            self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())

            if wordToDelete in self.newFilteredWords:
                # This is a new filtered word.  Just remove it from the new word list
                self.newFilteredWords.remove(wordToDelete)
            elif wordToDelete not in self.removedFilteredWords:
                self.removedFilteredWords.append(wordToDelete)

