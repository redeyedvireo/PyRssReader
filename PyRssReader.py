import os, sys, datetime, logging
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pathlib import Path
from database import Database
from language_filter import LanguageFilter
from ad_filter import AdFilter
from image_cache import ImageCache
from image_prefetcher import ImagePrefetcher
from feed_item_filter_matcher import FeedItemFilterMatcher
from feed_tree import FeedTree
from title_tree import TitleTree, kDateColumn
from content_view import RssContentView
from feed_updater import FeedUpdater
from preferences_dialog import PrefsDialog
from purge_dialog import PurgeDialog
from feed_purger import FeedPurger
from keyboard_handler import KeyboardHandler
from proxy import Proxy
from utility import getResourceFilePixmap

from feed import kItemsOfInterestFeedId


kDatabaseName = "Feeds.db"
kAppName      = "RssReader"         # Only needed for finding the database path
kAppNameForSettings = "PyRssReader" # Used for saving settings

kStarIcon = "star.png"

# Settings groups
kWindowSettingsGroup = "window"
kSize = "size"
kPos = "pos"
kProxySettingsGroup = "proxy"
kHorizSplitterSizes = "horizsplitterSizes"
kVertSplitterSizes = "vertsplitterSizes"
kTitleTreeSettingsGroup = "titletree"
kColumnWidths = "columnwidths"
kSortColumn = "sortcolumn"
kColumnSortOrder = "columnsortorder"
kFeedSettingsGroup = "feed"
kLastViewedFeedId = "lastviewedfeedid"
kProxyHostname = "proxyhostname"
kProxyPort = "proxyport"
kProxyUserId = "proxyuserid"

# Image cache size (number of cache entries)
kMaxCacheSize = 100


