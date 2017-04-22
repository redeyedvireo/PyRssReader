from PyQt5 import QtCore, QtGui
from lxml import etree
from feed import Feed
import datetime


class OpmlImporter:
    def __init__(self, db):
        super(OpmlImporter, self).__init__()
        self.db = db
        self.feeds = []

    def importFeeds(self, filename):
        """ Imports feeds from the given OPML file. """
        infile = open(filename, 'rb')
        tree = etree.parse(infile)
        infile.close()

        self.feeds = []

        body = tree.find('body')
        if body is not None:
            outlines = body.findall('outline')
            print("Outlines:")
            for outline in outlines:
                feed = Feed()

                feed.m_feedUrl = outline.get("xmlUrl")
                feed.m_feedTitle = outline.get("title")
                feed.m_feedName = feed.m_feedTitle  # This field is deprecated, but is still being set
                feed.m_feedDescription = outline.get("description")
                feed.m_feedWebPageLink = outline.get("htmlUrl")
                feed.m_feedLanguage = outline.get("language")
                feed.m_feedDateAdded = datetime.datetime.today()  # Date / time feed was added
                feed.m_feedLastUpdated = datetime.datetime(1990, 1, 1) # Indicate it has never been updated
                feed.m_feedLastPurged = datetime.datetime(1990, 1, 1) # Indicate it has never been purged

                feedImageAsStr = outline.get("image")
                if feedImageAsStr is not None:
                    imageByteArray = QtCore.QByteArray.fromBase64(feedImageAsStr.encode())
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(imageByteArray)
                    feed.m_feedImage = pixmap

                self.feeds.append(feed)

        return self.feeds
