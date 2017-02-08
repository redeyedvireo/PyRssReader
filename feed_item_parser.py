from lxml import etree
from lxml.etree import fromstring
import dateutil.parser
import datetime
from feed_item import FeedItem

# Dependencies:
# pip3 install lxml
# pip3 install python-dateutil


def parseFeed(feedItemRawText):
    """ Parses a feed item, from raw text received from the server.
        Returns a list of feedItem objects. """

    feedItemList = []

    rawText = feedItemRawText
    # TODO: Uncomment this if encoding errors occur (and delete the above line)
    #rawText = feedItemRawText.encode('utf-8')   # Not sure this is necessary

    # TODO: Need exception handling here.  If there is an error parsing the XML, just return an empty list
    root = etree.fromstring(rawText)
    channel = root.find('channel')
    items = channel.findall('item')

    if len(items) == 0:
        # Sometimes <entry> is used in place of <item>, but this is rare
        items = channel.findall('entry')

    for item in items:
        feedItem = FeedItem()

        feedItem.m_title = getElementValue(item, ['title'])
        feedItem.m_author = getElementValue(item, ['author', 'creator', 'dc:creator'])
        feedItem.m_link = getLink(item.find('link'))
        feedItem.m_description = item.find('description')
        feedItem.m_encodedContent = item.find('content')
        feedItem.m_categories = getCategories(item)
        feedItem.m_publicationDatetime = getPublicationDateTime(item)
        feedItem.m_guid = getElementValue(item, ['guid', 'id', 'link'])
        feedItem.m_thumbnailLink, width, height = getThumbnail(item)
        feedItem.m_enclosureLink, feedItem.m_enclosureLength, feedItem.m_enclosureType = getEnclosure(item)

        feedItemList.append(feedItem)

    return feedItemList

def getElementValue(element, nameList):
    """ Retrieves the text value of one of a list of element names.  nameList is the list of
        names to retrieve.  The way it works is: an attempt is made to retrieve the first element in nameList.
        If that name is not found, the next element will be checked.  If that element is not found, the next
        element is checked, etc.  If none of the elements are found, an empty string will be returned. """
    for name in nameList:
        elementList = element.iterfind("{}*{}{}".format('{', '}', name))
        if elementList is not None:
            for elt in elementList:
                value = elt.text.strip()
                if len(value) > 0:
                    return value

    # Not found
    return ""

def getLink(item):
    if item is None:
        return ""

    if 'href' in item.attrib:
        return item.attrib['href']
    else:
        return item.text

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
        enclosureUrl = enclosureElement.find('url')
        enclosureLength = getIntegerAttribute(enclosureElement, 'length', 0)
        enclosureType = getStringAttribute(enclosureElement, 'type', "")
    return (enclosureUrl, enclosureLength, enclosureType)

def getStringAttribute(element, attribute, defaultValue):
    if attribute in element.attrib:
        return element.attrib[attribute]
    else:
        return defaultValue

def getIntegerAttribute(element, attribute, defaultValue):
    if attribute in element.attrib:
        return int(element.attrib[attribute])
    else:
        return defaultValue