# ---------------------------------------------------------------
class PyRssReaderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PyRssReaderWindow, self).__init__()
        uic.loadUi('PyRssReaderWindow.ui', self)

        logging.basicConfig(filename="RssReader.log", level=logging.INFO)

        self.db = Database()
        self.proxy = Proxy()

        self.languageFilter = LanguageFilter(self.db)
        self.adFilter = AdFilter(self.db)
        self.imageCache = ImageCache(kMaxCacheSize)
        self.imagePrefetcher = ImagePrefetcher(self.db, self.imageCache, self.proxy)

        self.feedItemFilterMatcher = FeedItemFilterMatcher(self.db)
        self.feedPurger = FeedPurger(self.db, self)
        self.feedPurger.feedPurgedSignal.connect(self.onFeedPurged)
        self.feedPurger.messageSignal.connect(self.showStatusBarMessage)

        self.m_currentFeedId = -1
        self.feedIdsToUpdate = []

        # This is a persistent object, so it won't go out of scope while fetching feeds
        self.feedUpdater = FeedUpdater(self.db)
        self.feedUpdater.feedItemUpdateSignal.connect(self.onFeedItemUpdate)
        self.feedUpdater.feedUpdateMessageSignal.connect(self.showStatusBarMessage)

        self.keyboardHandler = KeyboardHandler(self)

        self.feedTreeObj = FeedTree(self.feedTree, self.db, self.keyboardHandler)
        self.feedTreeObj.feedSelectedSignal.connect(self.onFeedSelected)
        self.feedTreeObj.feedUpdateRequestedSignal.connect(self.onFeedUpdateRequested)

        self.titleTreeObj = TitleTree(self.titleTree, self.languageFilter, self.keyboardHandler, self.imagePrefetcher)
        self.titleTreeObj.feedItemSelectedSignal.connect(self.onFeedItemSelected)

        self.rssContentViewObj = RssContentView(self.rssContentView, self.languageFilter, self.adFilter, self.imageCache,
                                                self.keyboardHandler, self.proxy)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        print("Initializing application...")
        self.loadSettings()

        dbDir = self.getDatabasePath()
        print("DB dir: {}".format(dbDir))
        self.db.open(dbDir)

        self.languageFilter.initialize()
        self.adFilter.initialize()
        self.feedItemFilterMatcher.initialize()

        feedList = self.db.getFeeds()
        feedIdStr = self.db.getGlobalValue("feed-order")
        feedOrderListOfStrings = feedIdStr.split(",")
        feedOrderList = [int(idStr) for idStr in feedOrderListOfStrings]
        self.feedTreeObj.addFeeds(feedList, feedOrderList)

        if self.proxy.usesProxy():
            password = QtWidgets.QInputDialog.getText(self, "Password", "Enter Proxy Password for user {}".format(self.proxy.proxyUser),
                                                      QtWidgets.QLineEdit.Password)
            if password[1]:
                self.proxy.proxyPassword = password[0]

        if self.m_currentFeedId >= 0:
            self.onFeedSelected(self.m_currentFeedId)
            self.feedTreeObj.setCurrentFeed(self.m_currentFeedId)

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
        self.m_currentFeedId = int(settingsObj.value(kLastViewedFeedId, -1))
        settingsObj.endGroup()

        # HTML Proxy
        settingsObj.beginGroup(kProxySettingsGroup)
        self.proxy.proxyUrl = settingsObj.value(kProxyHostname, "")
        self.proxy.proxyPort = int(settingsObj.value(kProxyPort, 0))
        self.proxy.proxyUser = settingsObj.value(kProxyUserId, "")
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

        # HTML Proxy
        settingsObj.beginGroup(kProxySettingsGroup)
        settingsObj.setValue(kProxyHostname, self.proxy.proxyUrl)
        settingsObj.setValue(kProxyPort, self.proxy.proxyPort)
        settingsObj.setValue(kProxyUserId, self.proxy.proxyUser)
        settingsObj.endGroup()

    def onFeedSelected(self, feedId):
        print("onFeedSelected: {} was selected.".format(feedId))
        self.m_currentFeedId = feedId
        if self.m_currentFeedId != kItemsOfInterestFeedId:
            feed = self.db.getFeed(feedId)
            self.feedNameLabel.setText(feed.m_feedName)
            self.feedImageLabel.setPixmap(feed.m_feedFavicon)
            self.populateFeedItemView(feedId)
        else:
            self.feedNameLabel.setText("Items of Interest")
            starPixmap = getResourceFilePixmap(kStarIcon)
            self.feedImageLabel.setPixmap(starPixmap)
            ioiList = self.db.getItemsOfInterest()

            # Read the actual feed items
            feedItemList = []
            for ioiTuple in ioiList:
                feedItem = self.db.getFeedItem(ioiTuple[1], ioiTuple[0])
                feedItemList.append(feedItem)

            self.titleTreeObj.addFeedItems(feedItemList, False)

    def populateFeedItemView(self, feedId, sameFeed=False):
        feedItemList = self.db.getFeedItems(feedId)
        self.titleTreeObj.addFeedItems(feedItemList, sameFeed)

    def onFeedItemSelected(self, feedId, feedItemGuid):
        print("onFeedItemSelected: guid: {}, from feed: {}".format(feedItemGuid, feedId))
        feedItem = self.db.getFeedItem(feedItemGuid, feedId)
        self.db.setFeedItemReadFlag(feedId, feedItemGuid, True)
        self.feedTreeObj.updateFeedCount(feedId)
        self.rssContentViewObj.setContents(feedItem)

    def onFeedUpdateRequested(self, feedId):
        print("onFeedUpdateRequested for feed: {}".format(feedId))
        if feedId > 0:
            self.feedUpdater.updateFeed(feedId, self.proxy)
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
            self.feedUpdater.updateFeed(feedIdToUpdate, self.proxy)
        else:
            self.showStatusBarMessage("Updating complete.")


    @QtCore.pyqtSlot(int, list)
    def onFeedItemUpdate(self, feedId, feedItemList):
        self.db.addFeedItems(feedItemList, feedId)
        self.feedItemFilterMatcher.filterFeedItems(feedId, feedItemList)

        if feedId == self.m_currentFeedId:
            # Update title tree with new set of feed items
            self.populateFeedItemView(feedId, True)

        QtCore.QTimer.singleShot(0, self.updateNextFeed)

    @QtCore.pyqtSlot()
    def on_actionPreferences_triggered(self):
        prefsDialog = PrefsDialog(self, self.proxy)
        if prefsDialog.exec() == QtWidgets.QDialog.Accepted:
            self.proxy = prefsDialog.getProxySettings()
            self.rssContentViewObj.setProxy(self.proxy)


    @QtCore.pyqtSlot()
    def on_actionPurge_Old_News_triggered(self):
        purgeDlg = PurgeDialog(self)
        if purgeDlg.exec() == QtWidgets.QDialog.Accepted:
            priorDays = purgeDlg.getDays()
            purgeUnreadItems = purgeDlg.purgeUnreadItems()

            self.feedPurger.purgeAllFeeds(priorDays, purgeUnreadItems)
            self.onFeedSelected(self.m_currentFeedId)   # Force repopulation of title tree


    @QtCore.pyqtSlot(int)
    def onFeedPurged(self, feedId):
        self.feedTreeObj.updateFeedCount(feedId)

        if feedId == self.m_currentFeedId:
            # Update title tree with new set of feed items
            self.populateFeedItemView(feedId, True)

    @QtCore.pyqtSlot(str, int)
    def showStatusBarMessage(self, message, timeout=10000):
        """ Displays a message on the status bar. """
        self.statusBar.showMessage(message, timeout)


    def closeEvent(self, event):
        print("Closing database...")
        self.db.close()
        self.saveSettings()

# ---------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = PyRssReaderWindow()
    wind.show()

    sys.exit(app.exec_())
