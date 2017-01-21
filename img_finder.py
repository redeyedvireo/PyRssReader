# Finds all <img> tags in a block of HTML.
from html.parser import HTMLParser


class ImgFinder(HTMLParser):
    def __init__(self, htmlText):
        super(ImgFinder, self).__init__()

        self.imgList = []
        self.feed(htmlText)

    def hasImages(self):
        return len(self.imgList) > 0

    def getImages(self):
        return self.imgList

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            #print("Found an image tag with attrs: {}".format(attrs))
            src = self.getImgSource(attrs)
            if len(src) > 0:
                self.imgList.append(src)

    def getImgSource(self, attrs):
        """ Returns the URL of an image, from its 'src' attribute. """
        src = ""
        for attr in attrs:
            if attr[0] == "src":
                src = attr[1]

        return src

