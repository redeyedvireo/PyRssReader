import os, sys, datetime
from PyQt5 import QtCore, QtNetwork, QtWidgets, uic
from pathlib import Path
from database import Database

kDatabaseName = "Feeds.db"
kAppName      = "RssReader"         # Only needed for finding the database path

# ---------------------------------------------------------------
class PyRssReaderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PyRssReaderWindow, self).__init__()
        uic.loadUi('PyRssReaderWindow.ui', self)

        self.db = Database()

        dbDir = self.getDatabasePath()
        print("DB dir: {}".format(dbDir))
        self.db.open(dbDir)

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


# ---------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = PyRssReaderWindow()
    wind.show()

    sys.exit(app.exec_())
