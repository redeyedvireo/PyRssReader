import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path
from exceptions import DbError
from feed import Feed
from feed_item import FeedItem
from feed_item_filter import  FeedItemFilter
from utility import julianDayToDate, dateToJulianDay

# Global value data type constants
kDataTypeInteger = 0
kDataTypeString = 1
kDataTypeBlob = 2

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

    def reportError(self, errorMessage):
        logging.error(errorMessage)
        print(errorMessage)
        raise DbError(errorMessage)

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
            self.reportError("Error ending a transaction: {}".format(sqlErr.text()))

    def getGlobalValue(self, key):
        """ Returns the value of a 'global value' for the given key. """
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select datatype from globals where key = ?")
        queryObj.bindValue(0, key)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve a global value key: {}".format(sqlErr.text()))
            return None

        if queryObj.next():
            typeField = queryObj.record().indexOf("datatype")

            dataType = queryObj.value(typeField)
        else:
            # key not found
            return None

        if dataType == kDataTypeInteger:
            createStr = "select intval from globals where key=?"
        elif dataType == kDataTypeString:
            createStr = "select stringval from globals where key=?"
        elif dataType == kDataTypeBlob:
            createStr = "select blobval from globals where key=?"
        else:
            # Unknown data type
            self.reportError("getGlobalValue: unknown data type: {}".format(dataType))
            return None

        # Now that the data type is known, retrieve the data itself.
        queryObj.prepare(createStr)
        queryObj.bindValue(0, key)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve a page: {}".format(sqlErr.text()))
            return None

        if queryObj.next():
            if dataType == kDataTypeInteger:
                valueField = queryObj.record().indexOf("intval")
            elif dataType == kDataTypeString:
                valueField = queryObj.record().indexOf("stringval")
            elif dataType == kDataTypeBlob:
                valueField = queryObj.record().indexOf("blobval")

            value = queryObj.value(valueField)
            return value

    def getFeeds(self):
        """ Returns a list of feed objects, consisting of all feeds. """
        feedList = []
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select feedid, parentid, name, title, description, language, url, added, lastupdated, webpagelink, favicon, image, lastpurged from feeds")

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve all feeds: {}".format(sqlErr.text()))
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


    def getFeedIds(self):
        """ Returns a list of feed IDs. """
        feedList = []
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select feedid from feeds")

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve feed IDs: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here
            return []

        while queryObj.next():
            feedId = queryObj.record().value(0)
            feedList.append(feedId)

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
            self.reportError("Error when attempting to retrieve a single feeds: {}".format(sqlErr.text()))
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

    def getFeedItemUnreadCount(self, feedId):
        """ Returns the number of unread feed items in the given feed. """
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        # Determine number of unread items
        queryStr = "select title from {} where readflag='0'".format(feedTableName)
        queryObj.prepare(queryStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve number of unread items in feed: {}".format(sqlErr.text()))
            return 0

        numUnreadItems = 0

        while queryObj.next():
            numUnreadItems += 1

        return numUnreadItems

    def getUnreadCountForItemsOfInterest(self):
        """ Returns the number of unread feed items in the Items of Interest feed. """
        ioiList = self.getItemsOfInterest()
        unreadCount = 0

        for ioiTuple in ioiList:
            if not self.isFeedItemRead(ioiTuple[0], ioiTuple[1]):
                unreadCount += 1

        return unreadCount

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
            self.reportError("Error when attempting to retrieve all guids: {}".format(sqlErr.text()))
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
            self.reportError("Error when attempting to retrieve all feed items: {}".format(sqlErr.text()))
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
            self.reportError("Error adding a feed item: {}".format(sqlErr.text()))
            # TODO: Maybe an exception should be thrown here


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
            self.reportError("Error when attempting to retrieve a single feed item: {}".format(sqlErr.text()))
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

    def deleteFeedItem(self, feedId, guid):
        """ Deletes the given feed item. """
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "delete from {} where guid=?".format(feedTableName)

        queryObj.prepare(queryStr)

        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete a feed item: {}".format(sqlErr.text()))

    def setFeedItemReadFlag(self, feedId, guid, readFlag):
        """ Sets the read flag of the given feed item."""
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "update {} set readflag=? where guid=?".format(feedTableName)

        queryObj.prepare(queryStr)

        queryObj.addBindValue(1 if readFlag else 0)
        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to set feed item's read flag: {}".format(sqlErr.text()))

    def isFeedItemRead(self, feedId, guid):
        """ Returns True if the given feed item is read, False otherwise.
            False is returned if the feed item doesn't exist. """
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)
        queryStr = "select readflag from {} where guid=?".format(feedTableName)
        queryObj.prepare(queryStr)

        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to get feed item's read flag: {}".format(sqlErr.text()))
            return False

        bReturn = False
        if queryObj.next():
            readFlag = queryObj.record().value(0)
            bReturn = True if readFlag == 1 else False

        return bReturn

    def getItemsOfInterest(self):
        """ Retrieves all the items of interest, as a list of tuples of the form: (feedId, guid). """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select feedid, guid from itemsofinterest"

        queryObj.prepare(queryStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when retrieving items of interest: {}".format(sqlErr.text()))
            return

        itemsOfInterestList = []

        while queryObj.next():
            feedId = queryObj.record().value(0)
            guid = queryObj.record().value(1)
            itemsOfInterestList.append( (feedId, guid) )

        return itemsOfInterestList

    def addItemOfInterest(self, feedId, guid):
        """ Adds a feed item to the Items of Interest feed. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "insert into itemsofinterest (feedid, guid) values (?, ?)"

        queryObj.prepare(queryStr)
        queryObj.addBindValue(feedId)
        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when adding an item of interest: {}".format(sqlErr.text()))

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
            self.reportError("Error when attempting to retrieve all filtered words: {}".format(sqlErr.text()))

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
            self.reportError("Error when attempting to retrieve all ad filters: {}".format(sqlErr.text()))

        allFilters = []

        while queryObj.next():
            filteredWord = queryObj.record().value(0)

            if filteredWord:
                allFilters.append(filteredWord)

        return allFilters

    def getFeedItemFilters(self):
        """ Returns a list of all the global feed item filters. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "select filterid, feedid, field, verb, querystring, action from feeditemfilters"
        queryObj.prepare(queryStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve all feed item filters: {}".format(sqlErr.text()))
            return []

        allFilters = []

        while queryObj.next():
            feedItemFilter = FeedItemFilter()

            feedItemFilter.m_filterId = queryObj.record().value(0)
            feedItemFilter.m_feedId = queryObj.record().value(1)
            feedItemFilter.m_fieldId = queryObj.record().value(2)
            feedItemFilter.m_verb = queryObj.record().value(3)
            feedItemFilter.m_queryStr = queryObj.record().value(4)
            feedItemFilter.m_action = queryObj.record().value(5)

            allFilters.append(feedItemFilter)

        return allFilters
