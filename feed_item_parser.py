import logging
from lxml import etree
from lxml.etree import fromstring
import dateutil.parser
import datetime
from datetime import timezone
from feed_item import FeedItem
from PyQt5 import QtCore

# Dependencies:
# pip3 install lxml
# pip3 install python-dateutil


def parseFeed(feedItemRawText):
    """ Parses a feed item, from raw text received from the server.
        Returns a list of feedItem objects. """

    # Debug: save feed to disk
    #fileObj = open('feed.xml', 'w')
    #fileObj.write(feedItemRawText.decode('utf-8'))
    #fileObj.close()

    feedItemList = []

    rawText = feedItemRawText
    # TODO: Uncomment this if encoding errors occur (and delete the above line)
    #rawText = feedItemRawText.encode('utf-8')   # Not sure this is necessary

    # TODO: Need exception handling here.  If there is an error parsing the XML, just return an empty list
    try:
        root = etree.fromstring(rawText)
    except Exception as inst:
        if len(rawText) > 50:
            feedTextToDisplay = "<Feed text too large>"
        else:
            feedTextToDisplay = rawText

        errMsg = "parseFeed: Exception: {} when parsing feed item text:\n{}".format(inst, feedTextToDisplay)
        print(errMsg)
        logging.error(errMsg)
        return []

    # Debug saved parsed feed to disk
    #fileObj = open('feed-parsed.xml', 'w')
    #fileObj.write(etree.tostring(root, pretty_print=True).decode("utf-8"))
    #fileObj.close()

    channel = root.find('channel')

    # Some feeds (ahem, GOOGLE!) don't have a channel tag
    if channel is not None:
        feedItemParent = channel
    else:
        feedItemParent = root

    # Note: can't use findall() to find tags, because this will ignore namespaced items.  Must use iterfind()
    #items = feedItemParent.iterfind("{*}item")
    items = feedItemParent.findall("{*}item")
    #testItems = feedItemParent.findall("{*}item")

    # Test if any items were found
    itemsFound = False
    for item in items:
        itemsFound = True

        # Since items is a generator, by attempting to iterate, we've moved past the first item.  To
        # reset, we must issue the iterfind() call again.
        #items = feedItemParent.iterfind("{*}item")
        break

    if not itemsFound:
        # Sometimes <entry> is used in place of <item>, but this is rare
        #items = feedItemParent.iterfind("{*}entry")
        items = feedItemParent.findall("{*}entry")

    for item in items:
        feedItem = FeedItem()

        feedItem.m_title = getElementValue(item, ['title'])
        feedItem.m_author = getElementValue(item, ['author', 'creator', 'dc:creator'])
        feedItem.m_link = getLink(item)
        feedItem.m_description = getElementValue(item, ['description'])
        feedItem.m_encodedContent = getElementValue(item, ['content', 'encoded'])
        feedItem.m_categories = getCategories(item)
        feedItem.m_publicationDatetime = getPublicationDateTime(item)
        feedItem.m_guid = getElementValue(item, ['guid', 'id', 'link'])
        feedItem.m_thumbnailLink, width, height = getThumbnail(item)
        feedItem.m_thumbnailSize = QtCore.QSize(width, height)
        feedItem.m_enclosureLink, feedItem.m_enclosureLength, feedItem.m_enclosureType = getEnclosure(item)

        feedItemList.append(feedItem)

    return feedItemList

def getElementValue(element, nameList):
    """ Retrieves the text value of one of a list of element names.  nameList is the list of
        names to retrieve.  The way it works is: an attempt is made to retrieve the first element in nameList.
        If that name is not found, the next element will be checked.  If that element is not found, the next
        element is checked, etc.  If none of the elements are found, an empty string will be returned. """
    for name in nameList:
        elementList = element.iterfind("{{*}}{}".format(name))
        if elementList is not None:
            for elt in elementList:
                if elt.text is not None:
                    value = elt.text.strip()
                    if len(value) > 0:
                        return value

    # Not found
    return ""

def getLink(item):
    if item is None:
        return ""

    elementList = item.iterfind("{{*}}{}".format('link'))
    if elementList is not None:
        for elt in elementList:
            if 'href' in elt.attrib:
                return elt.attrib['href']
            else:
                if elt.text is not None:
                    value = elt.text.strip()
                    if len(value) > 0:
                        return value

    logging.error("Can't find link element in {}".format(str(item)))
    return ""

def getCategories(item):
    """ Returns all categories as a list. """
    categories = []
    categoryElementList = item.findall('category')
    for element in categoryElementList:
        categories.append(element.text)
    return categories

def getPublicationDateTime(item):
    """ Returns the publication datetime as a datetime object. """
    pubDateTime = datetime.datetime.now()
    dateElement = item.find('pubDate')
    if dateElement is None:
        dateElement = item.find('updated')
    if dateElement is None:
        dateElement = item.find('date')

    if dateElement is not None:
        pubDateTime = dateutil.parser.parse(dateElement.text)

    # Make sure pubDateTime is an "aware" datetime; ie, that it has a timezone.
    if pubDateTime.tzinfo is None or pubDateTime.tzinfo.utcoffset(pubDateTime):
        pubDateTime = pubDateTime.replace(tzinfo=timezone.utc)
    return pubDateTime

def getThumbnail(item):
    """ Returns the thumbnail URL as a string, and the size as a tuple of the form: (imageURL, width, height). """
    imageUrl = ""
    imageWidth = 0
    imageHeight = 0

    thumbnailElement = item.find('thumbnail')
    if thumbnailElement is not None:
        imageUrl = thumbnailElement.text.strip()
        imageWidth = getIntegerAttribute(thumbnailElement, 'width', 0)
        imageHeight = getIntegerAttribute(thumbnailElement, 'height', 0)

    return (imageUrl, imageWidth, imageHeight)

def getEnclosure(item):
    """ Returns the enclosure data, if it exists.  Returns a tuple of the form: (url, length, type).  If there
        is no enclosure, url and type will be the empty string, and length will be 0. """
    enclosureUrl = ""
    enclosureLength = 0
    enclosureType = ""

    enclosureElement = item.find('enclosure')
    if enclosureElement is not None:
        enclosureUrl = getStringAttribute(enclosureElement, 'url', "")
        enclosureLength = getIntegerAttribute(enclosureElement, 'length', 0)
        enclosureType = getStringAttribute(enclosureElement, 'type', "")
    return (enclosureUrl, enclosureLength, enclosureType)

def getStringAttribute(element, attribute, defaultValue):
    if attribute in element.attrib:
        return element.attrib[attribute]
    else:
        return defaultValue

def getIntegerAttribute(element, attribute, defaultValue):
    returnValue = defaultValue
    if attribute in element.attrib:
        valueStr = element.attrib[attribute]
        if len(valueStr) > 0:
            returnValue = int(valueStr)
    return returnValue
