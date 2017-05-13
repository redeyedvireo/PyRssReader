from PyQt5 import QtGui
import os, os.path
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
