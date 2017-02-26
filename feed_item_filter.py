

class FeedItemFilter:
    def __init__(self):
        super(FeedItemFilter, self).__init__()

        self.m_filterId = 0
        self.m_feedId = 0       # Feed ID of filter( if 0, it is a global filter)
        self.m_fieldId = -1     # ID of field in DB to be queried
        self.m_verb = 0         # Specifies how to query the item
        self.m_queryStr = ""    # Query string(ie, string to search for , etc.)
        self.m_action = 0       # Action ID(ie, what to do with selected feed items)
