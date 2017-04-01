from enum import Enum, auto
from bs4 import BeautifulSoup
import re
import logging
from feed_item_filter import FilterField
from feed_item_filter import FilterQuery
from feed_item_filter import FilterAction

from feed_item_filter import FeedItemFilter
from database import Database


class FeedItemFilterMatcher:
    def __init__(self, db):
        super(FeedItemFilterMatcher, self).__init__()
        self.db = db
        self.filterList = []

    def initialize(self):
        self.loadFiltersFromDb()

    def loadFiltersFromDb(self):
        """ Loads the filters from the database.  This should be done at app initialization time. """
        self.filterList = self.db.getFeedItemFilters()

    def filterFeedItems(self, feedId, feedItemList):
        """ Performs the filtering action on the feed item list. """
        for feedItem in feedItemList:
            self.testFeedItem(feedId, feedItem)

    def testFeedItem(self, feedId, feedItem):
        for filter in self.filterList:
            if self.filterMatch(filter, feedItem):
                self.doMatchAction(filter, feedId, feedItem)

    def filterMatch(self, filterItem, feedItem):
        """ Returns True if the filter item matches the given feed item. """
        matchFound = False

        if filterItem.m_fieldId == FilterField.eFieldTitle.value:
            feedText = feedItem.m_title
        elif filterItem.m_fieldId == FilterField.eFieldAuthor.value:
            feedText = feedItem.m_author
        elif filterItem.m_fieldId == FilterField.eFieldDescription.value:
            if feedItem.m_encodedContent:
                htmlBody = feedItem.m_encodedContent
            else:
                htmlBody = feedItem.m_description
            soup = BeautifulSoup(htmlBody, 'html.parser')
            feedText = soup.get_text()
        elif filterItem.m_fieldId == FilterField.eFieldCategories.value:
            feedText = ",".join(feedItem.m_categories)
        else:
            # Unknown filter
            logging.error("Unknown feed item filter field ID: {}".format(filterItem.m_fieldId))
            return False

        # See if the feed item is "matched" (or "selected")
        if filterItem.m_verb == FilterQuery.eQueryContains.value:
            matchFound = True if filterItem.m_queryStr.lower() in feedText.lower() else False
        elif filterItem.m_verb == FilterQuery.eQueryDoesNotContain.value:
            matchFound = False if filterItem.m_queryStr.lower() in feedText.lower() else True
        elif filterItem.m_verb == FilterQuery.eQueryEquals.value:
            matchFound = True if filterItem.m_queryStr == feedText else False
        elif filterItem.m_verb == FilterQuery.eQueryRegularExpressionMatch.value:
            matchFound = True if re.search(filterItem.m_queryStr, feedText) else False
        else:
            matchFound = False

        return matchFound

    def doMatchAction(self, filterItem, feedId, feedItem):
        """ Performs an action according to the filterItem. """
        if filterItem.m_action == FilterAction.eActionCopyToInterestFeed.value:
            self.db.addItemOfInterest(feedId, feedItem.m_guid)
        elif filterItem.m_action == FilterAction.eActionMarkAsRead.value:
            self.db.setFeedItemReadFlag(feedId, feedItem.m_guid, True)
        elif filterItem.m_action == FilterAction.eActionDeleteFeedItem.value:
            self.db.deleteFeedItem(feedId, feedItem.m_guid)

