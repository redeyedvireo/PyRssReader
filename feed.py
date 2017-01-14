from PyQt5 import QtGui

class Feed(object):
    def __init__(self):
        super(Feed, self).__init__()

        # User data
        self.m_feedName = ""  # User-specified name of feed
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

        self.m_feedFavicon = None  # Favicon for the feed's main web site (for display in feed tree)
        self.m_feedImage = None  # Image from the feed itself. This is generally not an icon.

        self.m_feedId = -1  # ID number of the feed
        self.m_parentId = -1  # Used in the feed tree

        self.m_feedFavicon = QtGui.QPixmap()
        self.m_feedImage = QtGui.QPixmap()
