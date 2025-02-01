from PySide6 import QtCore, QtWidgets
from feed_identifier import FeedIdentifier
from proxy import Proxy
from ui_NewFeedDlg import Ui_NewFeedDlg

class NewFeedDialog(QtWidgets.QDialog):
    def __init__(self, parent, proxy: Proxy):
        super(NewFeedDialog, self).__init__(parent)

        self.ui = Ui_NewFeedDlg()
        self.ui.setupUi(self)

        self.proxy = proxy
        self.feedIdentifier = FeedIdentifier(self.proxy)
        self.feed = None

        self.ui.nextButton.setEnabled(False)
        self.ui.stackedWidget.setCurrentIndex(0)

    @QtCore.Slot(str)
    def on_feedUrlEdit_textEdited(self, text):
        self.ui.nextButton.setEnabled(len(text) > 0)

    @QtCore.Slot()
    def on_nextButton_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            feedUrl = self.ui.feedUrlEdit.text()
            self.feed = self.feedIdentifier.identifyFeed(feedUrl)

            if self.feed is None or not self.feed.isValid():
                QtWidgets.QMessageBox.critical(self, "RssReader", "Feed not valid")
                return

            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.nextButton.setText("Add Feed")
            self.ui.feedUrlLabel.setText(feedUrl)
            self.ui.feedNameLabel.setText(self.feed.m_feedTitle)
            self.ui.descriptionLabel.setText(self.feed.m_feedDescription)
        else:
            # If we're on the second page of the stacked widget, then clicking this button is
            # equivalent to clicking OK, which accepts the feed.
            self.accept()

    def getFeed(self):
        return self.feed
