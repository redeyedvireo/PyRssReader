
class FeedItem:
    def __init__(self):
        super(FeedItem, self).__init__()

        self.m_title = ""
        self.m_author = ""
        self.m_link = ""
        self.m_description = ""
        self.m_encodedContent = ""  # < content: encoded > tag sometimes contains the article
        self.m_categories = []
        self.m_publicationDatetime = None   # datetime (stored in database as a Julian Day, (eg, a Unix timestamp)
        self.m_thumbnailLink = ""
        self.m_thumbnailSize = None     # QSize
        self.m_guid = ""
        self.m_feedburnerOrigLink = ""  # TODO: Is this a Digg thing?

        self.m_enclosureLink = ""       # Link to media enclosure (e.g. podcast)
        self.m_enclosureLength = 0      # Length of enclosure item
        self.m_enclosureType = ""       # MIME type of enclosure (for ex.: "media/mpeg")

        self.m_parentFeedId = -1        # Feed ID that owns this feed item
        self.m_feedWebPageLink = ""     # URL of the feed item's web page.  This is not part of the feed item's XML,
                                        # but is taken from the feed.
                                        # TODO: This field will eventually be filled in by the feed item parser.  However,
                                        #       it will be necessary to modify the database structure to include this item,
                                        #       which means it will be necessary to add the database version update code.

        self.m_bRead = False            # True if feed item has been read

    def hasEnclosure(self):
        return len(self.m_enclosureLink) > 0

    def isRead(self):
        return self.m_bRead

    def getFeedItemText(self):
        """ Returns the text of the feed item. """
        feedItemText = ""
        if self.m_encodedContent:
            feedItemText = self.m_encodedContent
        else:
            feedItemText = self.m_description
        return feedItemText

    def isValid(self):
        return len(self.m_guid) > 0 and self.m_parentFeedId != -1
