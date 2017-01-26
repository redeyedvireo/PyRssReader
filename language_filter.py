import re
from exceptions import DbError

# Filtered words are replaced with this
kReplacementString = "****"

class LanguageFilter:
    def __init__(self, db):
        self.db = db
        self.filteredWords = []

    def initialize(self):
        """ Performs an initial read of filtered words.  This should be called during
            application initialization time. """
        try:
            self.filteredWords = self.db.getFilteredWords()
        except DbError as e:
            print("LanguageFilter.initialize: {}".format(e.message))

    def filterString(self, inString):
        """ Filters the given string.  That is, any occurrence of a filtered word is replaced
            with ****. """
        filteredString = inString
        for filteredWord in self.filteredWords:
            filteredString = re.sub(r"\b{}\b".format(filteredWord), kReplacementString, filteredString, flags = re.IGNORECASE)
        return filteredString
