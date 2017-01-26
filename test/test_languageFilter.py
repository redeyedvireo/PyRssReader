from unittest import TestCase
from language_filter import LanguageFilter
from database import Database

FILTER_STRING_1 = "The quick brown fox jumps over the lazy dog."

class TestLanguageFilter(TestCase):
    def test_filterString(self):
        db = Database()
        languageFilter = LanguageFilter(db)
        languageFilter.filteredWords = ['quick', 'fox']
        filteredString = languageFilter.filterString(FILTER_STRING_1)
        self.assertEqual(filteredString, "The **** brown **** jumps over the lazy dog.")

    def test_filterString_2(self):
        """ Testing case sensitivity. """
        db = Database()
        languageFilter = LanguageFilter(db)
        languageFilter.filteredWords = ['quick', 'fox', 'the']
        filteredString = languageFilter.filterString(FILTER_STRING_1)
        self.assertEqual(filteredString, "**** **** brown **** jumps over **** lazy dog.")
