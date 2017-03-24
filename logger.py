import logging
import logging.config
import logging.handlers
import os.path

gLogger = None

kLogFile = 'RssReader.log'

class Logger(object):
    def __init__(self, logDir):
        super(Logger, self).__init__()

        self.logObj = logging.getLogger('pyrssreader')
        formatter = logging.Formatter('%(asctime)s -%(module)s- %(levelname)s - %(message)s')
        logFile = os.path.join(logDir, kLogFile)
        logHandler = logging.FileHandler(logFile)
        logHandler.setLevel(logging.DEBUG)
        logHandler.setFormatter(formatter)
        self.logObj.addHandler(logHandler)
        self.logObj.setLevel(logging.DEBUG)

    def LogDebug(self, msg):
        self.logObj.debug(msg)

    def LogInfo(self, msg):
        self.logObj.info(msg)

    def LogWarning(self, msg):
        self.logObj.warning(msg)

    def LogCritical(self, msg):
        self.logObj.critical(msg)

    def LogError(self, msg):
        self.logObj.error(msg)

def InitLogging(logDir):
    global gLogger

    if gLogger == None:
        gLogger = Logger(logDir)

def CloseLogging():
    global gLogger
    
    if gLogger != None:
        gLogger = None
