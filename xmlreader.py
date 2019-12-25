from xml.dom import minidom
from xml.etree import ElementTree


file = "quotes.xml"


class XMLReader:
    def __init__(self):
        self.doc = ElementTree.parse(file).getroot()  # minidom.parse(file)

    def get_quotes(self, style, subcat):
        quote_tree = self.doc.find(style)
        quote_list = []
        for q in quote_tree.iter("q"):
            quote_list.append(q.text)

        return quote_list
