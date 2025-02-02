from PySide6 import QtCore, QtWidgets
from ui_FeedPropertiesDlg import Ui_FeedPropertiesDlg

class FeedPropertiesDialog(QtWidgets.QDialog):
    def __init__(self, parent, db, feedId):
        super(FeedPropertiesDialog, self).__init__(parent)

        self.ui = Ui_FeedPropertiesDlg()
        self.ui.setupUi(self)

        self.db = db
        self.feedId = feedId
        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.feed = self.db.getFeed(self.feedId)

        self.ui.titleLabel.setText(self.feed.m_feedTitle)
        self.ui.urlLabel.setText(self.feed.m_feedUrl)
        self.ui.dateAddedLabel.setText(str(self.feed.m_feedDateAdded))
        self.ui.lastUpdatedLabel.setText(str(self.feed.m_feedLastUpdated))
        self.ui.lastPurgedLabel.setText(str(self.feed.m_feedLastPurged))
        self.ui.feedIconLabel.setPixmap(self.feed.m_feedFavicon)
