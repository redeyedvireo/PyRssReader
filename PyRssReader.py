import os, sys, datetime, logging
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pathlib import Path
from database import Database
from feed_tree import FeedTree
from title_tree import TitleTree
from content_view import RssContentView


kDatabaseName = "Feeds.db"
kAppName      = "RssReader"         # Only needed for finding the database path

# ---------------------------------------------------------------
class PyRssReaderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PyRssReaderWindow, self).__init__()
        uic.loadUi('PyRssReaderWindow.ui', self)

        logging.basicConfig(filename="RsReader.log", level=logging.INFO)
        logging.info('Started')

        self.db = Database()

        self.feedTreeObj = FeedTree(self.feedTree)
        self.feedTreeObj.feedSelectedSignal.connect(self.onFeedSelected)

        self.titleTreeObj = TitleTree(self.titleTree)
        self.titleTreeObj.feedItemSelectedSignal.connect(self.onFeedItemSelected)

        self.rssContentViewObj = RssContentView(self.rssContentView)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        print("Initializing application...")

        dbDir = self.getDatabasePath()
        print("DB dir: {}".format(dbDir))
        self.db.open(dbDir)

        feedList = self.db.getFeeds()
        self.feedTreeObj.addFeeds(feedList)

    # TODO: This should be a static method (or class method?) of Database
    def getDatabasePath(self):
        return "{}\\{}".format(self.getDatabaseDirectory(), kDatabaseName)

    # TODO: This should be a static method (or class method?) of Database
    def getDatabaseDirectory(self):
        procEnv = QtCore.QProcessEnvironment.systemEnvironment()

        if procEnv.contains("APPDATA"):
            # Indicates Windows platform
            appDataPath = procEnv.value("APPDATA")

            databasePath = "{}\\{}".format(appDataPath, kAppName)

            #  Create directory if non - existent
            dbDir = Path(databasePath)

            if not dbDir.exists():
                # Directory doesn't exist - create it.
                if not dbDir.mkdir():
                    errMsg = "Could not create the data directory: {}".format(databasePath)
                    QtWidgets.QMessageBox.critical(self, kAppName, errMsg)
                    return ""

            return databasePath

    def onFeedSelected(self, feedId):
        print("onFeedSelected: {} was selected.".format(feedId))
        feed = self.db.getFeed(feedId)
        self.feedNameLabel.setText(feed.m_feedName)
        self.feedImageLabel.setPixmap(feed.m_feedFavicon)
        self.populateFeedItemView(feedId)

    def populateFeedItemView(self, feedId):
        feedItemList = self.db.getFeedItems(feedId)
        self.titleTreeObj.addFeedItems(feedItemList)

    def onFeedItemSelected(self, feedItemGuid, feedId):
        print("onFeedItemSelected: guid: {}, from feed: {}".format(feedItemGuid, feedId))
        feedItem = self.db.getFeedItem(feedItemGuid, feedId)
        self.rssContentViewObj.setContents(feedItem)

    def closeEvent(self, event):
        print("Closing database...")
        self.db.close()
        logging.info("Program exiting")

# ---------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = PyRssReaderWindow()
    wind.show()

    sys.exit(app.exec_())
