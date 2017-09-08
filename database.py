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

# Current database version.  Previous versions are not handled by the Python version.
kCurrentDatabaseVersion = 7

# Name of item in the globals table that indicates the version of the database
kDatabaseVersionId = "databaseversion"

#
kFeedOrderGlobalKey = "feed-order"

kPocketUsernameKey = "pocket-username"
kPocketAccessToken = "pocket-accesstoken"


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
                self.updateDatabase()
            else:
                # Create the database, and all tables
                self.createNewDatabase()
        else:
            print("Error: could not open database.")
            logging.error("Could not open database")

    def close(self):
        if self.db is not None:
            self.db.close()

    def createNewDatabase(self):
        """ Creates a new database. """
        logging.info("Creating new database...")

        self.createGlobalsTable()
        self.createFeedTable()
        self.createFilteredWordsTable()
        self.createItemsOfInterestTable()
        self.createFilterTable()

        self.createAdFilterTable()

        # Initialize global data
        self.setGlobalValue("highestfeedid", 0)     # Highest value currently used for a feed ID - probably not needed any more
        self.setGlobalValue(kFeedOrderGlobalKey, "")    # Order in which feeds appear in the UI
        self.setGlobalValue(kDatabaseVersionId, kCurrentDatabaseVersion)

    def createGlobalsTable(self):
        """ Creates the globals table. """
        queryObj = QtSql.QSqlQuery(self.db)

        createStr = "create table globals ("
        createStr += "key text UNIQUE, "
        createStr += "datatype int, "
        createStr += "intval int, "
        createStr += "stringval text, "
        createStr += "blobval blob"
        createStr += ")"

        queryObj.prepare(createStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to the globals table: {}".format(sqlErr.text()))

    def createFeedTable(self):
        """ Creates the feed table. """
        queryObj = QtSql.QSqlQuery(self.db)

        createStr = "create table feeds ("
        createStr += "feedid integer primary key, "  # Unique Feed ID (must not be 0).  SQLite guarantees this field to be unique
        createStr += "name text, "  # User - specified name of feed
        createStr += "url text, "  # Feed URL
        createStr += "parentid integer, "  # Page's parent page (TODO: Figure out how to use this)
        createStr += "added integer, "  # Date and time the feed was added, as a time_t
        createStr += "lastupdated integer, "  # Date and time page was last updated, as a time_t
        createStr += "title text, "  # Feed title
        createStr += "language text, "  # Feed language
        createStr += "description text, "  # Feed description
        createStr += "webpagelink text, "  # URL of web site that owns this feed
        createStr += "favicon blob, "  # Favicon for feed's main web site
        createStr += "image blob, "  # Feed image(not a favicon)
        createStr += "lastpurged integer default 0"  # Date and time the feed was last purged

        createStr += ")"

        queryObj.prepare(createStr)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to create the feed table: {}".format(sqlErr.text()))

    def createFeedItemsTable(self, feedId):
        """ Creates a feed item table. """
        feedTableName = self.feedItemsTableName(feedId)
        queryObj = QtSql.QSqlQuery(self.db)

        createStr = "create table {} (".format(feedTableName)
        createStr += "title text, " # Item title
        createStr += "author text, " # Item author
        createStr += "link text, " # Item link
        createStr += "description text, " # Item description
        createStr += "categories text, " # Item categories
        createStr += "pubdatetime integer, " # Date / time of item 's publication, as a time_t
        createStr += "thumbnaillink text, " # Link to item 's thumbnail
        createStr += "thumbnailwidth integer, " # Width of thumbnail
        createStr += "thumbnailheight integer, " # Height of thumbnail
        createStr += "guid text UNIQUE, " # Item guid(usually just the URL of the article)
        createStr += "feedburneroriglink text, " # Feedburner link(possibly unnecessary?)
        createStr += "readflag integer, " # 0 for Not Read, non - zero for Read
        createStr += "enclosurelink text, " # Link to media enclosure(ie, podcast)
        createStr += "enclosurelength integer, " # Length of enclosure
        createStr += "enclosuretype text, " # Type of enclosure(such as "media/mpeg")
        createStr += "contentencoded text " # Store < content: encoded > tag data
        createStr += ")"

        queryObj.prepare(createStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to create a feed item table: {}".format(sqlErr.text()))

    def deleteFeedItemsTable(self, feedId):
        """ Deletes a feed items table. """
        feedItemsTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)
        queryStr = "drop table {}".format(feedItemsTableName)

        queryObj.prepare(queryStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete a feed items table: {}".format(sqlErr.text()))

    def createFilteredWordsTable(self):
        """ Creates the filtered words (aka language filter) table. """
        queryObj = QtSql.QSqlQuery(self.db)

        # Create filteredwords table - table to hold words that should not be displayed.
        # Words in this table will be replaced with asterisks (or something similar) when
        # displayed to the user.
        createStr = "create table filteredwords ("
        createStr += "word text "  # Word to filter
        createStr += ")"

        queryObj.prepare(createStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to create the filtered words table: {}".format(sqlErr.text()))

    def createItemsOfInterestTable(self):
        """ Creates the Items of Interest table. """
        queryObj = QtSql.QSqlQuery(self.db)

        # Create items of interest table - table that holds links to interesting feed items
        createStr = "create table itemsofinterest ("
        createStr += "feedid integer, " # Feed ID of this item
        createStr += "guid text "       # Item guid
        createStr += ")"

        queryObj.prepare(createStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to create the Items of Interest table: {}".format(sqlErr.text()))

    def createFilterTable(self):
        """ Creates the filter table. """
        queryObj = QtSql.QSqlQuery(self.db)

        # Create items of interest table - table that holds links to interesting feed items
        createStr = "create table feeditemfilters ("
        createStr += "filterid integer primary key, "  # Filter ID
        createStr += "feedid integer, "  # Feed ID
        createStr += "field integer, "  # ID of field to query
        createStr += "verb integer, "  # Query action to perform
        createStr += "querystring text, "  # String to look for
        createStr += "action integer "  # Action ID
        createStr += ")"

        queryObj.prepare(createStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to create the filter table: {}".format(sqlErr.text()))

    def createAdFilterTable(self):
        """ Creates the ad filter table. """
        queryObj = QtSql.QSqlQuery(self.db)

        # Create ad filter table - table that holds strings of ad-related words to filter.
        # When HTML elements are encountered with these words, the HTML elements will be
        # removed.  Such elements contain undesirable advertisement-related content.
        createStr = "create table adfilters ("
        createStr += "word text "  # Word to filter
        createStr += ")"

        queryObj.prepare(createStr)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to create the ad filter table: {}".format(sqlErr.text()))

    def reportError(self, errorMessage):
        logging.error(errorMessage)
        print(errorMessage)

        # TODO: Decide if throwing an error is the right thing to do.
        #raise DbError(errorMessage)

    def updateDatabase(self):
        """ Updates the database to the current version. """
        # Nothing to do at this point.
        pass

    def beginTransaction(self):
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("begin transaction")
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error beginning a transaction: {}".format(sqlErr.text()))

    def endTransaction(self):
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("end transaction")
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error ending a transaction: {}".format(sqlErr.text()))

    def vacuumDatabase(self):
        """ Performs a 'vacuum' operation on the database.  This compacts the database file. """
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("vacuum;")

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to vacuum the database: {}".format(sqlErr.text()))

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


    def setGlobalValue(self, key, value):
        """ Sets the value of the given key to the given value. """

        # See if the key exists
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select datatype from globals where key = ?")
        queryObj.bindValue(0, key)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to determine if a global value exists: {}".format(sqlErr.text()))
            return

        if queryObj.next():
            # Key exists; update its value
            if isinstance(value, int):
                createStr = "update globals set intval=? where key=?"
            elif isinstance(value, str):
                createStr = "update globals set stringval=? where key=?"
            elif isinstance(value, QtCore.QByteArray):
                createStr = "update globals set blobval=? where key=?"
            else:
                self.reportError("setGlobalValue: invalid data type")
                return

            queryObj.prepare(createStr)

            queryObj.addBindValue(value)
            queryObj.addBindValue(key)
        else:
            if isinstance(value, int):
                createStr = "insert into globals (key, datatype, intval) values (?, ?, ?)"
                dataType = kDataTypeInteger
            elif isinstance(value, str):
                createStr = "insert into globals (key, datatype, stringval) values (?, ?, ?)"
                dataType = kDataTypeString
            elif isinstance(value, QtCore.QByteArray):
                createStr = "insert into globals (key, datatype, blobval) values (?, ?, ?)"
                dataType = kDataTypeBlob
            else:
                self.reportError("setGlobalValue: invalid data type")
                return

            queryObj.prepare(createStr)

            queryObj.addBindValue(key)
            queryObj.addBindValue(dataType)
            queryObj.addBindValue(value)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to set a global value: {}".format(sqlErr.text()))


    def globalValueExists(self, key):
        """ Checks if a global value exists. """
        queryObj = QtSql.QSqlQuery(self.db)
        queryObj.prepare("select datatype from globals where key=?")
        queryObj.addBindValue(key)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()

        if sqlErr.type() != QtSql.QSqlError.NoError:
            return False
        else:
            atLeastOne = queryObj.next()
            return atLeastOne


    def getFeedOrder(self):
        """ Returns the list of feeds, in the order in which they were organized on the UI by the user.
            This is returned as a list of ints. """
        feedIdStr = self.getGlobalValue(kFeedOrderGlobalKey)
        feedOrder = []
        if feedIdStr:
            feedOrderStr = feedIdStr.split(",")
            if len(feedOrderStr) > 0:
                feedOrder = [int(idStr) for idStr in feedOrderStr]
        return feedOrder

    def removeFeedFromFeedOrder(self, feedId):
        """ Removes the given feed ID from the feed order. """
        feedOrderList = self.getFeedOrder()

        try:
            feedOrderList.remove(feedId)
            self.setFeedOrder(feedOrderList)
        except ValueError:
            self.reportError("db.removeFeedFromFeedOrder: Feed ID {} was not found in the feed order.".format(feedId))

    def setFeedOrder(self, feedOrderList):
        """ Sets the order of feeds in the database. """
        feedIdStrList = [ str(x) for x in feedOrderList]
        feedOrderString = ",".join(feedIdStrList)
        self.setGlobalValue(kFeedOrderGlobalKey, feedOrderString)

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


    def addFeed(self, feed):
        """ Adds a feed to the database.  Returns the feed with its feed ID updated to reflect the actual feed ID. """

        # Write favicon to a buffer
        faviconBytes = QtCore.QByteArray()
        tempBuffer = QtCore.QBuffer(faviconBytes)
        tempBuffer.open(QtCore.QIODevice.WriteOnly)
        feed.m_feedFavicon.save(tempBuffer, "PNG")  # Write pixmap into bytes in PNG format

        # Write feed image to a buffer
        imageBytes = QtCore.QByteArray()
        tempImageBuffer = QtCore.QBuffer(imageBytes)
        tempImageBuffer.open(QtCore.QIODevice.WriteOnly)
        feed.m_feedImage.save(tempImageBuffer, "PNG")   # Write pixmap into bytes in PNG format

        queryObj = QtSql.QSqlQuery(self.db)

        # Note that feedid is not specified here.  Since feedid is the primary key, it's value is chosen by
        # SQLite to be a unique value.
        queryStr = "insert into feeds (parentid, name, title, description, language, url, added, lastupdated, " \
                   "webpagelink, favicon, image, lastpurged) " \
                   "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        queryObj.prepare(queryStr)

        queryObj.addBindValue(feed.m_parentId)
        queryObj.addBindValue(feed.m_feedName)
        queryObj.addBindValue(feed.m_feedTitle)
        queryObj.addBindValue(feed.m_feedDescription)
        queryObj.addBindValue(feed.m_feedLanguage)
        queryObj.addBindValue(feed.m_feedUrl)
        queryObj.addBindValue(dateToJulianDay(feed.m_feedDateAdded))
        queryObj.addBindValue(dateToJulianDay(feed.m_feedLastUpdated))
        queryObj.addBindValue(feed.m_feedWebPageLink)
        queryObj.addBindValue(faviconBytes)
        queryObj.addBindValue(imageBytes)
        queryObj.addBindValue(dateToJulianDay(feed.m_feedLastPurged))

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to add a feed: {}".format(sqlErr.text()))
            return

        # Retrieve the feed ID (it is set by SQLite when the row was created)
        queryObj.prepare("select last_insert_rowid();")
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to retrieve the last inserted row id: {}".format(sqlErr.text()))
            # Note that if an error occurs here, and we exit, the above-created row will still be present, thus
            # leaving the database in an inconsistent state.  But, without the rowid of the newly-created row,
            # we can't delete it!
            return None

        if queryObj.next():
            feedId = queryObj.record().value(0)
        else:
            self.reportError("Can't retrieve the last inserted row id.")
            # Note that if an error occurs here, and we exit, the above-created row will still be present, thus
            # leaving the database in an inconsistent state.  But, without the rowid of the newly-created row,
            # we can't delete it!
            return None

        # Create the corresponding FeedItemsTable for this feed
        self.createFeedItemsTable(feedId)
        feed.m_feedId = feedId
        return feed

    def deleteFeed(self, feedId):
        """ Deletes a feed.  This involves:
            1. Deleting the feed's feed item table
            2. Deleting the feed's ID from the feed table
            3. Removing the feed's ID from the feed order, stored in the globals table
        """
        self.deleteFeedItemsTable(feedId)

        queryObj = QtSql.QSqlQuery(self.db)
        queryStr = "delete from feeds where feedid=?"
        queryObj.prepare(queryStr)

        queryObj.addBindValue(feedId)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete a feed from the feed table: {}".format(sqlErr.text()))

        self.removeFeedFromFeedOrder(feedId)

    def updateFeedLastUpdatedField(self, feedId, lastUpdatedDate):
        """ Updates the last-updated field for the given feed. """
        queryObj = QtSql.QSqlQuery(self.db)

        # Determine number of unread items
        queryStr = "update feeds set lastupdated=? where feedid=?"
        queryObj.prepare(queryStr)
        queryObj.addBindValue(dateToJulianDay(lastUpdatedDate))
        queryObj.addBindValue(feedId)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to update the last-updated field: {}".format(sqlErr.text()))

    def updateFeedLastPurgedField(self, feedId, lastPurgedDate):
        """ Updates the last-purged field for the given feed. """
        queryObj = QtSql.QSqlQuery(self.db)

        # Determine number of unread items
        queryStr = "update feeds set lastpurged=? where feedid=?"
        queryObj.prepare(queryStr)
        queryObj.addBindValue(dateToJulianDay(lastPurgedDate))
        queryObj.addBindValue(feedId)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to update the last-purged field: {}".format(sqlErr.text()))

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


    def setFeedReadFlagAllItems(self, feedId, readFlag):
        """ Sets the read flag of all feed items in the given feed to the given value:
            readFlag:  True: read, False: unread. """
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "update {} set readflag=?".format(feedTableName)

        queryObj.prepare(queryStr)
        queryObj.addBindValue(1 if readFlag else 0)
        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to set the read flag for all feed items in feed {}: {}".format(feedId, sqlErr.text()))


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


    def getFeedItemsFromList(self, feedItemList):
        """ Returns a list of feed items, corresponding to the given feed item guids in feedItemList. """
        contentList = []
        self.beginTransaction()

        for feedItem in feedItemList:
            feedId = feedItem[0]
            guid = feedItem[1]
            result = self.getFeedItem(guid, feedId)

            if result is not None:
                contentList.append(result)

        self.endTransaction()
        return contentList


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

    def deleteFeedItemsByDate(self, feedId, targetDate, deleteUnreadItems):
        """ Deletes feed items in the given feed.
            :param feedId Feed ID in which to delete the items
            :param targetDate Items on this date and later will be deleted
            :param deleteUnreadItems If true, unread items in the target range will be included
        """
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)

        if deleteUnreadItems:
            queryStr = "delete from {} where pubdatetime<=?".format(feedTableName)
        else:
            queryStr = "delete from {} where pubdatetime<=? and readflag=1".format(feedTableName)
        queryObj.prepare(queryStr)

        queryObj.addBindValue(dateToJulianDay(targetDate))

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete feed items by date: {}".format(sqlErr.text()))

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
            self.reportError("Error when attempting to get feed item's read flag: {}, on feed {}".format(sqlErr.text(), feedId))
            return False

        bReturn = False
        if queryObj.next():
            readFlag = queryObj.record().value(0)
            bReturn = True if readFlag == 1 else False

        return bReturn

    def feedItemExists(self, feedId, guid):
        """ Returns True if the given feed item exists, False otherwise. """
        feedTableName = self.feedItemsTableName(feedId)

        queryObj = QtSql.QSqlQuery(self.db)
        queryStr = "select title from {} where guid=?".format(feedTableName)
        queryObj.prepare(queryStr)
        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to determine if a feed item exists: {}".format(sqlErr.text()))
            return False

        return queryObj.next()

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

    def deleteItemOfInterest(self, feedId, guid):
        """ Deletes an item of interest. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "delete from itemsofinterest where feedid=? and guid=?"

        queryObj.prepare(queryStr)
        queryObj.addBindValue(feedId)
        queryObj.addBindValue(guid)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when deleting an item of interest: {}".format(sqlErr.text()))

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

    def addFilteredWord(self, newWord):
        """ Adds a word to the language filter table. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "insert into filteredwords (word) values (?)"
        queryObj.prepare(queryStr)
        queryObj.addBindValue(newWord)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to add a new filtered word: {}".format(sqlErr.text()))

    def deleteFilteredWord(self, word):
        """ Deletes a word from the language filter table. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "delete from filteredwords where word=?"
        queryObj.prepare(queryStr)
        queryObj.addBindValue(word)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete a filtered word: {}".format(sqlErr.text()))

    def addFilteredWords(self, wordList):
        """ Adds multiple filtered words to the database. """
        self.beginTransaction()

        for word in wordList:
            self.addFilteredWord(word)

        self.endTransaction()

    def deleteFilteredWords(self, wordList):
        """ Deletes multiple filtered words from the database. """
        self.beginTransaction()

        for word in wordList:
            self.deleteFilteredWord(word)

        self.endTransaction()

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

    def addAdFilter(self, word):
        """ Adds an ad filter word to the database. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "insert into adfilters (word) values (?)"
        queryObj.prepare(queryStr)
        queryObj.addBindValue(word)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to add a new ad filter word: {}".format(sqlErr.text()))

    def deleteAdFilter(self, word):
        """ Deletes an ad filter word from the database. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "delete from adfilters where word=?"
        queryObj.prepare(queryStr)
        queryObj.addBindValue(word)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete an ad filter word: {}".format(sqlErr.text()))

    def addAdFilters(self, wordList):
        """ Adds a list of words to the ad filter in the database. """
        self.beginTransaction()

        for word in wordList:
            self.addAdFilter(word)

        self.endTransaction()

    def deleteAdFilters(self, wordList):
        """ Deletes multiple words from the ad filter in the database. """
        self.beginTransaction()

        for word in wordList:
            self.deleteAdFilter(word)

        self.endTransaction()

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

    def addFeedItemFilter(self, filter):
        """ Adds a feed item filter. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "insert into feeditemfilters "
        queryStr += "(feedid, field, verb, querystring, action) "
        queryStr += "values (?, ?, ?, ?, ?)"

        queryObj.prepare(queryStr)

        queryObj.addBindValue(filter.m_feedId)
        queryObj.addBindValue(filter.m_fieldId)
        queryObj.addBindValue(filter.m_verb)
        queryObj.addBindValue(filter.m_queryStr)
        queryObj.addBindValue(filter.m_action)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to add a feed item filter: {}".format(sqlErr.text()))

    def deleteFeedItemFilter(self, filterId):
        """ Deletes a filter. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "delete from feeditemfilters where filterid=?"

        queryObj.prepare(queryStr)

        queryObj.addBindValue(filterId)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to delete a feed item filter: {}".format(sqlErr.text()))

    def updateFeedItemFilter(self, filter):
        """ Updates all fields of a filter. """
        queryObj = QtSql.QSqlQuery(self.db)

        queryStr = "update feeditemfilters set "
        queryStr += "feedid=?, field=?, verb=?, querystring=?, action=? "
        queryStr += "where filterid=?"

        queryObj.prepare(queryStr)

        queryObj.addBindValue(filter.m_feedId)
        queryObj.addBindValue(filter.m_fieldId)
        queryObj.addBindValue(filter.m_verb)
        queryObj.addBindValue(filter.m_queryStr)
        queryObj.addBindValue(filter.m_action)
        queryObj.addBindValue(filter.m_filterId)

        queryObj.exec_()

        # Check for errors
        sqlErr = queryObj.lastError()
        if sqlErr.type() != QtSql.QSqlError.NoError:
            self.reportError("Error when attempting to update a feed item filter: {}".format(sqlErr.text()))

    def addFeedItemFilters(self, filterList):
        """ Adds the filters in filterList. """
        self.beginTransaction()

        for filter in filterList:
            self.addFeedItemFilter(filter)

        self.endTransaction()

    def updateFeedItemFilters(self, filterList):
        """ Updates the filters in filterIdList. """
        self.beginTransaction()

        for filter in filterList:
            self.updateFeedItemFilter(filter)

        self.endTransaction()

    def deleteFeedItemFilters(self, filterIdList):
        """ Deletes filters whose IDs are contained in filterItemList. """
        self.beginTransaction()

        for filterId in filterIdList:
            self.deleteFeedItemFilter(filterId)

        self.endTransaction()


    def setPocketUsernameAndAccessToken(self, username, accessToken):
        """ Sets the Pocket username and access token as global values. """
        self.setGlobalValue(kPocketUsernameKey, username)
        self.setGlobalValue(kPocketAccessToken, accessToken)

    def getPocketAccessToken(self):
        """ Returns the Pocket access token. """
        return self.getGlobalValue(kPocketAccessToken)

    def getPocketUsername(self):
        """ Returns the Pocket username. """
        return self.getGlobalValue(kPocketUsernameKey)

    def isPocketInitialized(self):
        """ Returns True if Pocket has been initialized.  This simply means that the Pocket access token has been
            obtained. """
        return self.globalValueExists(kPocketAccessToken)
