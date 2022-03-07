from PyQt5 import QtCore, QtGui, QtWebEngineWidgets

class CustomWebEnginePage(QtWebEngineWidgets.QWebEnginePage):
  def __init__(self, parent) -> None:
      super(CustomWebEnginePage, self).__init__(parent)
      webEngineSettings = self.settings()
      # webEngineSettings.setFontFamily('verdana')
      # webEngineSettings.setAttribute(QtWebEngineWidgets.QtWebEngineSettings.LocalContentCanAccessRemoteUrls, False)


  def acceptNavigationRequest(self, url,  _type, isMainFrame):
      if _type == QtWebEngineWidgets.QWebEnginePage.NavigationTypeLinkClicked:
          QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
          return False
      return super().acceptNavigationRequest(url,  _type, isMainFrame)
