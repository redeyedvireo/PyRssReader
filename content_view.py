import logging
import os, os.path
from PyQt5 import QtCore, QtGui, QtWidgets


class RssContentView(QtCore.QObject):
    def __init__(self, textBrowser):
        super(RssContentView, self).__init__()

        self.m_css = ""
        self.m_feedHeaderHtml = ""
        self.m_processedFeedContents = ""

        self.textBrowser = textBrowser
        QtCore.QTimer.singleShot(0, self.initialize)

    def initialize(self):
        self.m_css = self.getResourceFileText("pagestyle.css")
        self.m_feedHeaderHtml = self.getResourceFileText("feedHeader.html")

        # Replace carriage returns and line feeds with spaces
        self.m_css = self.m_css.replace("\r", "").replace("\n", "")
        self.m_feedHeaderHtml = self.m_feedHeaderHtml.replace("\r", "").replace("\n", "")

        doc = self.textBrowser.document()

        doc.setDefaultStyleSheet(self.m_css)

        # InitAdBlockList()

    # TODO: This should go in a utility file.
    def getResourceFileText(self, filename):
        scriptDir = os.getcwd()
        filePath = os.path.join(scriptDir, "Resources", filename)

        file = open(filePath, 'r')
        contents = file.read()
        file.close()

        return contents

    def setContents(self, feedItem):
        """ Sets a feed item's HTML into the text browser. """
        # Title
        # TODO: use language filter on the title
        strTitleLink = self.m_feedHeaderHtml.replace("%1", feedItem.m_link).replace("%2", feedItem.m_title)

        # TODO: use language filter on the body
        htmlBody = ""
        if feedItem.m_encodedContent:
            htmlBody = feedItem.m_encodedContent
        else:
            htmlBody = feedItem.m_description

        # TODO: Find image names
        self.m_processedFeedContents = "{}<body>{}</body>".format(strTitleLink, htmlBody)

        self.textBrowser.setHtml(self.m_processedFeedContents)