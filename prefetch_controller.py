# This class manages the prefetching of images for the current feed.
#
# To start with, the algorithm is fairly simple:
#   - Start by prefetching images from the first 10 feed items.
#   - Pick a "trigger" item, which is the next-to-last of the 10 prefetched items;
#       when the trigger feed item is hit, pre-fetch images from the next 10 items.
#   - If the user jumps past the trigger, set the new location as the start of a new block
#       of 10 feed items to prefetch.
#   - If the user jumps backwards, prior to the start of the current block of 10 items, simply set this
#       as the start of a new block of 10, and prefetch them.
#
# Refinements to this will be made over time.  Such refinements will include:
#   - Keep track of which rows have been prefetched, in a list.  When a new block of 10 items is needed, check
#       this list to ensure rows are not prefetched more than once.
#   - Keep track of the direction of feed item navigation.  If the user navigates backwards, run the above algorithm
#       in the reverse direction.

class PrefetchController:

    def __init__(self):
        super(PrefetchController, self).__init__()
        self.prefetchRange = 10         # Number of feed items for which images are to be prefetched
        self.currentPrefetchTrigger = self.prefetchRange - 1    # When this row is selected, prefetch the next range
        self.rangeStart = 1     # Note that we don't need to prefetch the 0'th item, as that is the initially displayed item
        self.rangeEnd = self.prefetchRange - 1
        self.numRows = 0
        self.maxRow = 0
        self.currentSelectedRow = 0     # Row that is currently selected
        self.needToPrefetch = False

    def setNumRows(self, rows):
        self.numRows = rows
        self.maxRow = self.numRows - 1

        self.rangeStart = 1
        self.rangeEnd = self.prefetchRange - 1

        if self.maxRow < self.rangeEnd:
            self.rangeEnd = self.maxRow

        self.currentPrefetchTrigger = self.rangeEnd
        self.needToPrefetch = True      # Prefetch is needed after the number of rows has been determined

    def rowSelected(self, row):
        self.currentSelectedRow = row

        if self.currentSelectedRow >= self.currentPrefetchTrigger:
            # The user has navigated beyond the trigger.  Update the prefetch range, and set
            # the needToPrefetch flag.
            self.needToPrefetch = True
            if self.rangeEnd == self.maxRow:
                # At the end of the rows
                self.needToPrefetch = False
            else:
                # Compute new range to prefetch
                self.rangeStart = self.rangeEnd + 1
                self.rangeEnd = min(self.rangeEnd + self.prefetchRange, self.maxRow)
                self.currentPrefetchTrigger = self.rangeEnd

    def prefetchNeeded(self):
        """ Returns True if it is time to perform another prefetch. """
        return self.needToPrefetch

    def prefetchList(self):
        """ Returns the list of rows that are to be prefetched.  Calling this function
            resets the needToPrefetch flag. """
        self.needToPrefetch = False
        # Recall that with range(x, y), the last item is y-1.
        return list(range(self.rangeStart, self.rangeEnd+1))