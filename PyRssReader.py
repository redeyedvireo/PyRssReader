import os, sys, datetime, logging
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pathlib import Path
from database import Database
from language_filter import LanguageFilter
from ad_filter import AdFilter
from feed_tree import FeedTree
from title_tree import TitleTree
from content_view import RssContentView
from resource_fetcher import ResourceFetcher
from feed_item_parser import parseFeed


kDatabaseName = "Feeds.db"
kAppName      = "RssReader"         # Only needed for finding the database path
kAppNameForSettings = "PyRssReader" # Used for saving settings

# Settings groups
kWindowSettingsGroup = "window"
kSize = "size"
kPos = "pos"
kHorizSplitterSizes = "horizsplitterSizes"
kVertSplitterSizes = "vertsplitterSizes"
kTitleTreeSettingsGroup = "titletree"
kColumnWidths = "columnwidths"
kFeedSettingsGroup = "feed"
kLastViewedFeedId = "lastviewedfeedid"


# ---------------------------------------------------------------
class PyRssReaderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PyRssReaderWindow, self).__init__()
        uic.loadUi('PyRssReaderWindow.ui', self)

        logging.basicConfig(filename="RsReader.log", level=logging.INFO)
        logging.info('Application Started')

        self.db = Database()
        self.languageFilter = LanguageFilter(self.db)
        self.adFilter = AdFilter(self.db)

        self.m_currentFeedId = -1

        self.feedTreeObj = FeedTree(self.feedTree)
        self.feedTreeObj.feedSelectedSignal.connect(self.onFeedSelected)

        self.titleTreeObj = TitleTree(self.titleTree, self.languageFilter)
        self.titleTreeObj.feedItemSelectedSignal.connect(self.onFeedItemSelected)

        self.rssContentViewObj = RssContentView(self.rssContentView, self.languageFilter, self.adFilter)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        print("Initializing application...")
        self.loadSettings()

        dbDir = self.getDatabasePath()
        print("DB dir: {}".format(dbDir))
        self.db.open(dbDir)

        self.languageFilter.initialize()
        self.adFilter.initialize()

        feedList = self.db.getFeeds()
        self.feedTreeObj.addFeeds(feedList)

        if self.m_currentFeedId >= 0:
            self.onFeedSelected(self.m_currentFeedId)

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

    def loadSettings(self):
        """ Loads application settings. """
        settingsObj = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, kAppName, kAppNameForSettings)

        # Window size and position
        settingsObj.beginGroup(kWindowSettingsGroup)
        if settingsObj.contains(kSize):
            self.resize(settingsObj.value(kSize))

        if settingsObj.contains(kPos):
            self.move(settingsObj.value(kPos))

        if settingsObj.contains(kHorizSplitterSizes):
            self.horizSplitter.restoreState(settingsObj.value(kHorizSplitterSizes))

        if settingsObj.contains(kVertSplitterSizes):
            self.vertSplitter.restoreState(settingsObj.value(kVertSplitterSizes))

        settingsObj.endGroup()

        # Title tree data
        settingsObj.beginGroup(kTitleTreeSettingsGroup)
        if settingsObj.contains(kColumnWidths):
            columnList = settingsObj.value(kColumnWidths)
            self.titleTreeObj.SetColumnWidths(columnList)
        settingsObj.endGroup()

        # Last-viewed feed
        settingsObj.beginGroup(kFeedSettingsGroup)
        self.m_currentFeedId = int(settingsObj.value(kLastViewedFeedId, 0))
        settingsObj.endGroup()

    def saveSettings(self):
        """ Saves application settings. """
        settingsObj = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, kAppName, kAppNameForSettings)

        # Window size and position
        settingsObj.beginGroup(kWindowSettingsGroup)
        settingsObj.setValue(kSize, self.size())
        settingsObj.setValue(kPos, self.pos())
        settingsObj.setValue(kHorizSplitterSizes, self.horizSplitter.saveState())
        settingsObj.setValue(kVertSplitterSizes, self.vertSplitter.saveState())
        settingsObj.endGroup()

        # Title tree data
        settingsObj.beginGroup(kTitleTreeSettingsGroup)
        columnList = self.titleTreeObj.GetColumnWidths()
        settingsObj.setValue(kColumnWidths, columnList)
        settingsObj.endGroup()

        #  Last-viewed feed
        settingsObj.beginGroup(kFeedSettingsGroup)
        settingsObj.setValue(kLastViewedFeedId, self.m_currentFeedId)
        settingsObj.endGroup()

    def onFeedSelected(self, feedId):
        print("onFeedSelected: {} was selected.".format(feedId))
        self.m_currentFeedId = feedId
        feed = self.db.getFeed(feedId)
        self.feedNameLabel.setText(feed.m_feedName)
        self.feedImageLabel.setPixmap(feed.m_feedFavicon)
        self.populateFeedItemView(feedId)

    def populateFeedItemView(self, feedId):
        feedItemList = self.db.getFeedItems(feedId)
        self.titleTreeObj.addFeedItems(feedItemList)

    def onFeedItemSelected(self, feedItemGuid):
        print("onFeedItemSelected: guid: {}, from feed: {}".format(feedItemGuid, self.m_currentFeedId))
        feedItem = self.db.getFeedItem(feedItemGuid, self.m_currentFeedId)
        self.rssContentViewObj.setContents(feedItem)

    @QtCore.pyqtSlot()
    def on_actionUpdate_Feeds_triggered(self):
        feeds = self.db.getFeeds()

        # For now, just get one feed
        feedUrl = feeds[0].m_feedUrl
        resourceFetcher = ResourceFetcher(feedUrl)
        feedText = resourceFetcher.getData()
        feedItemList = parseFeed(feedText)

        for feedItem in feedItemList:
            print("Title: {}".format(feedItem.m_title))
            print("Author: {}".format(feedItem.m_author))
            print("Link: {}".format(feedItem.m_link))
            print("Publication date: {}".format(feedItem.m_publicationDatetime))
            print("GUID: {}".format(feedItem.m_guid))
            print("Categories: {}".format(feedItem.m_categories))
            print("Publication date/time: {}".format(feedItem.m_publicationDatetime))
            print("Thumbnail: {}".format(feedItem.m_thumbnailLink))
            print("Enclosure: {}".format(feedItem.m_enclosureLink))
            print()

    def closeEvent(self, event):
        print("Closing database...")
        self.db.close()
        self.saveSettings()
        logging.info("Program exiting")

# ---------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = PyRssReaderWindow()
    wind.show()

    sys.exit(app.exec_())
