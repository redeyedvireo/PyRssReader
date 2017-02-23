from title_tree_view_item import TitleTreeViewItem

class TitleTreeCategoriesItem(TitleTreeViewItem):
    def __init__(self, categoryList, bRead, feedId, guid):
        categoryString = ", ".join(categoryList)
        TitleTreeViewItem.__init__(self, categoryString, bRead, feedId, guid)
