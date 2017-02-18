import os, sys, datetime, logging
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pathlib import Path
from database import Database
from language_filter import LanguageFilter
from ad_filter import AdFilter
from feed_tree import FeedTree
from title_tree import TitleTree, kDateColumn
from content_view import RssContentView
from resource_fetcher import ResourceFetcher
from feed_item_parser import parseFeed
from feed_updater import FeedUpdater


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
kSortColumn = "sortcolumn"
kColumnSortOrder = "columnsortorder"
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
        self.feedIdsToUpdate = []

        # This is a persistent object, so it won't go out of scope while fetching feeds
        self.feedUpdater = FeedUpdater(self.db)
        self.feedUpdater.feedItemUpdateSignal.connect(self.onFeedItemUpdate)
        self.feedUpdater.feedUpdateMessageSignal.connect(self.showStatusBarMessage)

        self.feedTreeObj = FeedTree(self.feedTree)
        self.feedTreeObj.feedSelectedSignal.connect(self.onFeedSelected)
        self.feedTreeObj.feedUpdateRequestedSignal.connect(self.onFeedUpdateRequested)

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
        sortColumn = int(settingsObj.value(kSortColumn, kDateColumn))
        self.titleTreeObj.setSortColumn(sortColumn)
        sortOrder = int(settingsObj.value(kColumnSortOrder, QtCore.Qt.DescendingOrder))
        self.titleTreeObj.setSortOrder(sortOrder)
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
        settingsObj.setValue(kSortColumn, self.titleTreeObj.getSortColumn())
        settingsObj.setValue(kColumnSortOrder, self.titleTreeObj.getSortOrder())
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

    def onFeedUpdateRequested(self, feedId):
        print("onFeedUpdateRequested for feed: {}".format(feedId))
        if feedId > 0:
            self.feedUpdater.updateFeed(feedId)
        else:
            logging.error("onFeedUpdateRequested: Invalid feedId: {}".format(feedId))

    @QtCore.pyqtSlot()
    def on_actionUpdate_Feeds_triggered(self):
        self.feedIdsToUpdate = self.db.getFeedIds()

        self.updateNextFeed()

    def updateNextFeed(self):
        """ Starts the update process for the next feed in the list.  This is the feed that is
            at the head of self.feedIdsToUpdate. """
        if self.feedIdsToUpdate:
            feedIdToUpdate = self.feedIdsToUpdate.pop(0)
            self.feedUpdater.updateFeed(feedIdToUpdate)
        else:
            self.showStatusBarMessage("Updating complete.")


    @QtCore.pyqtSlot(int, list)
    def onFeedItemUpdate(self, feedId, feedItemList):
        self.db.addFeedItems(feedItemList, feedId)

        if feedId == self.m_currentFeedId:
            # Update title tree with new set of feed items
            self.populateFeedItemView(feedId)

        QtCore.QTimer.singleShot(0, self.updateNextFeed)

    @QtCore.pyqtSlot(str, int)
    def showStatusBarMessage(self, message, timeout=10000):
        """ Displays a message on the status bar. """
        self.statusBar.showMessage(message, timeout)


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
