from PyQt5 import QtGui

class Feed(object):
    # User data
    m_feedName = "" # User-specified name of feed
    m_feedUrl = ""  # URL of the feed

    # Tracking info
    m_feedDateAdded = None # Date / time feed was added
    m_feedLastUpdated = None # Date / time feed was last updated
    m_feedLastPurged = None # Date / time feed was last purged

    # Data from feed XML
    m_feedTitle = ""        # Actual title, given by the feed data
    m_feedLanguage = ""
    m_feedDescription = ""
    m_feedWebPageLink = ""

    m_feedFavicon = None # Favicon for the feed's main web site (for display in feed tree)
    m_feedImage = None    # Image from the feed itself. This is generally not an icon.

    m_feedId = -1       # ID number of the feed
    m_parentId = -1     # Used in the feed tree

    def __init__(self):
        super(Feed, self).__init__()

        self.m_feedFavicon = QtGui.QPixmap()
        self.m_feedImage = QtGui.QPixmap()
