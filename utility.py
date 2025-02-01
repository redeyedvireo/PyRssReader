from PySide6 import QtGui
import sys, os, os.path
import time
import datetime
from datetime import timezone

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

def getResourceFileText(filename):
    scriptDir = os.getcwd()
    filePath = os.path.join(scriptDir, "Resources", filename)

    file = open(filePath, 'r')
    contents = file.read()
    file.close()

    return contents

def getResourceFilePixmap(filename):
    scriptDir = os.getcwd()
    filePath = os.path.join(scriptDir, "Resources", filename)

    file = open(filePath, 'rb')
    imageData = file.read()
    file.close()

    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(imageData)

    return pixmap

def getResourceFileIcon(filename):
    return QtGui.QIcon(getResourceFilePixmap(filename))

def getScriptPath():
  if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path, executable = os.path.split(sys.executable)
  else:
    application_path = os.path.dirname(os.path.abspath(__file__))

  return application_path

def getLogfilePath(logFileName):
    return os.path.join(getScriptPath(), logFileName)