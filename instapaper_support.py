import requests
import json
import webbrowser
import logging

from proxy import Proxy

class InstapaperSupport:
  def __init__(self, proxy=None):
    self.proxy: Proxy | None = proxy

    # These are stored as plain text in memory
    self.instapaperUsername: str = ""
    self.instapaperPassword: str = ""

  def initialize(self):
    """ Initializes the proxy headers. """
    pass

  @property
  def isAuthorized(self):
    return len(self.instapaperUsername) > 0 and len(self.instapaperPassword) > 0

  def usingProxy(self):
    return self.proxy.usesProxy() if self.proxy else False

  def saveArticle(self, url: str, title: str = "") -> bool:
    """ Saves an article to Instapaper.  Returns True if successful, or False if not. """
    apiUrl = 'https://www.instapaper.com/api/add'

    params = {
      "url": url,
      "title": title,
    }

    try:
      if self.proxy and self.proxy.usesProxy():
        response = requests.get(apiUrl, params=params, auth=(self.instapaperUsername, self.instapaperPassword), proxies=self.proxy.getProxyDict())
      else:
        response = requests.get(apiUrl, params=params, auth=(self.instapaperUsername, self.instapaperPassword))

      if response.status_code == 201:
        return True
      else:
        logging.error(f"[InstapaperSuppoart.saveArticle] Save article error: {response.status_code}: {response.text}")
        return False

    except requests.exceptions.ProxyError as err:
      logging.error(f'[InstapaperSupport.saveArticle] Proxy error: {err.args}')
      return False

    except Exception as inst:
      logging.error(f'[InstapaperSupport.saveArticle] Exception: type: {type(inst)}')
      logging.error(f'Exception args: {inst.args}')
      logging.error(f'Exception object: {inst}')
      return False

  def addArticleToInstapaper(self, url, title):
    """ Adds an article to Instapaper.  This is the function to use from outside this class to save articles.
        Returns True if successful, False otherwise. """
    return self.saveArticle(url, title)
