from bs4 import BeautifulSoup
import re
from exceptions import DbError

# Uses BeautifulSoup to filter ads out of the HTML.
# https://www.crummy.com/software/BeautifulSoup/bs4/doc


class AdFilter:
    def __init__(self, db):
        self.db = db
        self.filters = []

    def initialize(self):
        """ Performs initial read of filtered words from the database.  This should be called during
            application initialization time. """
        try:
            self.filters = self.db.getAdFilters()
        except DbError as e:
            print("AdFilter.initialize: {}".format(e.message))

    def filterHtml(self, htmlString):
        """ Performs ad filtering of the given HTML.  <img> and <a> tags are scanned to see if they
            contain references to any of the ad filter URLs from the database.  Any that do are removed
            from the document. """
        soup = BeautifulSoup(htmlString, 'html.parser')

        for filter in self.filters:
            # Do src's first (for <img> tags), because an anchor (which uses href) might contain an <img>
            for tag in soup.find_all(src=re.compile(filter)):
                tag.extract()

            for tag in soup.find_all(href=re.compile(filter)):
                tag.extract()

        return soup.prettify()
