import os, sys, datetime, logging
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pathlib import Path
from database import Database
from feed_tree import FeedTree

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

        self.feedTree = FeedTree(self.feedTree)

        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        print("Initializing application...")

        dbDir = self.getDatabasePath()
        print("DB dir: {}".format(dbDir))
        self.db.open(dbDir)

        feedList = self.db.getFeeds()
        #print("Feeds: {}".format(feedList))
        for feed in feedList:
            self.feedTree.addFeedToTopLevel(feed.m_feedTitle, feed.m_feedId, QtGui.QIcon(feed.m_feedFavicon))


    def getDatabasePath(self):
        return "{}\\{}".format(self.getDatabaseDirectory(), kDatabaseName)

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
