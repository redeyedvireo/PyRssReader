from bs4 import BeautifulSoup, NavigableString
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

    def addFilterWord(self, newWord):
        """ Adds a word to the filter. """
        self.db.addFilteredWord(newWord)
        self.filteredWords.append(newWord)

    def filterString(self, inString):
        """ Filters the given string.  That is, any occurrence of a filtered word is replaced with ****. """
        filteredString = inString
        for filteredWord in self.filteredWords:
            filteredString = re.sub(r"\b{}\b".format(filteredWord), kReplacementString, filteredString, flags = re.IGNORECASE)
        return filteredString

    def filterHtml(self, htmlString):
        """ Performs language filtering on all the strings of the given HTML.  Only operates on the
            tags within the HTML that contain strings.  Does not touch the tags themselves.  Thus,
            even if HTML keywords, such as 'title', or 'body', are among the words to be filtered,
            the HTML structure will not be compromised. """
        soup = BeautifulSoup(htmlString, 'html.parser')

        navigableStrings = self.findAllNavigableStrings(soup)

        for navigableString in navigableStrings:
            newString = self.filterString(navigableString.string)
            navigableString.replace_with(newString)

        return soup.prettify()

    def findAllNavigableStrings(self, soup):
        navigableStrings = []

        for tag in soup.find_all():
            if len(tag.contents) == 1:
                if type(tag.contents[0]) is NavigableString:
                    navigableStrings.append(tag.contents[0])
            else:
                # Iterate through the elements of this tag
                for element in tag.contents:
                    if type(element) is NavigableString:
                        navigableStrings.append(element)

        return navigableStrings
