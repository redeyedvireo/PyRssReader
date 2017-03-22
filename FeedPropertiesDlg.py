from PyQt5 import uic, QtCore, QtWidgets


class FeedPropertiesDialog(QtWidgets.QDialog):
    def __init__(self, parent, db, feedId):
        super(FeedPropertiesDialog, self).__init__(parent)
        uic.loadUi('FeedPropertiesDlg.ui', self)
        self.db = db
        self.feedId = feedId
        QtCore.QTimer.singleShot(0, self.populateDialog)

    def populateDialog(self):
        self.feed = self.db.getFeed(self.feedId)
        
        self.titleLabel.setText(self.feed.m_feedTitle)
        self.urlLabel.setText(self.feed.m_feedUrl)
        self.dateAddedLabel.setText(str(self.feed.m_feedDateAdded))
        self.lastUpdatedLabel.setText(str(self.feed.m_feedLastUpdated))
        self.lastPurgedLabel.setText(str(self.feed.m_feedLastPurged))
        self.feedIconLabel.setPixmap(self.feed.m_feedFavicon)
