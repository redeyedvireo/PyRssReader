from enum import Enum, auto


class FilterField(Enum):
    eFieldNone = 0
    eFieldTitle = auto()
    eFieldAuthor = auto()
    eFieldDescription = auto()
    eFieldCategories = auto()

# This is also known as the "verb"
class FilterQuery(Enum):
    eQueryIgnore = 0
    eQueryContains = auto()
    eQueryDoesNotContain = auto()
    eQueryEquals = auto()
    eQueryRegularExpressionMatch = auto()   # Use a regular expression for the query string

class FilterAction(Enum):
    eActionDoNothing = 0
    eActionCopyToInterestFeed = auto()   # Copy feed item to the "Items of Interest" feed
    eActionMarkAsRead = auto()
    eActionDeleteFeedItem = auto()


class FeedItemFilter:
    def __init__(self):
        super(FeedItemFilter, self).__init__()

        self.m_filterId = 0
        self.m_feedId = 0       # Feed ID of filter( if 0, it is a global filter)
        self.m_fieldId = -1     # ID of field in DB to be queried
        self.m_verb = 0         # Specifies how to query the item
        self.m_queryStr = ""    # Query string(ie, string to search for , etc.)
        self.m_action = 0       # Action ID(ie, what to do with selected feed items)

    def __str__(self):
        return "ID: {} - {}".format(self.m_filterId, FeedItemFilter.StringifyFilter(self))

    @staticmethod
    def StringifyFilter(filter):
        filterStr = "When "

        # Field
        if filter.m_fieldId == FilterField.eFieldTitle.value:
            filterStr += "the title "
        elif filter.m_fieldId == FilterField.eFieldAuthor.value:
            filterStr += "the author "
        elif filter.m_fieldId == FilterField.eFieldDescription.value:
            filterStr += "the description "
        elif filter.m_fieldId == FilterField.eFieldCategories.value:
            filterStr += "the categories "
        else:
            return "INVALID FIELD"

        # Query (or verb)
        if filter.m_verb == FilterQuery.eQueryContains.value:
            filterStr += "contains "
        elif filter.m_verb == FilterQuery.eQueryDoesNotContain.value:
            filterStr += "does not contain "
        elif filter.m_verb == FilterQuery.eQueryEquals.value:
            filterStr += "exactly equals "
        elif filter.m_verb == FilterQuery.eQueryRegularExpressionMatch.value:
            filterStr += "matches regular expression "
        else:
            return "INVALID VERB"

        # Query string
        filterStr += '"{}"'.format(filter.m_queryStr)
        filterStr += ", "
        
        # Action
        if filter.m_action == FilterAction.eActionCopyToInterestFeed.value:
            filterStr += "mark it as an Item of Interest."
        elif filter.m_action == FilterAction.eActionMarkAsRead.value:
            filterStr += "mark it as read."
        elif filter.m_action == FilterAction.eActionDeleteFeedItem.value:
            filterStr += "delete it."
        else:
            return "INVALID ACTION"

        return filterStr


