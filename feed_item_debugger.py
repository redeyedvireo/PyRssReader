from lxml import etree

def debugParseFeed(feedItemRawText):
    rawText = feedItemRawText

    root = etree.fromstring(rawText)

    # Debug saved parsed feed to disk
    #fileObj = open('feed-parsed.xml', 'w')
    #fileObj.write(etree.tostring(root, pretty_print=True).decode("utf-8"))
    #fileObj.close()

    print(etree.tostring(root, pretty_print=True).decode("utf-8"))

    print("Printing children...")
    for child in root:
        print(child.tag)

    #channel = root.find('channel')
    #items = channel.findall('item')
    print("Root: {}".format(root.tag))
    items = root.findall('item')

    print("All entries:")
    entries = root.iterfind("{*}entry")
    for entry in entries:
        print("Entry: {}".format(entry))

    if len(items) == 0:
        # Sometimes <entry> is used in place of <item>, but this is rare
        items = root.findall('entry')

    for item in items:
        print("Item: {}".format(item))
