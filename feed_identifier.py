import logging
import datetime
import feedparser
from lxml import etree
from proxy import Proxy
from resource_fetcher import ResourceFetcher
from feed import Feed
from feed_item_parser import getElementValue
from urllib.parse import urlparse
from dateutil.relativedelta import *


class FeedIdentifier:
    def __init__(self, proxy: Proxy):
        super(FeedIdentifier, self).__init__()
        self.proxy = proxy
        self.feed = None

    def identifyFeed(self, feedUrl):
        # Fetch the feed manually, since feedparser doesn't know about proxies.
        resourceFetcher = ResourceFetcher(feedUrl, self.proxy)
        feedText = resourceFetcher.getData()

        if feedText is None:
            return None

        try:
            parsedFeed = feedparser.parse(feedText)
        except Exception as inst:
            errMsg = f"parseFeed: Exception: {inst} when parsing feed item text:{feedText}"
            logging.error(errMsg)
            return None

        self.feed = Feed()

        if parsedFeed.bozo:
            exc = parsedFeed.bozo_exception
            logging.info(f'Got Bozo error in feed: exception type: {type(exc).__name__}')
            return self.feed

        self.feed.m_feedUrl = feedUrl
        self.feed.m_feedTitle = self.getFeedData(parsedFeed, 'title', 'Untitled Feed')
        self.feed.m_feedName = self.getFeedData(parsedFeed, 'title', 'Untitled Feed')    # This field is deprecated, but is still being set
        self.feed.m_feedLanguage = self.getFeedData(parsedFeed, 'language', 'en-US')
        self.feed.m_feedDescription = self.getFeedData(parsedFeed, 'description', 'Description not found')
        self.feed.m_feedWebPageLink = self.getFeedData(parsedFeed, 'link', '')
        self.feed.m_feedDateAdded = datetime.datetime.today()
        self.feed.m_feedLastUpdated = datetime.datetime(1990, 1, 1) # Indicate it has never been updated
        self.feed.m_feedLastPurged = datetime.datetime(1990, 1, 1)  # Indicate it has never been purged

        self.readFeedImage(parsedFeed)

        if self.feed.m_feedImage.isNull():
            # The feed did not contain an image.  Try getting the favicon from the feed's web site.
            self.getWebsiteFavicon()

        return self.feed

    def identifyFeedOLD(self, feedUrl):
        # TODO: This should probably be done in a thread
        resourceFetcher = ResourceFetcher(feedUrl, self.proxy)
        feedText = resourceFetcher.getData()

        self.feed = Feed()

        if feedText is None:
            return self.feed

        try:
            root = etree.fromstring(feedText, None)
        except Exception as inst:
            if len(feedText) > 50:
                feedTextToDisplay = "<Feed text too large>"
            else:
                feedTextToDisplay = feedText

            errMsg = "parseFeed: Exception: {} when parsing feed item text:\n{}".format(inst, feedTextToDisplay)
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

        self.readFeedImageOLD(feedRoot)

        if self.feed.m_feedImage.isNull():
            # The feed did not contain an image.  Try getting the favicon from the feed's web site.
            self.getWebsiteFavicon()

        return self.feed

    def getFeedData(self, parsedFeed, dataItemName, defaultValue):
        if dataItemName in parsedFeed.feed:
            return parsedFeed.feed.get(dataItemName)
        else:
            return defaultValue

    def readFeedImage(self, parsedFeed):
        if self.feed is None:
            return

        if 'image' in parsedFeed.feed:
            imageRoot = parsedFeed.feed.image
            feedImageUrl = imageRoot.href if 'href' in imageRoot else ''

            if feedImageUrl is not None:
                resourceFetcher = ResourceFetcher(feedImageUrl, self.proxy)
                self.feed.m_feedImage = resourceFetcher.getDataAsPixmap()

    def readFeedImageOLD(self, feedRoot):
        if self.feed is None:
            return

        imageRoot = feedRoot.find('image')
        if imageRoot is not None:
            feedImageUrlElement = imageRoot.find('url')

            if feedImageUrlElement.text is not None:
                feedImageUrl = feedImageUrlElement.text

                resourceFetcher = ResourceFetcher(feedImageUrl, self.proxy)
                self.feed.m_feedImage = resourceFetcher.getDataAsPixmap()

    def getWebsiteFavicon(self):
        """ Attempts to retrieve the favicon from the feed's web site. """
        if self.feed is None:
            return

        if self.feed.m_feedWebPageLink:
            parsed_uri = urlparse(self.feed.m_feedWebPageLink)
            faviconUrl = '{uri.scheme}://{uri.netloc}/favicon.ico'.format(uri=parsed_uri)
            resourceFetcher = ResourceFetcher(faviconUrl, self.proxy)
            self.feed.m_feedFavicon = resourceFetcher.getDataAsPixmap()
