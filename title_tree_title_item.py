from title_tree_view_item import TitleTreeViewItem

class TitleTreeTitleItem(TitleTreeViewItem):
    def __init__(self, originalText, displayText, bRead, feedId, guid):
        """ originalText is the original text from the feed.  This must be saved so that it
            can be filtered later, if the user changes the language filter. """
        TitleTreeViewItem.__init__(self, displayText, bRead, feedId, guid)

        self.originalText = originalText

    def setDisplayText(self, text):
        """ Sets the text that will be displayed in the widget.  This is generally the language-filtered
            version of the original text from the feed item. """
        self.setText(text)
