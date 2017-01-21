import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path
from feed import Feed
from feed_item import FeedItem


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
            else:
                # TODO: Create the database, and all tables
                errMsg = "Database {} does not exist.".format(pathName)
                print(errMsg)
                logging.info(errMsg)
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
            logging.error("Error when attempting to retrieve all feeds: {}".format(sqlErr.text()))
            print("getFeeds: error: {}".format(sqlErr.text()))
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
            return feed
        
        while queryObj.next():
            feed.m_feedId = queryObj.record().value(0)
            feed.m_parentId = queryObj.record().value(1)
            feed.m_feedName = queryObj.record().value(2)
            feed.m_feedTitle = queryObj.record().value(3)
            feed.m_feedDescription = queryObj.record().value(4)
            feed.m_feedLanguage = queryObj.record().value(5)
            feed.m_feedUrl = queryObj.record().value(6)
            feed.m_feedDateAdded = queryObj.record().value(7)    # TODO: Convert to time
            feed.m_feedLastUpdated = queryObj.record().value(8)  # TODO: Convert to time
            feed.m_feedWebPageLink = queryObj.record().value(9)
            favicon = queryObj.record().value(10)
            if isinstance(favicon, QtCore.QByteArray):
                feed.m_feedFavicon.loadFromData(favicon)

            feed.m_feedImage = queryObj.record().value(11)
            feed.m_feedLastPurged = queryObj.record().value(12)  # TODO: Convert to time
            
        return feed

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
            return []

        while queryObj.next():
            feedItem = FeedItem()

            feedItem.m_title = queryObj.record().value(0)
            feedItem.m_author = queryObj.record().value(1)
            feedItem.m_link = queryObj.record().value(2)
            feedItem.m_description = queryObj.record().value(3)

            categoriesStr = queryObj.record().value(4)
            feedItem.m_categories = list(filter(None, categoriesStr.split(",")))    # Filter out empty strings

            feedItem.m_publicationDatetime = queryObj.record().value(5)     # Convert to datetime
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
            return feedItem

        while queryObj.next():
            feedItem.m_title = queryObj.record().value(0)
            feedItem.m_author = queryObj.record().value(1)
            feedItem.m_link = queryObj.record().value(2)
            feedItem.m_description = queryObj.record().value(3)

            categoriesStr = queryObj.record().value(4)
            feedItem.m_categories = list(filter(None, categoriesStr.split(",")))    # Filter out empty strings

            feedItem.m_publicationDatetime = queryObj.record().value(5)     # Convert to datetime
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
