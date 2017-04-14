from lxml import etree


class OpmlExporter:
    def __init__(self, db):
        super(OpmlExporter, self).__init__()
        self.db = db

    def export(self, filename):
        domTree = self.createDomTree()
        # Debug
        print("Exported: {}".format(etree.tostring(domTree)))
        outfile = open(filename, 'wb')
        domTree.write(outfile, pretty_print=True, encoding='UTF-8')
        outfile.close()

    def createDomTree(self):
        feeds = self.db.getFeeds()

        root = etree.Element('opml', version='1.0')
        doc = etree.ElementTree(root)

        head = etree.SubElement(root, 'head', title='RSS Feeds')

        body = etree.SubElement(root, 'body')

        for feed in feeds:
            feedImageAsStr = feed.getFeedIconAsTextEncodedByteArray()

            element = etree.SubElement(body, 'outline',
                                       description=feed.m_feedDescription,
                                       title=feed.m_feedTitle,
                                       xmlUrl=feed.m_feedUrl,
                                       htmlUrl=feed.m_feedWebPageLink,
                                       type="rss",
                                       version="RSS",
                                       language=feed.m_feedLanguage,
                                       image=feedImageAsStr)

        return doc

