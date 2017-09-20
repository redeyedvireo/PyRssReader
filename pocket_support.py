import requests
import json
import webbrowser
import logging


class PocketSupport:
    kHeaders = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}

    # The consumer key identifies this app
    kConsumerKey = "70343-0b54f25bfe2f1e90688ea732"

    # Although Pocket uses this URL when authenticating, the code does not need to know that
    # the redirect happened.
    kRedirectUri = "https://google.com"


    def __init__(self, db, proxy):
        self.db = db
        self.proxy = proxy
        self.proxyDict = None
        self.requestToken = None
        self.isAuthorized = False
        self.accessToken = None
        self.username = None

    def initialize(self):
        """ Initializes the proxy headers. """
        if self.proxy.usesProxy():
            self.proxyDict = { 'http' : 'http://{}:{}@{}:{}/'.format(self.proxy.proxyUser, self.proxy.proxyPassword,
                                                                     self.proxy.proxyUrl, self.proxy.proxyPort),
                               'https' : 'https://{}:{}@{}:{}/'.format(self.proxy.proxyUser, self.proxy.proxyPassword,
                                                                       self.proxy.proxyUrl, self.proxy.proxyPort) }

    def usingProxy(self):
        if self.proxyDict is not None:
            return True
        else:
            return False

    def obtainRequestToken(self):
        """ Obtain the request token.  Returns True if successful, or False if not. """
        requestUrl = 'https://getpocket.com/v3/oauth/request'

        data = json.dumps({"consumer_key": self.kConsumerKey,
                           "redirect_uri": self.kRedirectUri})

        if self.usingProxy():
            response = requests.post(requestUrl, headers=self.kHeaders, data=data, proxies=self.proxyDict)
        else:
            response = requests.post(requestUrl, headers=self.kHeaders, data=data)

        if response.status_code == 200:
            responseJson = response.json()
            self.requestToken = responseJson['code']
            return True
        else:
            errorMessage = "Obtain request token error: {}: {}".format(response.status_code, response.text)
            print(errorMessage)
            logging.error(errorMessage)
            return False

    def obtainAuthorizationFromUserForTheApp(self):
        # Provide authorization from the user, which involves going to the Pocket web site, with the request token.
        authorizationUrl = "https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}".format(self.requestToken, self.kRedirectUri)

        webbrowser.open_new(authorizationUrl)

    def obtainAccessToken(self):
        """ Converts a request token to a Pocket access token.  Returns True if successful, or False if not. """
        requestUrl = 'https://getpocket.com/v3/oauth/authorize'

        data = json.dumps({"consumer_key": self.kConsumerKey,
                           "code": self.requestToken})

        if self.usingProxy():
            response = requests.post(requestUrl, headers=self.kHeaders, data=data, proxies=self.proxyDict)
        else:
            response = requests.post(requestUrl, headers=self.kHeaders, data=data)

        if response.status_code == 200:
            responseJson = response.json()
            self.username = responseJson['username']
            self.accessToken = responseJson['access_token']
            return True

        else:
            errorMessage = "Convert request token to access token error: {}: {}".format(response.status_code, response.text)
            print(errorMessage)
            logging.error(errorMessage)
            return False

    def saveArticle(self, url, title):
        """ Adds an article to Pocket.  Returns True if successful, False otherwise. """
        if self.accessToken is None:
            return False

        requestUrl = 'https://getpocket.com/v3/add'

        data = json.dumps({'url': url,
                           'title': title,
                           'consumer_key': self.kConsumerKey,
                           'access_token': self.accessToken})

        if self.usingProxy():
            response = requests.post(requestUrl, headers=self.kHeaders, data=data, proxies=self.proxyDict)
        else:
            response = requests.post(requestUrl, headers=self.kHeaders, data=data)

        if response.status_code == 200:
            responseJson = response.json()
            return True

        else:
            errorMessage = "Add article to Pocket error: {}: {}".format(response.status_code, response.text)
            print(errorMessage)
            logging.error(errorMessage)
            return False

    def addArticleToPocket(self, url, title):
        """ Adds an article to Pocket.  This is the function to use from outside this class to save articles.
            The class expects that the Pocket access token has been saved in the database; the class, by itself,
            cannot completely retrieve the access token, because there will need to be a UI component that asks
            the user to indicate that the request was granted.
            Returns True if successful, False otherwise. """
        if self.accessToken is None:
            self.accessToken = self.db.getPocketAccessToken()
        return self.saveArticle(url, title)

    def doStepOneOfAuthorization(self):
        """ Performs step 1 of authorization, which is to obtain the request token, and to show the Pocket web page for
            authorization.  Returns True if no error occurs.
            If this function returns True, the application should display a dialog box asking if the redirect web page
            has appeared (which, currently, is the Google serach page.)  If the user clicks Yes, it is OK to proceed
            to step 2 of authorization (obtaining the access token). """
        if not self.obtainRequestToken():
            return False

        self.obtainAuthorizationFromUserForTheApp()
        return True

    def doStepTwoOfAuthorization(self):
        """ Performs step 2 of authorization, which is to obtain the access token.  Returns True if successful,
            or False if not. """
        if self.obtainAccessToken():
            self.db.setPocketUsernameAndAccessToken(self.username, self.accessToken)
            return True
        else:
            return False

