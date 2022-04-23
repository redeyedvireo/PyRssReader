# Proxy settings

class Proxy:
    def __init__(self):
        self.proxyUrl = ""
        self.proxyPort = 0
        self.proxyUser = ""
        self.proxyPassword = ""

        self.proxyDict = { 'http': 'http://{}:{}@{}:{}/'.format(self.proxy.proxyUser, self.proxy.proxyPassword,
                                                            self.proxy.proxyUrl, self.proxy.proxyPort),
                            'https': 'https://{}:{}@{}:{}/'.format(self.proxy.proxyUser, self.proxy.proxyPassword,
                                                            self.proxy.proxyUrl, self.proxy.proxyPort) }

    def __str__(self):
        return "Host: {}, Port: {}, User: {}, Password: {}".format(self.proxyUrl, self.proxyPort, self.proxyUser, self.proxyPassword)

    def usesProxy(self):
        return len(self.proxyUrl) > 0
