import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path
from exceptions import DbError
from feed import Feed
from feed_item import FeedItem
from utility import julianDayToDate, dateToJulianDay

class Database:
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
            else:
                # TODO: Create the database, and all tables
                #       Note: when creating the language filter database, add some hard-coded words
                errMsg = "Database {} does not exist.".format(pathName)
                print(errMsg)
                logging.info(errMsg)
        else:
            print("Error: could not open database.")
            logging.error("Could not open database")

    def close(self):
        if self.db is not None:
            self.db.close()

    def beginTransaction(self):
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("begin transaction")
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            errMsg = "Error beginning a transaction: {}".format(sqlErr.text())
            logging.error(errMsg)
            print(errMsg)

    def endTransaction(self):
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("end transaction")
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            errMsg = "Error ending a transaction: {}".format(sqlErr.text())
            logging.error(errMsg)
            print(errMsg)

    def getFeeds(self):
        """ Returns a list of feed objects, consisting of all feeds. """
        feedList = []
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select feedid, parentid, name, title, description, language, url, added, lastupdated, webpagelink, favicon, image, lastpurged from feeds")

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            logging.error("Error when attempting to retrieve all feeds: {}".format(sqlErr.text()))
            print("getFeeds: error: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here
            return []

        while queryObj.next():
            feedObj = Feed()

            feedObj.m_feedId = queryObj.record().value(0)
            feedObj.m_parentId = queryObj.record().value(1)
            feedObj.m_feedName = queryObj.record().value(2)
            feedObj.m_feedTitle = queryObj.record().value(3)
            feedObj.m_feedDescription = queryObj.record().value(4)
            feedObj.m_feedLanguage = queryObj.record().value(5)
            feedObj.m_feedUrl = queryObj.record().value(6)
            feedObj.m_feedDateAdded = julianDayToDate(queryObj.record().value(7))    # Convert to time
            feedObj.m_feedLastUpdated = julianDayToDate(queryObj.record().value(8))  # Convert to time
            feedObj.m_feedWebPageLink = queryObj.record().value(9)
            favicon = queryObj.record().value(10)
            if isinstance(favicon, QtCore.QByteArray):
                feedObj.m_feedFavicon.loadFromData(favicon)

            feedObj.m_feedImage = queryObj.record().value(11)
            feedObj.m_feedLastPurged = julianDayToDate(queryObj.record().value(12))  # Convert to time
            feedList.append(feedObj)

        return feedList


    def getFeed(self, feedId):
        """ Returns data for a single feed. """
        feed = Feed()
        
        queryObj = QtSql.QSqlQuery(self.db)
        
        queryStr = "select feedid, parentid, name, title, description, language, url, added, lastupdated, "
        queryStr += "webpagelink, favicon, image, lastpurged from feeds where feedid=?"
        
        queryObj.prepare(queryStr)
        
        queryObj.addBindValue(feedId)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            logging.error("Error when attempting to retrieve a single feeds: {}".format(sqlErr.text()))
            print("getFeed: error: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here
            return feed
        
        while queryObj.next():
            feed.m_feedId = queryObj.record().value(0)
            feed.m_parentId = queryObj.record().value(1)
            feed.m_feedName = queryObj.record().value(2)
            feed.m_feedTitle = queryObj.record().value(3)
            feed.m_feedDescription = queryObj.record().value(4)
            feed.m_feedLanguage = queryObj.record().value(5)
            feed.m_feedUrl = queryObj.record().value(6)
            feed.m_feedDateAdded = julianDayToDate(queryObj.record().value(7))    # Convert to time
            feed.m_feedLastUpdated = julianDayToDate(queryObj.record().value(8))  # Convert to time
            feed.m_feedWebPageLink = queryObj.record().value(9)
            favicon = queryObj.record().value(10)
            if isinstance(favicon, QtCore.QByteArray):
                feed.m_feedFavicon.loadFromData(favicon)

            feed.m_feedImage = queryObj.record().value(11)
            feed.m_feedLastPurged = julianDayToDate(queryObj.record().value(12))  # Convert to time
            
        return feed

    def getFeedItemGuids(self, feedId):
        """ Returns the GUIDs for all feed items for the given feed.
            This is used when adding new feed items, to ensure that they do not already exist. """
        guidList = []
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select "
        queryStr += "guid"
        queryStr += " from {}".format(feedTableName)

        queryObj.prepare(queryStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            logging.error("Error when attempting to retrieve all guids: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here
            return []

        while queryObj.next():
            guid = queryObj.record().value(0)
            guidList.append(guid)

        return guidList

    def getFeedItems(self, feedId):
        """ Returns a list of feed items for the given feed ID. """
        feedItemList = []
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select "
        queryStr += "title, author, link, description, categories, pubdatetime, "
        queryStr += "thumbnaillink, thumbnailwidth, thumbnailheight, "
        queryStr += "guid, feedburneroriglink, readflag, "
        queryStr += "enclosurelink, enclosurelength, enclosuretype, contentencoded "
        queryStr += "from {}".format(feedTableName)

        queryObj.prepare(queryStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            logging.error("Error when attempting to retrieve all feed items: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here
            return []

        while queryObj.next():
            feedItem = FeedItem()

            feedItem.m_title = queryObj.record().value(0)
            feedItem.m_author = queryObj.record().value(1)
            feedItem.m_link = queryObj.record().value(2)
            feedItem.m_description = queryObj.record().value(3)

            categoriesStr = queryObj.record().value(4)
            feedItem.m_categories = list(filter(None, categoriesStr.split(",")))    # Filter out empty strings

            feedItem.m_publicationDatetime = julianDayToDate(queryObj.record().value(5))     # Convert to datetime
            feedItem.m_thumbnailLink = queryObj.record().value(6)
            thumbnailWidth = queryObj.record().value(7)
            thumbnailHeight = queryObj.record().value(8)
            feedItem.m_thumbnailSize = QtCore.QSize(thumbnailWidth, thumbnailHeight)

            feedItem.m_guid = queryObj.record().value(9)
            feedItem.m_feedburnerOrigLink = queryObj.record().value(10)
            feedItem.m_bRead = True if queryObj.record().value(11) == 1 else False

            feedItem.m_enclosureLink = queryObj.record().value(12)
            feedItem.m_enclosureLength = queryObj.record().value(13)
            feedItem.m_enclosureType = queryObj.record().value(14)
            feedItem.m_encodedContent = queryObj.record().value(15)

            feedItem.m_parentFeedId = feedId

            feedItemList.append(feedItem)

        return feedItemList


    def addFeedItems(self, feedItemList, feedId):
        """ Adds multiple feed items, using a transaction.  Does not check for duplicates. """
        self.beginTransaction()

        for feedItem in feedItemList:
            self.addFeedItem(feedItem, feedId)

        self.endTransaction()


    def addFeedItem(self, feedItem, feedId):
        """ Adds the given feed item to the given feed. """
        queryObj = QtSql.QSqlQuery(self.db)

        feedTableName = self.feedItemsTableName(feedId)

        queryStr = "insert into {} ".format(feedTableName)
        queryStr += "(title, author, link, description, categories, pubdatetime, thumbnaillink, thumbnailwidth, "
        queryStr += "thumbnailheight, guid, feedburneroriglink, readflag, "
        queryStr += "enclosurelink, enclosurelength, enclosuretype, contentencoded)"
        queryStr += "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        queryObj.prepare(queryStr)

        queryObj.addBindValue(feedItem.m_title)
        queryObj.addBindValue(feedItem.m_author)
        queryObj.addBindValue(feedItem.m_link)
        queryObj.addBindValue(feedItem.m_description)
        queryObj.addBindValue(",".join(feedItem.m_categories))
        queryObj.addBindValue(dateToJulianDay(feedItem.m_publicationDatetime))
        queryObj.addBindValue(feedItem.m_thumbnailLink)
        queryObj.addBindValue(feedItem.m_thumbnailSize.width())
        queryObj.addBindValue(feedItem.m_thumbnailSize.height())
        queryObj.addBindValue(feedItem.m_guid)
        queryObj.addBindValue(feedItem.m_feedburnerOrigLink)
        queryObj.addBindValue(1 if feedItem.isRead() else 0)
        queryObj.addBindValue(feedItem.m_enclosureLink)
        queryObj.addBindValue(feedItem.m_enclosureLength)
        queryObj.addBindValue(feedItem.m_enclosureType)
        queryObj.addBindValue(feedItem.m_encodedContent)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            errMsg = "Error adding a feed item: {}".format(sqlErr.text())
            logging.error(errMsg)
            print(errMsg)


    def getFeedItem(self, guid, feedId):
        """ Retrieves a single feed item."""
        feedItem = FeedItem()

        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select "
        queryStr += "title, author, link, description, categories, pubdatetime, "
        queryStr += "thumbnaillink, thumbnailwidth, thumbnailheight, "
        queryStr += "guid, feedburneroriglink, readflag, "
        queryStr += "enclosurelink, enclosurelength, enclosuretype, contentencoded "
        queryStr += "from {} where guid=?".format(feedTableName)

        queryObj.prepare(queryStr)

        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            logging.error("Error when attempting to retrieve a single feed item: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here
            return feedItem

        while queryObj.next():
            feedItem.m_title = queryObj.record().value(0)
            feedItem.m_author = queryObj.record().value(1)
            feedItem.m_link = queryObj.record().value(2)
            feedItem.m_description = queryObj.record().value(3)

            categoriesStr = queryObj.record().value(4)
            feedItem.m_categories = list(filter(None, categoriesStr.split(",")))    # Filter out empty strings

            feedItem.m_publicationDatetime = julianDayToDate(queryObj.record().value(5))     # Convert to datetime
            feedItem.m_thumbnailLink = queryObj.record().value(6)
            thumbnailWidth = queryObj.record().value(7)
            thumbnailHeight = queryObj.record().value(8)
            feedItem.m_thumbnailSize = QtCore.QSize(thumbnailWidth, thumbnailHeight)

            feedItem.m_guid = queryObj.record().value(9)
            feedItem.m_feedburnerOrigLink = queryObj.record().value(10)
            feedItem.m_bRead = True if queryObj.record().value(11) == 1 else False

            feedItem.m_enclosureLink = queryObj.record().value(12)
            feedItem.m_enclosureLength = queryObj.record().value(13)
            feedItem.m_enclosureType = queryObj.record().value(14)
            feedItem.m_encodedContent = queryObj.record().value(15)

            feedItem.m_parentFeedId = feedId

        return feedItem

    def feedItemsTableName(self, feedId):
        tableName = "FeedItems{:06}".format(feedId)
        return tableName

    def getFilteredWords(self):
        """ Reads the filtered words from the database, and returns them as a list. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select word from filteredwords"

        queryObj.prepare(queryStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            errMsg = "Error when attempting to retrieve all filtered words: {}".format(sqlErr.text())
            logging.error(errMsg)
            raise DbError(errMsg)

        allFilteredWords = []

        while queryObj.next():
            filteredWord = queryObj.record().value(0)

            if filteredWord:
                allFilteredWords.append(filteredWord)

        return allFilteredWords

    def getAdFilters(self):
        """ Reads the URLS/domains for filtering ads, and returns them as a list. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select word from adfilters"

        queryObj.prepare(queryStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            errMsg = "Error when attempting to retrieve all ad filters: {}".format(sqlErr.text())
            logging.error(errMsg)
            raise DbError(errMsg)

        allFilters = []

        while queryObj.next():
            filteredWord = queryObj.record().value(0)

            if filteredWord:
                allFilters.append(filteredWord)

        return allFilters
