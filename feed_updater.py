from feed_item_parser import parseFeed
from feed_item_debugger import debugParseFeed
from resource_fetcher import ResourceFetcher

# Use DEBUG = True to invoke feed parse debugging
#DEBUG = True
DEBUG = False

class FeedUpdater:
    def __init__(self, db):
        super(FeedUpdater, self).__init__()
        self.db = db

    def updateFeed(self, feedId):
        """ Updates the given feed. """
        feed = self.db.getFeed(feedId)
        feedUrl = feed.m_feedUrl
        resourceFetcher = ResourceFetcher(feedUrl)
        feedText = resourceFetcher.getData()

        if DEBUG:
            debugParseFeed(feedText)
            return
        else:
            feedItemList = parseFeed(feedText)

        guids = self.db.getFeedItemGuids(feedId)
        noDuplicatesList = []

        for feedItem in feedItemList:
            if feedItem.m_guid not in guids:
                #print("Adding {} to the database.".format(feedItem.m_guid))
                noDuplicatesList.append(feedItem)
            else:
                print("GUID: {} already exists".format(feedItem.m_guid))

        self.db.addFeedItems(noDuplicatesList, feedId)
