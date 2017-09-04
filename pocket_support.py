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


    def __init__(self):
        self.requestToken = None
        self.isAuthorized = False
        self.accessToken = None
        self.username = None

    def obtainRequestToken(self):
        """ Obtain the request token. """
        requestUrl = 'https://getpocket.com/v3/oauth/request'

        data = json.dumps({"consumer_key": self.kConsumerKey,
                           "redirect_uri": self.kRedirectUri})

        response = requests.post(requestUrl, headers=self.kHeaders, data=data)

        if response.status_code == 200:
            responseJson = response.json()
            self.requestToken = responseJson['code']
        else:
            errorMessage = "Obtain request token error: {}: {}".format(response.status_code, response.text)
            print(errorMessage)
            logging.error(errorMessage)

    def obtainAuthorizationFromUserForTheApp(self):
        # Provide authorization from the user, which involves going to the Pocket web site, with the request token.
        authorizationUrl = "https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}".format(self.requestToken, self.kRedirectUri)

        webbrowser.open_new(authorizationUrl)

    def convertRequestTokenToPocketAccessToken(self):
        """ Converts a request token to a Pocket access token. """
        requestUrl = 'https://getpocket.com/v3/oauth/authorize'

        data = json.dumps({"consumer_key": self.kConsumerKey,
                           "code": self.requestToken})

        response = requests.post(requestUrl, headers=self.kHeaders, data=data)

        if response.status_code == 200:
            responseJson = response.json()
            self.username = responseJson['username']
            self.accessToken = responseJson['access_token']

        else:
            errorMessage = "Convert request token to access token error: {}: {}".format(response.status_code, response.text)
            print(errorMessage)
            logging.error(errorMessage)

    def addArticleToPocket(self, url, title):
        """ Adds an article to Pocket. """
        if self.accessToken is None:
            return

        requestUrl = 'https://getpocket.com/v3/add'

        data = json.dumps({'url': url,
                           'title': title,
                           'consumer_key': self.kConsumerKey,
                           'access_token': self.accessToken})

        response = requests.post(requestUrl, headers=self.kHeaders, data=data)

        if response.status_code == 200:
            responseJson = response.json()

        else:
            errorMessage = "Add article to Pocket error: {}: {}".format(response.status_code, response.text)
            print(errorMessage)
            logging.error(errorMessage)
