from PyQt5 import QtCore
import os, os.path
import datetime

def julianDayToDate(julianDay):
    """ Returns a Python datetime object corresponding to the given Julian day. """
    dateTime = datetime.datetime.fromtimestamp(julianDay)

    # Testing:
    #qtDate = QtCore.QDateTime.fromTime_t(julianDay)
    #print("Python: {}, Qt: {}".format(dateTime, qtDate.toString("M/d/yyyy, h:mm AP")))
    return dateTime

def getResourceFileText(filename):
    scriptDir = os.getcwd()
    filePath = os.path.join(scriptDir, "Resources", filename)

    file = open(filePath, 'r')
    contents = file.read()
    file.close()

    return contents
