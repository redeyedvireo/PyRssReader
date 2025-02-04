from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets
import logging
from custom_web_engine_page import CustomWebEnginePage
from keyboard_handler import KeyboardHandler
from utility import getResourceFilePixmap, getResourceFileText

WEBURLTAG = "http://"
WEBURLTAGS = "https://"

class RssContentViewNew(QtWebEngineWidgets.QWebEngineView):
  # Emitted when the current feed item should be re-selected.  This is usually due to the language filter
  # being changed, which requires the current feed item to be re-read, and re-filtered.
  reselectFeedItemSignal = QtCore.Signal()
  urlHovered = QtCore.Signal(str, int)

  def __init__(self, parent, languageFilter, adFilter, imageCache, keyboardHandler: KeyboardHandler, proxy) -> None:
    super(RssContentViewNew, self).__init__(parent)

    self.languageFilter = languageFilter
    self.adFilter = adFilter
    self.keyboardHandler = keyboardHandler
    self.m_feedHeaderHtml = ""
    self.m_processedFeedContents = ""
    self.rawFeedContents = ""
    self.m_completeHtmlDocument = ''
    self.filteredTitle = ""             # Language-filtered title
    self.currentFeedItem = None
    self.currentFeed = None
    self.webPage = None
    self.hoveredLink = ''

    self.keyboardHandler.nextFeedSignal.connect(self.onNextFeed)
    self.keyboardHandler.previousFeedSignal.connect(self.onPreviousFeed)

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

    self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
    self.customContextMenuRequested.connect(self.onContextMenu)


  def eventFilter(self, obj, event):
      if obj == self:
          if event.type() == QtCore.QEvent.Type.KeyRelease:
              keyCode = event.key()
              self.keyboardHandler.handleKey(keyCode)
              return False

      return QtWebEngineWidgets.QWebEngineView.eventFilter(self, obj, event)


  def setProxy(self, proxy):
      self.proxy = proxy

  def setContents(self, feedItem, feed):
    """ Sets a feed item's HTML into the text browser. """
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

    self.webPage = CustomWebEnginePage(self)

    self.webPage.setHtml(self.m_processedFeedContents)

    settings = self.webPage.settings()
    settings.setFontFamily(QtWebEngineCore.QWebEngineSettings.FontFamily.StandardFont, 'Verdana')
    settings.setFontSize(QtWebEngineCore.QWebEngineSettings.FontSize.DefaultFontSize, 14)
    # settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.FontFamily.SansSerifFont, True)

    self.setPage(self.webPage)

    viewSettings = self.settings()
    viewSettings.setFontFamily(QtWebEngineCore.QWebEngineSettings.FontFamily.SansSerifFont, 'Verdana')

    # This is currently not used, but I'm leaving this hook in here in case it is needed in the future.
    #self.fixDocument()

    self.page().linkHovered.connect(self.onLinkHovered)

    # Set focus onto the content view, so that arrow keys will scroll the content view
    self.setFocus()

  def onLinkHovered(self, url):
    self.hoveredLink = url
    self.urlHovered.emit(url, 0)

  def onContextMenu(self, point):
    # menu = self.createStandardContextMenu()
    menu = QtWidgets.QMenu()
    # menu.addSeparator()

    if len(self.hoveredLink) > 0:
      menu.addAction("Copy link to clipboard", self.onCopyHoveredLinkToClipboard)

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
      if self.webPage is None:
          return

      self.webPage.toHtml(self.toHtmlCallback)

  def toHtmlCallback(self, html):
      clipboard = QtWidgets.QApplication.clipboard()
      clipboard.setText(html)

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

  def onCopyHoveredLinkToClipboard(self):
      clipboard = QtWidgets.QApplication.clipboard()
      clipboard.setText(self.hoveredLink)

  def runLanguageFilter(self):
    self.reselectFeedItemSignal.emit()

  def onNextFeed(self):
    pass

  def onPreviousFeed(self):
    pass
