import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path
from feed import Feed


class Database(object):
    def __init__(self):
        super(Database, self).__init__()
        self.db = None

    def open(self, pathName):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        p = Path(pathName)
        dbExists = p.is_file()

        self.db.setDatabaseName(pathName)

        if self.db.open():
            if dbExists:
                print("Database open")
                logging.info("Database opened")
            else:
                # TODO: Create the database, and all tables
                print("Database {} does not exist.".format(pathName))
                logging.info("Database doesn't exist")
        else:
            print("Error: could not open database.")
            logging.error("Could not open database")

    def close(self):
        if self.db is not None:
            self.db.close()

    def getFeeds(self):
        """ Returns a list of feed objects, consisting of all feeds. """
        feedList = []
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select feedid, parentid, name, title, description, language, url, added, lastupdated, webpagelink, favicon, image, lastpurged from feeds")

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            # Todo - log the error
            #QLOG_ERROR() << "Error when attempting to retrieve all feeds: " << sqlErr.text()
            print("getFeeds: error: {}".format(sqlErr.text()))

        while queryObj.next():
            feedObj = Feed()
            feedObj.m_feedId = queryObj.record().value(0)
            feedObj.m_parentId = queryObj.record().value(1)
            feedObj.m_feedName = queryObj.record().value(2)
            feedObj.m_feedTitle = queryObj.record().value(3)
            feedObj.m_feedDescription = queryObj.record().value(4)
            feedObj.m_feedLanguage = queryObj.record().value(5)
            feedObj.m_feedUrl = queryObj.record().value(6)
            feedObj.m_feedDateAdded = queryObj.record().value(7)    # TODO: Convert to time
            feedObj.m_feedLastUpdated = queryObj.record().value(8)  # TODO: Convert to time
            feedObj.m_feedWebPageLink = queryObj.record().value(9)
            favicon = queryObj.record().value(10)
            if isinstance(favicon, QtCore.QByteArray):
                feedObj.m_feedFavicon.loadFromData(favicon)

            feedObj.m_feedImage = queryObj.record().value(11)
            feedObj.m_feedLastPurged = queryObj.record().value(12)  # TODO: Convert to time
            feedList.append(feedObj)

        return feedList
