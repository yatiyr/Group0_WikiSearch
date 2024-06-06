import xml.sax

from Settings import *

class XMLParser(xml.sax.ContentHandler):
    
    def __init__(self, pageProcessor, indexCreator):
        self.tag = ''
        self.title = ''
        self.text = ''
        self.page_processor = pageProcessor
        self.create_index = indexCreator

    def startElement(self,name,attrs):
        
        self.tag=name

    def endElement(self,name):

        if name=='page':
            
            print(Settings.pageNumber)
            
            Settings.idTitleMap[Settings.pageNumber]=self.title.lower()
            title, body, category, infobox, link, reference = self.page_processor.PageProcess(self.title, self.text)
            
            self.create_index.Index(title, body, category, infobox, link, reference)

            self.tag = ""
            self.title = ""
            self.text = ""

    def characters(self, content):
        
        if self.tag == 'title':
            self.title += content

        if self.tag == 'text':
            self.text += content        