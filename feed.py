from PyQt5 import QtCore, QtGui

kItemsOfInterestFeedId = 2147483647

class Feed(object):
    def __init__(self):
        super(Feed, self).__init__()

        # User data
        self.m_feedName = ""  # User-specified name of feed.  This is deprecated; use m_feedTitle.
        self.m_feedUrl = ""  # URL of the feed

        # Tracking info
        self.m_feedDateAdded = None  # Date / time feed was added
        self.m_feedLastUpdated = None  # Date / time feed was last updated
        self.m_feedLastPurged = None  # Date / time feed was last purged

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
        if not isinstance(self.m_feedImage, str) and not self.m_feedImage.isNull():
            if isinstance(self.m_feedImage, QtCore.QByteArray):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(self.m_feedImage)
                self.m_feedImage = pixmap
            return self.m_feedImage
        else:
            if isinstance(self.m_feedFavicon, QtCore.QByteArray):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(self.m_feedImage)
                self.m_feedFavicon = pixmap
            return self.m_feedFavicon

    def getFeedIconAsTextEncodedByteArray(self):
        """ Returns the feed icon as a base64-encoded string.  This is used when exporting a feed as XML. """
        pixmap = self.getFeedIcon()
        if pixmap is not None:
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QIODevice.ReadWrite)
            pixmap.save(buffer, "PNG")
            base64ByteArray = buffer.data().toBase64()
            testByteArray = bytearray(base64ByteArray)
            base64ByteArrayStr = testByteArray.decode('utf-8')
            return str(base64ByteArrayStr)
        else:
            return ""

    def feedName(self):
        if self.m_feedName:
            return self.m_feedName
        else:
            return self.m_feedTitle
