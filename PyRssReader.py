import sys
import os.path
import logging
from logging.handlers import RotatingFileHandler
from PySide6 import QtCore, QtGui, QtWidgets
from pathlib import Path
from content_view_new import RssContentViewNew
from database import Database
from language_filter import LanguageFilter
from ad_filter import AdFilter
from prefetch_statusbar_widget import PrefetchStatusbarWidget
from image_cache import ImageCache
from image_prefetcher import ImagePrefetcher
from feed_item_filter_matcher import FeedItemFilterMatcher
from feed_tree import FeedTree
from title_tree import TitleTree, kDateColumn
from content_view import RssContentView
from feed_updater import FeedUpdater
from preferences_dialog import PrefsDialog
from NewFeed import NewFeedDialog
from purge_dialog import PurgeDialog
from feed_purger import FeedPurger
from keyboard_handler import KeyboardHandler
from proxy import Proxy
from ui_PyRssReaderWindow import Ui_RssReaderWindow
from utility import getDatabasePath, getDefaultEnclosureDirectory, getResourceFilePixmap, getLogfilePath, getScriptPath, textToDialog, runningFromBundle
from preferences import Preferences
from filter_manager_dialog import FilterManagerDialog
from language_filter_dialog import LanguageFilterDialog
from ad_filter_dialog import AdFilterDialog
from opml_exporter import OpmlExporter
from opml_importer import OpmlImporter
from enclosure_downloader import EnclosureDownloader
from pocket_support import PocketSupport

from feed import kItemsOfInterestFeedId


kDatabaseName = "Feeds.db"
kAppName      = "RssReader"         # Only needed for finding the database path
kAppNameForSettings = "PyRssReader" # Used for saving settings
kLogFile = 'PyRssReader.log'

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
kProxyPassword = "proxypassword"
kGeneralPreferencesGroup = "preferences"
kFeedUpdateInterval = "feedupdateinterval"
kUpdateOnAppStart = "updateonappstart"
kEnclosureDirectory = "enclosuredirectory"

# Image cache size (number of cache entries)
kMaxCacheSize = 100

# For status bar messages (don't clear the message)
kDontClearMessage = 0

kMaxLogileSize = 1024 * 1024

