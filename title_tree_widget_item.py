from PyQt5 import QtCore, QtWidgets, QtGui

kFeedItemType = QtWidgets.QTreeWidgetItem.UserType + 1
kGroupItemType = kFeedItemType + 1

kEnclosureColumn = 0
kTitleColumn = 1
kDateColumn = 2
kCreatorColumn = 3
kTagsColumn = 4

# This must be updated to indicate the number of columns
kNumColumns = 5


class TitleTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, feedItem, parent):
        super(TitleTreeWidgetItem, self).__init__(parent, kFeedItemType)

        #self.m_feedItem = feedItem     # I don't think we'll need to store the entire feed item in this object

        self.m_date = feedItem.m_publicationDatetime    # Current datetime
        self.m_guid = feedItem.m_guid                   # Feed item's GUID, as a string
        self.m_feedId = feedItem.m_parentFeedId           # Feed to which this feed item belongs
        self.m_bRead = feedItem.m_bRead                 # True if the item has been read

        self.setText(kEnclosureColumn, "")


        if feedItem.hasEnclosure():
            self.setIcon(kEnclosureColumn, QtGui.QIcon(":/RssReader/Resources/Audio Enclosure.png"))

        #self.setText(kTitleColumn, CLanguageFilter::Instance()->FilterString(plainTitle))
        self.setText(kTitleColumn, feedItem.m_title)        # TODO: Use language filter, filter out HTML, etc.
        self.setText(kDateColumn, "{}".format(feedItem.m_publicationDatetime.strftime("%Y-%m-%d")))
        self.setText(kCreatorColumn, feedItem.m_author)
        self.setText(kTagsColumn, ",".join(feedItem.m_categories))

        self.setTextAlignment(kEnclosureColumn, QtCore.Qt.AlignLeft)
        self.setReadState(self.m_bRead)

    def setReadState(self, isRead):
        self.m_bRead = isRead

        for i in range(kNumColumns):
            itemFont = self.font(i)
            itemFont.setBold(not isRead)
            self.setFont(i, itemFont)

    def guid(self):
        return self.m_guid

    def feedId(self):
        return self.m_feedId
