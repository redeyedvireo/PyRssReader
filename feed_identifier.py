import logging
import datetime
from lxml import etree
from resource_fetcher import ResourceFetcher
from feed import Feed
from feed_item_parser import getElementValue
from urllib.parse import urlparse
from dateutil.relativedelta import *


class FeedIdentifier:
    def __init__(self, proxy):
        super(FeedIdentifier, self).__init__()
        self.proxy = proxy
        self.feed = None

    def identifyFeed(self, feedUrl):
        # TODO: This should probably be done in a thread
        resourceFetcher = ResourceFetcher(feedUrl, self.proxy)
        feedText = resourceFetcher.getData()

        self.feed = Feed()

        try:
            root = etree.fromstring(feedText)
        except Exception as inst:
            if len(feedText) > 50:
                feedTextToDisplay = "<Feed text too large>"
            else:
                feedTextToDisplay = feedText

            errMsg = "parseFeed: Exception: {} when parsing feed item text:\n{}".format(inst, feedTextToDisplay)
            print(errMsg)
            logging.error(errMsg)
            return self.feed

        channel = root.find('channel')

        if channel is None:
            # Some feeds use 'feed' instead of 'channel'
            channel = root.find('feed')

        # Some feeds (ahem, GOOGLE!) don't have a channel or feed tag
        if channel is not None:
            feedRoot = channel
        else:
            feedRoot = root

        self.feed.m_feedUrl = feedUrl
        self.feed.m_feedTitle = getElementValue(feedRoot, ['title'])
        self.feed.m_feedName = self.feed.m_feedTitle    # This field is deprecated, but is still being set
        self.feed.m_feedLanguage = getElementValue(feedRoot, ['language'])
        self.feed.m_feedDescription = getElementValue(feedRoot, ['description'])
        self.feed.m_feedWebPageLink = getElementValue(feedRoot, ['link'])
        self.feed.m_feedDateAdded = datetime.datetime.today()
        self.feed.m_feedLastUpdated = datetime.datetime(1990, 1, 1) # Indicate it has never been updated
        self.feed.m_feedLastPurged = datetime.datetime(1990, 1, 1)  # Indicate it has never been purged

        self.readFeedImage(feedRoot)

        if self.feed.m_feedImage.isNull():
            # The feed did not contain an image.  Try getting the favicon from the feed's web site.
            self.getWebsiteFavicon()

        return self.feed

    def readFeedImage(self, feedRoot):
        imageRoot = feedRoot.find('image')
        if imageRoot is not None:
            feedImageUrlElement = imageRoot.find('url')

            if feedImageUrlElement.text is not None:
                feedImageUrl = feedImageUrlElement.text

                resourceFetcher = ResourceFetcher(feedImageUrl, self.proxy)
                self.feed.m_feedImage = resourceFetcher.getDataAsPixmap()

    def getWebsiteFavicon(self):
        """ Attempts to retrieve the favicon from the feed's web site. """
        if self.feed.m_feedWebPageLink:
            parsed_uri = urlparse(self.feed.m_feedWebPageLink)
            faviconUrl = '{uri.scheme}://{uri.netloc}/favicon.ico'.format(uri=parsed_uri)
            resourceFetcher = ResourceFetcher(faviconUrl, self.proxy)
            self.feed.m_feedFavicon = resourceFetcher.getDataAsPixmap()