# ---------------------------------------------------------------
class PyRssReaderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PyRssReaderWindow, self).__init__()

        self.ui = Ui_RssReaderWindow()
        self.ui.setupUi(self)

        self.db = Database()
        self.proxy = Proxy()
        self.preferences = Preferences()

        self.languageFilter = LanguageFilter(self.db)
        self.adFilter = AdFilter(self.db)
        self.prefetchStatusbarWidget = PrefetchStatusbarWidget(self)
        self.imageCache = ImageCache(kMaxCacheSize)
        self.imagePrefetcher = ImagePrefetcher(self.db, self.imageCache, self.proxy)

        self.imagePrefetcher.imagePrefetchStartingSignal.connect(self.prefetchStatusbarWidget.prefetchOn)
        self.imagePrefetcher.imagePrefetchDoneSignal.connect(self.prefetchStatusbarWidget.prefetchOff)
        self.ui.statusBar.addPermanentWidget(self.prefetchStatusbarWidget)

        self.feedItemFilterMatcher = FeedItemFilterMatcher(self.db)
        self.feedPurger = FeedPurger(self.db, self)
        self.feedPurger.feedPurgedSignal.connect(self.onFeedPurged)
        self.feedPurger.messageSignal.connect(self.showStatusBarMessage)

        self.m_currentFeedId = -1
        self.feedIdsToUpdate = []

        # This is a persistent object, so it won't go out of scope while fetching feeds
        # self.feedUpdater = FeedUpdater(self.db)
        # self.feedUpdater.feedItemUpdateSignal.connect(self.onFeedItemUpdate)
        # self.feedUpdater.feedUpdateMessageSignal.connect(self.showStatusBarMessage)

        self.keyboardHandler = KeyboardHandler(self)

        self.keyboardHandler.minimizeApplicationSignal.connect(self.onMinimizeApp)

        self.feedTreeObj = FeedTree(self.ui.feedTree, self.db, self.keyboardHandler)
        self.feedTreeObj.feedSelectedSignal.connect(self.onFeedSelected)
        self.feedTreeObj.feedUpdateRequestedSignal.connect(self.onFeedUpdateRequested)
        self.feedTreeObj.feedReadStateSignal.connect(self.onSetFeedReadState)
        self.feedTreeObj.feedPurgeSignal.connect(self.onPurgeSingleFeed)
        self.feedTreeObj.feedDeleteSignal.connect(self.onDeleteFeed)

        self.titleTreeObj = TitleTree(self.db, self.ui.titleTree, self.languageFilter, self.keyboardHandler, self.imagePrefetcher)
        self.titleTreeObj.feedItemSelectedSignal.connect(self.onFeedItemSelected)
        self.titleTreeObj.downloadEnclosureSignal.connect(self.onDownloadEnclosure)

        # self.rssContentViewObj = RssContentView(self, self.languageFilter, self.adFilter, self.imageCache,
        #                                         self.keyboardHandler, self.proxy)

        self.rssContentViewObj = RssContentViewNew(self, self.languageFilter, self.adFilter, self.imageCache,
                                                self.keyboardHandler, self.proxy)

        self.addRssContentViewToLayout()
        self.rssContentViewObj.reselectFeedItemSignal.connect(self.onReselectFeedItem)
        self.rssContentViewObj.urlHovered.connect(self.showStatusBarMessage)

        self.feedUpdateTimer = QtCore.QTimer()
        self.feedUpdateTimer.timeout.connect(self.onFeedUpdateTimerTimeout)
        self.feedUpdateTimer.setInterval(60000)     # One-minute interval
        self.minutesSinceLastFeedUpdate = 0         # Minutes since last update of feeds

        self.enclosureDownloader = None

        self.pocketSupport = PocketSupport(self.db, self.proxy)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        self.loadSettings()

        dbDir = getDatabasePath(kAppName, kDatabaseName)
        logging.info("Database: {}".format(dbDir))
        self.db.open(dbDir)

        self.languageFilter.initialize()
        self.adFilter.initialize()
        self.feedItemFilterMatcher.initialize()

        feedList = self.db.getFeeds()
        feedOrderList = self.db.getFeedOrder()
        self.feedTreeObj.addFeeds(feedList, feedOrderList)

        # If proxy not saved in prefs, prompt user for it
        if self.proxy.usesProxy() and len(self.proxy.proxyPassword) == 0:
            password = QtWidgets.QInputDialog.getText(self, "Password", "Enter Proxy Password for user {}".format(self.proxy.proxyUser),
                                                      QtWidgets.QLineEdit.EchoMode.Password)
            if password[1]:
                self.proxy.proxyPassword = password[0]

        if self.m_currentFeedId >= 0:
            self.onFeedSelected(self.m_currentFeedId)
            self.feedTreeObj.setCurrentFeed(self.m_currentFeedId)

        self.pocketSupport.initialize()

        self.resetFeedUpdateMinuteCount()
        self.startFeedUpdateTimer()

        if self.preferences.updateOnAppStart:
            self.on_actionUpdate_Feeds_triggered()

    def loadSettings(self):
        """ Loads application settings. """
        settingsObj = QtCore.QSettings(QtCore.QSettings.Format.IniFormat, QtCore.QSettings.Scope.UserScope, kAppName, kAppNameForSettings)

        logging.info(f'Preferences path: {settingsObj.fileName()}')

        # Window size and position
        settingsObj.beginGroup(kWindowSettingsGroup)
        if settingsObj.contains(kSize):
            self.resize(settingsObj.value(kSize))

        if settingsObj.contains(kPos):
            self.move(settingsObj.value(kPos))

        if settingsObj.contains(kHorizSplitterSizes):
            self.ui.horizSplitter.restoreState(settingsObj.value(kHorizSplitterSizes))

        if settingsObj.contains(kVertSplitterSizes):
            self.ui.vertSplitter.restoreState(settingsObj.value(kVertSplitterSizes))

        settingsObj.endGroup()

        # Title tree data
        settingsObj.beginGroup(kTitleTreeSettingsGroup)
        if settingsObj.contains(kColumnWidths):
            columnList = settingsObj.value(kColumnWidths)
            self.titleTreeObj.SetColumnWidths(columnList)
        sortColumn = settingsObj.value(kSortColumn, kDateColumn, type=int)
        self.titleTreeObj.setSortColumn(sortColumn)
        sortOrder = settingsObj.value(kColumnSortOrder, QtCore.Qt.SortOrder.DescendingOrder)
        self.titleTreeObj.setSortOrder(sortOrder)
        settingsObj.endGroup()

        # Last-viewed feed
        settingsObj.beginGroup(kFeedSettingsGroup)
        self.m_currentFeedId = int(settingsObj.value(kLastViewedFeedId, -1, type=int))
        settingsObj.endGroup()

        # HTML Proxy
        settingsObj.beginGroup(kProxySettingsGroup)
        self.proxy.proxyUrl = settingsObj.value(kProxyHostname, "", type=str)
        self.proxy.proxyPort = settingsObj.value(kProxyPort, 0, type=int)
        self.proxy.proxyUser = settingsObj.value(kProxyUserId, "")
        self.proxy.proxyPassword = settingsObj.value(kProxyPassword, "", type=str)
        settingsObj.endGroup()

        # General Preferences
        settingsObj.beginGroup(kGeneralPreferencesGroup)
        self.preferences.feedUpdateInterval = settingsObj.value(kFeedUpdateInterval, 30, type=int)
        self.preferences.updateOnAppStart = settingsObj.value(kUpdateOnAppStart, False, type=bool)
        self.preferences.enclosureDirectory = settingsObj.value(kEnclosureDirectory, getDefaultEnclosureDirectory(), type=str)
        settingsObj.endGroup()

    def saveSettings(self):
        """ Saves application settings. """
        settingsObj = QtCore.QSettings(QtCore.QSettings.Format.IniFormat, QtCore.QSettings.Scope.UserScope, kAppName, kAppNameForSettings)

        # Window size and position
        settingsObj.beginGroup(kWindowSettingsGroup)
        settingsObj.setValue(kSize, self.size())
        settingsObj.setValue(kPos, self.pos())
        settingsObj.setValue(kHorizSplitterSizes, self.ui.horizSplitter.saveState())
        settingsObj.setValue(kVertSplitterSizes, self.ui.vertSplitter.saveState())
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
        settingsObj.setValue(kProxyPassword, self.proxy.proxyPassword)
        settingsObj.endGroup()

        # General Preferences
        settingsObj.beginGroup(kGeneralPreferencesGroup)
        settingsObj.setValue(kFeedUpdateInterval, self.preferences.feedUpdateInterval)
        settingsObj.setValue(kUpdateOnAppStart, self.preferences.updateOnAppStart)
        settingsObj.setValue(kEnclosureDirectory, self.preferences.enclosureDirectory)
        settingsObj.endGroup()

    def addRssContentViewToLayout(self):
        self.ui.vertSplitter.addWidget(self.rssContentViewObj)

    def createFeedUpdater(self):
        """ Create the feed updater object.  This needs to be defined at class scope so that
            it doesn't go out of scope while updating many feeds, but it also must be
            destroyed after updating a feed to prevent memory leaks.
        """
        self.feedUpdater = FeedUpdater(self.db)
        self.feedUpdater.feedItemUpdateSignal.connect(self.onFeedItemUpdate)
        self.feedUpdater.feedUpdateMessageSignal.connect(self.showStatusBarMessage)

    @QtCore.Slot()
    def on_actionAbout_Qt_triggered(self):
        QtWidgets.QMessageBox.aboutQt(self, 'About Qt')

    @QtCore.Slot()
    def on_actionAbout_RssReader_triggered(self):
        QtWidgets.QMessageBox.about(self, "About PyRssReader", "PyRssReader by Jeff Geraci")

    def onFeedSelected(self, feedId):
        self.m_currentFeedId = feedId
        self.currentFeed = self.db.getFeed(feedId)
        if self.m_currentFeedId != kItemsOfInterestFeedId:
            feed = self.db.getFeed(feedId)
            self.ui.feedNameLabel.setText(feed.m_feedName)
            self.ui.feedImageLabel.setPixmap(feed.getFeedIcon())
            self.populateFeedItemView(feedId)
        else:
            self.ui.feedNameLabel.setText("Items of Interest")
            starPixmap = getResourceFilePixmap(kStarIcon)
            self.ui.feedImageLabel.setPixmap(starPixmap)
            ioiList = self.db.getItemsOfInterest()

            if ioiList is None:
                return

            # Read the actual feed items
            feedItemList = []
            for ioiTuple in ioiList:
                feedItem = self.db.getFeedItem(ioiTuple[1], ioiTuple[0])

                if feedItem is not None:
                    feedItemList.append(feedItem)
                else:
                    logging.error(f'Feed item {ioiTuple[1]} not found in feed {ioiTuple[0]}')

            self.titleTreeObj.addFeedItems(feedItemList, self.currentFeed, False)

    def populateFeedItemView(self, feedId, sameFeed=False):
        feedItemList = self.db.getFeedItems(feedId)
        self.titleTreeObj.addFeedItems(feedItemList, self.currentFeed, sameFeed)

    def onFeedItemSelected(self, feedId, feedItemGuid):
        feedItem = self.db.getFeedItem(feedItemGuid, feedId)

        if feedItem is not None:
            self.db.setFeedItemReadFlag(feedId, feedItemGuid, True)
            self.feedTreeObj.updateFeedCount(feedId)
            self.rssContentViewObj.setContents(feedItem, self.currentFeed)
        else:
            logging.error(f'Feed item {feedItemGuid} does not exist (feed ID: {feedId})')

    @QtCore.Slot()
    def onReselectFeedItem(self):
        """ Causes the current feed item to be reselected. """
        self.titleTreeObj.reselectFeedItem()

    def onFeedUpdateRequested(self, feedId):
        if feedId > 0:
            self.createFeedUpdater()
            self.feedUpdater.updateFeed(feedId, self.proxy)
        else:
            logging.error("onFeedUpdateRequested: Invalid feedId: {}".format(feedId))

    def startFeedUpdateTimer(self):
        self.feedUpdateTimer.start()

    def stopFeedUpdateTimer(self):
        self.feedUpdateTimer.stop()

    def resetFeedUpdateMinuteCount(self):
        self.minutesSinceLastFeedUpdate = 0

    @QtCore.Slot()
    def onFeedUpdateTimerTimeout(self):
        """ Slot to handle the feed update timer. """
        self.minutesSinceLastFeedUpdate += 1
        if self.minutesSinceLastFeedUpdate >= self.preferences.feedUpdateInterval:
            # Time to update feeds
            self.on_actionUpdate_Feeds_triggered()

    @QtCore.Slot()
    def on_actionUpdate_Feeds_triggered(self):
        self.stopFeedUpdateTimer()
        self.resetFeedUpdateMinuteCount()

        self.feedIdsToUpdate = self.db.getFeedIds()

        self.createFeedUpdater()
        self.updateNextFeed()

    def updateNextFeed(self):
        """ Starts the update process for the next feed in the list.  This is the feed that is
            at the head of self.feedIdsToUpdate. """
        if self.feedIdsToUpdate:
            feedIdToUpdate = self.feedIdsToUpdate.pop(0)
            self.feedUpdater.updateFeed(feedIdToUpdate, self.proxy)
        else:
            self.feedTreeObj.updateAllFeedCounts()
            self.showStatusBarMessage("Updating complete.")
            if not self.feedUpdateTimer.isActive():
                # Only want to do this if the timer is not running.  If the timer is running, calling
                # start() on it will restart it from 0.
                self.startFeedUpdateTimer()

            # Delete the feed updater to free its memory
            del self.feedUpdater

    def onFeedItemUpdate(self, feedId, feedItemList):
        self.db.addFeedItems(feedItemList, feedId)
        self.feedItemFilterMatcher.filterFeedItems(feedId, feedItemList)

        if feedId == self.m_currentFeedId:
            # Update title tree with new set of feed items
            self.populateFeedItemView(feedId, True)

        QtCore.QTimer.singleShot(0, self.updateNextFeed)

    @QtCore.Slot()
    def on_actionPreferences_triggered(self):
        prefsDialog = PrefsDialog(self, self.proxy, self.preferences)
        if prefsDialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.proxy = prefsDialog.getProxySettings()
            self.rssContentViewObj.setProxy(self.proxy)
            self.preferences = prefsDialog.getPreferences()
            self.saveSettings()


    @QtCore.Slot()
    def on_actionPurge_Old_News_triggered(self):
        purgeDlg = PurgeDialog(self)
        if purgeDlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            priorDays = purgeDlg.getDays()
            purgeUnreadItems = purgeDlg.purgeUnreadItems()

            self.feedPurger.purgeAllFeeds(priorDays, purgeUnreadItems)
            self.onFeedSelected(self.m_currentFeedId)   # Force repopulation of title tree


    def onPurgeSingleFeed(self, feedId):
        purgeDlg = PurgeDialog(self)
        if purgeDlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            priorDays = purgeDlg.getDays()
            purgeUnreadItems = purgeDlg.purgeUnreadItems()

            self.feedPurger.purgeSingleFeed(feedId, priorDays, purgeUnreadItems)

    def onFeedPurged(self, feedId):
        self.feedTreeObj.updateFeedCount(feedId)

        if feedId == self.m_currentFeedId:
            # Update title tree with new set of feed items
            self.populateFeedItemView(feedId, True)

    @QtCore.Slot()
    def on_actionAdd_Feed_triggered(self):
        dlg = NewFeedDialog(self, self.proxy)

        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            feed = dlg.getFeed()

            # Must add the feed to the database first, in order to have the feed ID set.
            feed = self.db.addFeed(feed)

            if feed is not None:
                feedId = feed.m_feedId

                if feedId > 0:
                    # Update feed ID with the value from the database
                    self.feedTreeObj.addFeed(feed)

                    # Switch to this feed
                    self.onFeedSelected(feedId)
                    # Fetch feed items
                    self.onFeedUpdateRequested(feedId)

    def onDeleteFeed(self, feedId):
        self.db.deleteFeed(feedId)

    @QtCore.Slot()
    def on_actionCreate_Global_Filter_triggered(self):
        dlg = FilterManagerDialog(self, self.db)
        dlg.exec()

    @QtCore.Slot()
    def on_actionEdit_Language_Filter_triggered(self):
        dlg = LanguageFilterDialog(self, self.db)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.languageFilter.initialize()
            # Reselecting the feed will repopulate title tree and content view.
            self.onFeedSelected(self.m_currentFeedId)

    @QtCore.Slot()
    def on_actionEdit_Ad_Filter_triggered(self):
        dlg = AdFilterDialog(self, self.db)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # Reselecting the feed will repopulate title tree and content view.
            self.onFeedSelected(self.m_currentFeedId)

    def onSetFeedReadState(self, feedId, readState):
        """ Marks all items in the given feed as read. """
        self.db.setFeedReadFlagAllItems(feedId, readState)
        self.titleTreeObj.setReadStateOfAllRows(readState)

    def showStatusBarMessage(self, message, timeout=10000):
        """ Displays a message on the status bar. """
        self.ui.statusBar.showMessage(message, timeout)

    def onDownloadEnclosure(self, enclosureUrl):
        # Don't clear message, until the enclosure has downloaded
        self.showStatusBarMessage("Downloading enclosure: {}".format(enclosureUrl), kDontClearMessage)

        self.enclosureDownloader = EnclosureDownloader(enclosureUrl, self.preferences.enclosureDirectory, self.proxy)
        self.enclosureDownloader.enclosureDownloadedSignal.connect(self.onEnclosureDownloaded)
        self.enclosureDownloader.start()

    def onEnclosureDownloaded(self, filename):
        self.showStatusBarMessage("{} downloaded.".format(filename))
        self.enclosureDownloader = None

    @QtCore.Slot()
    def onMinimizeApp(self):
        self.setWindowState(QtCore.Qt.WindowState.WindowMinimized)

    @QtCore.Slot()
    def on_actionOpen_Enclosure_Directory_triggered(self):
        urlStr = "file:///{}".format(self.preferences.enclosureDirectory)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlStr, QtCore.QUrl.ParsingMode.TolerantMode))

    @QtCore.Slot()
    def on_actionExport_OPML_triggered(self):
        exporter = OpmlExporter(self.db)

        filepathTuple = QtWidgets.QFileDialog.getSaveFileName(self, "Save OPML File")

        if filepathTuple:
            filepath = filepathTuple[0]
            exporter.export(filepath)

    @QtCore.Slot()
    def on_actionImport_OPML_triggered(self):
        importer = OpmlImporter(self.db)

        filepathTuple = QtWidgets.QFileDialog.getOpenFileName(self, "Load OPML File")

        if filepathTuple:
            filepath = filepathTuple[0]
            feeds = importer.importFeeds(filepath)

            feedIds = []
            for feed in feeds:
                # Must add the feed to the database first, in order to have the feed ID set.
                feed = self.db.addFeed(feed)

                if feed is not None:
                    feedId = feed.m_feedId

                    if feedId > 0:
                        # Update feed ID with the value from the database
                        feedIds.append(feedId)
                        self.feedTreeObj.addFeed(feed)

            # Switch to last feed
            self.onFeedSelected(feedId)

            # Fetch feed items for all feeds
            self.feedIdsToUpdate = feedIds
            self.stopFeedUpdateTimer()
            self.resetFeedUpdateMinuteCount()

            self.updateNextFeed()


    @QtCore.Slot()
    def on_actionAdd_to_Pocket_triggered(self):
        if self.rssContentViewObj.currentFeedItem is None:
            logging.error("self.rssContentViewObj.currentFeedItem is None.  (No feed item selected?)")
            return

        logging.info("Add to Pocket action triggered.  Title: {}, URL: {}".format(self.rssContentViewObj.filteredTitle, self.rssContentViewObj.currentFeedItem.m_link))

        if not self.db.isPocketInitialized():
            self.initializePocket()

        if not self.db.isPocketInitialized():
            errMsg = "Could not obtain Pocket authorization:"
            QtWidgets.QMessageBox.critical(self, kAppName, errMsg)
        else:
            result = self.pocketSupport.addArticleToPocket(self.rssContentViewObj.currentFeedItem.m_link, self.rssContentViewObj.filteredTitle)

            if result is True:
                QtWidgets.QMessageBox.information(self, "Add to Pocket", "The article was successfully added to Pocket.", QtWidgets.QMessageBox.StandardButton.Ok)
            else:
                QtWidgets.QMessageBox.critical(self, "Add to Pocket", "Could not add the article to Pocket.")

    def initializePocket(self):
        """ Initializes Pocket (ie, obtains the Pocket access token.)  This must be done from the UI, because a
            dialog box will need to be presented asking the user if the access was authorized.  This will be
            indicated by the appearance of the Google search page. """
        if self.pocketSupport.doStepOneOfAuthorization():
            # At this point, Pocket should have redirected the user to the redirect page, which is the Google search page.
            # Need to ask the user if this has happened.

            message = "When the Google search site appears, click Yes.  If it does not appear, click No."
            button = QtWidgets.QMessageBox.question(self, kAppName, message)

            if button == QtWidgets.QMessageBox.StandardButton.Yes:
                self.pocketSupport.doStepTwoOfAuthorization()


    def event(self, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.Type.WindowDeactivate:
            # If this application does still have the focus, which would be true in the case
            # of a dialog box being opened, don't minimize.
            if self.preferences.minimizeAppOnLoseFocus:
                if QtWidgets.QApplication.activeWindow() is None:
                    self.onMinimizeApp()
                    return True

        return super(PyRssReaderWindow, self).event(event)

    def closeEvent(self, event):
        self.shutdownApp()

    def shutdownApp(self):
        self.stopFeedUpdateTimer()
        feedOrderList = self.feedTreeObj.getFeedOrder()
        self.db.setFeedOrder(feedOrderList)
        self.db.close()
        self.saveSettings()

def main():
    # NOTE: Calling a log function before logging.basicConfig() will cause the logging to fail.

    handlers = [ ]
    handlers.append(RotatingFileHandler(getLogfilePath(kLogFile), maxBytes=kMaxLogileSize, backupCount=9))

    # Set log level based on whether we're running from a bundle or not
    logLevel = logging.INFO
    if runningFromBundle():
        logLevel = logging.DEBUG        # TODO: Change this back to INFO
    else:
        handlers.append(logging.StreamHandler())
        logLevel = logging.DEBUG

    logging.basicConfig(level=logLevel, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', handlers=handlers)

    # Simple logging - keep this here in case regular logging fails
    # logging.basicConfig(filename='myapp.log', level=logging.DEBUG)            Works in PyInstaller bundle
    # logging.basicConfig(filename='myapp.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')        # Works in PyInstaller bundle

    logging.info("Starting application...")
    logging.debug(f'Script path: {getScriptPath()}')
    logging.debug(f'Logfile: {getLogfilePath(kLogFile)}')

    if runningFromBundle():
        logging.debug("Running from within a PyInstaller bundle.")
    else:
        logging.debug("Running directly from source code.")

    wind = None
    returnVal = 0

    try:
        app = QtWidgets.QApplication(sys.argv)
        wind = PyRssReaderWindow()
        wind.show()
        returnVal = app.exec()

    except Exception as inst:
        logging.error(f'[main] Exception: type: {type(inst)}')
        logging.error(f'Exception args: {inst.args}')
        logging.error(f'Exception object: {inst}')
        returnVal = 1

        if wind is not None:
            wind.shutdownApp()

    logging.info("Shutting down...")
    logging.shutdown()

    return returnVal

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
