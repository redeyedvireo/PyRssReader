from PyQt5 import uic, QtCore, QtWidgets
from feed_identifier import FeedIdentifier

class NewFeedDialog(QtWidgets.QDialog):
    def __init__(self, parent, proxy):
        super(NewFeedDialog, self).__init__(parent)
        uic.loadUi('NewFeedDlg.ui', self)
        self.proxy = proxy
        self.feedIdentifier = FeedIdentifier(self.proxy)
        self.feed = None

        self.nextButton.setEnabled(False)
        self.stackedWidget.setCurrentIndex(0)

    @QtCore.pyqtSlot('QString')
    def on_feedUrlEdit_textEdited(self, text):
        self.nextButton.setEnabled(len(text) > 0)

    @QtCore.pyqtSlot()
    def on_nextButton_clicked(self):
        if self.stackedWidget.currentIndex() == 0:
            feedUrl = self.feedUrlEdit.text()
            self.feed = self.feedIdentifier.identifyFeed(feedUrl)

            if not self.feed.isValid():
                QtWidgets.QMessageBox.critical(self, "RssReader", "Feed not valid")
                return

            self.stackedWidget.setCurrentIndex(1)
            self.nextButton.setText("Add Feed")
            self.feedUrlLabel.setText(feedUrl)
            self.feedNameLabel.setText(self.feed.m_feedTitle)
            self.descriptionLabel.setText(self.feed.m_feedDescription)
        else:
            # If we're on the second page of the stacked widget, then clicking this button is
            # equivalent to clicking OK, which accepts the feed.
            self.accept()

    def getFeed(self):
        return self.feed
