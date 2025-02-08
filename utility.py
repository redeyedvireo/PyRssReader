from PySide6 import QtCore, QtGui, QtWidgets
import sys, os, os.path
from pathlib import Path
import time
import datetime
from datetime import timezone
import logging

def julianDayToDate(julianDay):
    """ Returns a Python datetime object corresponding to the given Julian day. """
    dateTime = datetime.datetime.fromtimestamp(julianDay)

    # Testing:
    #qtDate = QtCore.QDateTime.fromTime_t(julianDay)
    #print("Python: {}, Qt: {}".format(dateTime, qtDate.toString("M/d/yyyy, h:mm AP")))
    return dateTime.replace(tzinfo=timezone.utc)

def dateToJulianDay(inDate):
    """ Returns a Julian day (ie, a 'timestamp') for the given date. """
    return int(time.mktime(inDate.timetuple()))

def getTextFileFromResource(filename):
    file = QtCore.QFile(f":/RssReader/Resources/{filename}")
    if file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text):
        stream = QtCore.QTextStream(file)
        text = stream.readAll()
        file.close()
        return text
    else:
        logging.error(f'Could not open text file from resources: {filename}')
        return ''

def getResourceFilePixmap(filename):
    return QtGui.QPixmap(f':/Resources/{filename}')

def getResourceFileIcon(filename):
    return QtGui.QIcon(f':/Resources/{filename}')

def textToDialog(title, text, parent = None):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.exec()

def getScriptPath():
  if runningFromBundle():
    application_path, executable = os.path.split(sys.executable)
  else:
    application_path = os.path.dirname(os.path.abspath(__file__))

  return application_path

def runningFromBundle():
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def getLogfilePath(logFileName):
    logFilePath = os.path.join(getScriptPath(), logFileName)
    return logFilePath

def getDatabaseDirectory(appName: str):
    procEnv = QtCore.QProcessEnvironment.systemEnvironment()

    if procEnv.contains("APPDATA"):
        # Indicates Windows platform
        appDataPath = procEnv.value("APPDATA")

        databasePath = "{}\\{}".format(appDataPath, appName)

        #  Create directory if non - existent
        dbDir = Path(databasePath)

        if not dbDir.exists():
            # Directory doesn't exist - create it.
            if not dbDir.mkdir():
                logging.error("Could not create the data directory: {}".format(databasePath))
                return None

        return databasePath
    else:
        return None

def getDatabasePath(appName: str, databaseName: str) -> str | None:
    databaseDir = getDatabaseDirectory(appName)
    if databaseDir is None:
        return None
    databasePath = os.path.join(databaseDir, databaseName)
    return databasePath

def getDefaultEnclosureDirectory():
    """ Returns the default location for downloading enclosures.  This is the standard Downloads directory. """
    downloadDirectory = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DownloadLocation)
    return downloadDirectory
