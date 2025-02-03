from PySide6 import QtCore, QtGui
import datetime

kItemsOfInterestFeedId = 2147483647

class Feed(object):
    def __init__(self):
        super(Feed, self).__init__()

        # User data
        self.m_feedName = ""  # User-specified name of feed.  This is deprecated; use m_feedTitle.
        self.m_feedUrl = ""  # URL of the feed

        # Tracking info
        self.m_feedDateAdded = datetime.datetime(1990, 1, 1)  # Date / time feed was added (Indicate it has never been added)
        self.m_feedLastUpdated = datetime.datetime(1990, 1, 1)  # Date / time feed was last updated (Indicate it has never been updated)
        self.m_feedLastPurged = datetime.datetime(1990, 1, 1)  # Date / time feed was last purged (Indicate it has never been purged)

        # Data from feed XML
        self.m_feedTitle = ""  # Actual title, given by the feed data
        self.m_feedLanguage = ""
        self.m_feedDescription = ""
        self.m_feedWebPageLink = ""

        self.m_feedId = -1  # ID number of the feed
        self.m_parentId = -1  # Used in the feed tree

        self.m_feedFavicon = QtGui.QPixmap()        # Favicon for the feed's main web site (for display in feed tree)
        self.m_feedImage = QtGui.QPixmap()          # Image from the feed itself. This is generally not an icon.

    def isValid(self):
        """ Simplistic method to determine if a feed is valid.  (If it has no feed URL, it is not valid). """
        return len(self.m_feedUrl) > 0

    def getFeedIcon(self):
        returnPixmap = QtGui.QPixmap()

        if not isinstance(self.m_feedImage, str) and not self.m_feedImage.isNull():
            if isinstance(self.m_feedImage, QtCore.QByteArray):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(self.m_feedImage)
                self.m_feedImage = pixmap
            returnPixmap =  self.m_feedImage
        else:
            if isinstance(self.m_feedFavicon, QtCore.QByteArray):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(self.m_feedFavicon)
                self.m_feedFavicon = pixmap
            returnPixmap =  self.m_feedFavicon

        # Scale it to 32x32
        if not returnPixmap.isNull():
            returnPixmap = returnPixmap.scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)

        return returnPixmap

    def getFeedIconAsTextEncodedByteArray(self):
        """ Returns the feed icon as a base64-encoded string.  This is used when exporting a feed as XML. """
        pixmap = self.getFeedIcon()
        if pixmap is not None:
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)
            pixmap.save(buffer, "PNG")
            base64ByteArray = buffer.data().toBase64()
            testByteArray = base64ByteArray.data()

            base64ByteArrayStr = ""
            if type(testByteArray) is bytes:
                base64ByteArrayStr = testByteArray.decode('utf-8')
            else:
                # This should not happen.
                base64ByteArrayStr = str(base64ByteArray)

            return str(base64ByteArrayStr)
        else:
            return ""

    def feedName(self):
        if self.m_feedName:
            return self.m_feedName
        else:
            return self.m_feedTitle
