from urllib.request import Request, urlopen

class ResourceFetcher(object):
    def __init__(self, url):
        super(ResourceFetcher, self).__init__()
        self.request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        self.data = urlopen(self.request).read()

    def getData(self):
        return self.data
