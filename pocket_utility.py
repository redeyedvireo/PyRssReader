# This is a utility to use to obtain the various keys and tokens required to be able to access Pocket.
# This is not meant to be part of the application.

# Actually, some of this will be required to be used in the application, as this must be done for every user.

import sys
import time
import requests
import json
import webbrowser

# The consumer key identifies this app
consumerKey = "70343-0b54f25bfe2f1e90688ea732"

redirectUri = "https://google.com"

requestToken = None

isAuthorized = False

accessToken = None
username = None


def obtainRequestToken(consumerKey, redirectUri):
    """ Obtain the request token.  Returns the request token, or None, if there was an error. """
    requestTokenRequestUrl = 'https://getpocket.com/v3/oauth/request'
    headers={'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}

    data = json.dumps({"consumer_key": consumerKey,
                       "redirect_uri": redirectUri})

    print("ObtainRequestToken: JSON data: {}".format(data))

    response = requests.post(requestTokenRequestUrl, headers=headers, data=data)

    if response.status_code == 200:
        responseJson = response.json()
        print("Response JSON: {}".format(responseJson))
        return responseJson['code']
    else:
        print("Error: {}: {}".format(response.status_code, response.text))


def obtainAuthorizationFromUserForTheApp(requestToken, redirectUri):
    # Provide authorization from the user, which involves going to the Pocket web site, with the request token.
    authorizationUrl = "https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}".format(requestToken, redirectUri)

    webbrowser.open_new(authorizationUrl)


def convertRequestTokenToPocketAccessToken(consumerKey, requestToken):
    """ Converts a request token to a Pocket access token.  Returns a tuple of the form: (username, accesstoken), or
        None, if an error occurs. """
    requestUrl = 'https://getpocket.com/v3/oauth/authorize'
    headers={'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}

    data = json.dumps({"consumer_key": consumerKey,
                      "code": requestToken})

    print("ConvertRequestTokenToPocketAccessToken: JSON data: {}".format(data))

    response = requests.post(requestUrl, headers=headers, data=data)

    if response.status_code == 200:
        responseJson = response.json()
        print("Response JSON: {}".format(responseJson))
        username = responseJson['username']
        accessToken = responseJson['access_token']
        return (username, accessToken)

    else:
        print("Error: {}: {}".format(response.status_code, response.text))
        return None



# Start
if requestToken is None:
    requestToken = obtainRequestToken(consumerKey, redirectUri)
print("Request token: {}".format(requestToken))


if not isAuthorized:
    obtainAuthorizationFromUserForTheApp(requestToken, redirectUri)
    isAuthorized = True

    # Sleep for 5 seconds, to give Pocket a chance to redirect
    time.sleep(5)

# This is quite a quandary.  The user must give access to the app.  Pocket signals that access has been given
# by redirecting to the redirectUri.  The problem is, the app has no way of knowing when or if this has occurred.
# In the PyRssReader app, it might be good to display a dialog with OK/Cancel buttons that the user can hit indicate
# that authorization was granted, or not.  When OK is hit, then can proceed with converting a request token into
# an access token.

if isAuthorized:
    result = convertRequestTokenToPocketAccessToken(consumerKey, requestToken)

    if result is not None:
        username = result[0]
        accessToken = result[1]
        print("User name: {}, access token: {}".format(username, accessToken))
