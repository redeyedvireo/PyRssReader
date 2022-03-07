from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import logging
from custom_web_engine_page import CustomWebEnginePage

from utility import getResourceFilePixmap, getResourceFileText

WEBURLTAG = "http://"
WEBURLTAGS = "https://"

class RssContentViewNew(QtWebEngineWidgets.QWebEngineView):
  # Emitted when the current feed item should be re-selected.  This is usually due to the language filter
  # being changed, which requires the current feed item to be re-read, and re-filtered.
  reselectFeedItemSignal = QtCore.pyqtSignal()
  urlHovered = QtCore.pyqtSignal(str, int)

  def __init__(self, parent, languageFilter, adFilter, imageCache, keyboardHandler, proxy) -> None:
    super(RssContentViewNew, self).__init__(parent)

    self.languageFilter = languageFilter
    self.adFilter = adFilter
    self.m_feedHeaderHtml = ""
    self.m_processedFeedContents = ""
    self.rawFeedContents = ""
    self.m_completeHtmlDocument = ''
    self.filteredTitle = ""             # Language-filtered title
    self.currentFeedItem = None
    self.currentFeed = None

    QtCore.QTimer.singleShot(0, self.initialize)


  def initialize(self):
    self.m_css = getResourceFileText("pagestyle.css")
    self.m_feedHeaderHtml = getResourceFileText("feedHeader.html")
    self.m_completeHtmlDocument = getResourceFileText("completeHtmlDocument.html")

    # Replace carriage returns and line feeds with spaces
    self.m_css = self.m_css.replace("\r", "").replace("\n", "")
    self.m_feedHeaderHtml = self.m_feedHeaderHtml.replace("\r", "").replace("\n", "")
    self.m_completeHtmlDocument = self.m_completeHtmlDocument.replace("\r", "").replace("\n", "")

    self.setStyleSheet(self.m_css)

    self.dummyImage = QtGui.QPixmap(10, 10)
    self.dummyImage.fill()      # Fill it with white
    self.starImageForDebugging = getResourceFilePixmap("star.png")

    self.installEventFilter(self)

    self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.customContextMenuRequested.connect(self.onContextMenu)


  def eventFilter(self, obj, event):
      if obj == self:
          if event.type() == QtCore.QEvent.KeyRelease:
              keyCode = event.key()
              self.keyboardHandler.handleKey(keyCode)
              return False

      return QtWebEngineWidgets.QWebEngineView.eventFilter(self, obj, event)


  def setProxy(self, proxy):
      self.proxy = proxy

  def setContents(self, feedItem, feed):
    """ Sets a feed item's HTML into the text browser. """
    print(f"Setting contents for {feedItem.m_title}")
    self.currentFeedItem = feedItem
    self.currentFeed = feed

    # Title
    self.filteredTitle = self.languageFilter.filterString(feedItem.m_title)
    strTitleLink = self.m_feedHeaderHtml.replace("%1", feedItem.m_link).replace("%2", self.filteredTitle)

    htmlBody = feedItem.getFeedItemText()
    self.rawFeedContents = htmlBody

    # Create an HTML body
    if "<body>" not in htmlBody:
      newBody = self.m_completeHtmlDocument.format(strTitleLink, htmlBody)
      self.m_processedFeedContents = newBody
    else:
      logging.info("setContents: Error - feed item contained complete HTML.  GUID: {}".format(feedItem.m_guid))
      # TODO: Need to add the strTitleLink
      self.m_processedFeedContents = htmlBody

    self.m_processedFeedContents = self.languageFilter.filterHtml(self.m_processedFeedContents)
    self.m_processedFeedContents = self.adFilter.filterHtml(self.m_processedFeedContents)
    # self.m_processedFeedContents = self.fixHtml(self.m_processedFeedContents)

    webPage = CustomWebEnginePage(self)
  
    webPage.setHtml(self.m_processedFeedContents)

    self.setPage(webPage)

    # This is currently not used, but I'm leaving this hook in here in case it is needed in the future.
    #self.fixDocument()

    self.page().linkHovered.connect(self.onLinkHovered)

    # Set focus onto the content view, so that arrow keys will scroll the content view
    self.setFocus()

  @QtCore.pyqtSlot('QString')
  def onLinkHovered(self, url):
    self.urlHovered.emit(url, 0)

  @QtCore.pyqtSlot('QPoint')
  def onContextMenu(self, point):
    print("Context menu requested")
    # menu = self.createStandardContextMenu()
    menu = QtWidgets.QMenu()
    # menu.addSeparator()

    if self.hasSelection():
      selText = self.selectedText()
      menu.addAction("Add {} to language filter".format(selText), self.onAddToFilter)
      menu.addAction("Search for {} in Google".format(selText), self.onSearchGoogle)
      menu.addAction("Search for {} in Wikipedia".format(selText), self.onSearchWikipedia)

      menu.addSeparator()

    menu.addAction("Copy feed item source to clipboard", self.onCopyWebSource)
    menu.addAction("Copy raw feed item source to clipboard", self.onCopyRawFeedItemSource)
    menu.addAction("Rerun language filter", self.runLanguageFilter)

    menu.exec(self.mapToGlobal(point))

  def onCopyWebSource(self):
      clipboard = QtWidgets.QApplication.clipboard()
      clipboard.setText(self.toHtml())

  def onCopyRawFeedItemSource(self):
      clipboard = QtWidgets.QApplication.clipboard()
      clipboard.setText(self.rawFeedContents)

  def onAddToFilter(self):
      selText = self.selectedText()

      if selText:
          self.languageFilter.addFilterWord(selText)
          self.reselectFeedItemSignal.emit()
          # TODO: I think the entire feed should be reselected, so that the title tree gets reloaded.  But, must
          #       ensure that this feed item also is reselected, to ensure continuity of experience for the user.

  def onSearchGoogle(self):
      selText = self.selectedText()

      if selText:
          urlStr = "http://www.google.com/search?q={}".format(selText.strip().replace(" ", "+"))
          QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlStr))

  def onSearchWikipedia(self):
      selText = self.selectedText()

      if selText:
          urlStr = "http://en.wikipedia.org/wiki/{}".format(selText.strip().replace(" ", "_"))
          QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlStr))

  def runLanguageFilter(self):
    self.reselectFeedItemSignal.emit()
