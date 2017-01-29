from bs4 import BeautifulSoup, NavigableString

# Finds all <img> tags in a block of HTML.
from html.parser import HTMLParser

class ImgFinder:
    def __init__(self, htmlText):
        super(ImgFinder, self).__init__()

        self.imgList = []
        self.soup = BeautifulSoup(htmlText, 'html.parser')

        imageTags = self.soup.find_all('img')
        for tag in imageTags:
            self.imgList.append(tag.get('src'))

    def hasImages(self):
        return len(self.imgList) > 0

    def getImages(self):
        return self.imgList
