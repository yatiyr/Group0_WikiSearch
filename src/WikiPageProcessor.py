import Preprocessor

from Settings import *
'''
In the data dump, Wiki Pages consists of:

    - Title
    - Body
    - Category
    - Infobox
    - Link
    - Reference

parts. This class
'''
class WikiPageProcessor():
    def __init__(self, preprocessor):
        self.PP = preprocessor

    def Title(self, title):
        result = self.PP.preprocess_text(title)
        return result
    
    # Taken from 
    #
    # https://medium.com/analytics-vidhya/search-engine-in-python-from-scratch-c3f7cc453250
    def Infobox(self, text):
        result = []
        # We try to remove {{Infobox parts from the text
        try:
            text = text.split('\n')
            i = 0
            while '{{Infobox' not in text[i]:
                i += 1
            
            data = []
            data.append(text[i].replace('{{Infobox', ' '))
            i += 1

            while text[i] != '}}':
                if '{{Infobox' in text[i]:
                    replaced = text[i].replace('{{Infobox', ' ')
                    data.append(replaced)
                else:
                    data.append(text[i])
                i += 1

            infobox = ' '.join(data)

            result = self.PP.preprocess_text(infobox)
        except:
            pass

        return result
    
    def Body(self, text):

        result = []
        result = self.PP.preprocess_text(text, True)

        return result
    
    def Category(self, text):
        result = []

        try:
            text = text.split('\n')
            i = 0
            while not text[i].startswith('[[Category:'):
                i += 1

            data = []
            data.append(text[i].replace('[[Category:', ' ').replace(']]', ' '))
            i += 1

            while text[i].endswith(']]'):
                replaced = text[i].replace('[[Category:', ' ').replace(']]', ' ')
                data.append(replaced)
                i += 1

            category = ' '.join(data)
            result = self.PP.preprocess_text(category)
        except:
            pass

        return result
    
    def Links(self, text):
        result = []
        
        try:
            links = ''
            text = text.split("==External links==")

            if len(text) > 1:
                text = text[1].split("\n")[1:]
                for txt in text:
                    if txt == "":
                        break
                    if txt[0] == "*":
                        splittedText = txt.split(' ')
                        link = [word for word in splittedText if "http" not in word]
                        link = " ".join(link)
                        links += ' ' + link

            result = self.PP.preprocess_text(links)
        except:
            pass

        return result
    
    def References(self, text):

        result = []

        try:
            refs = ""
            text = text.split("==References==")

            if len(text) > 1:
                text = text[1].split("\n")[1:]
                for el in text:
                    if el == "":
                        break
                    if el[0] == "*":
                        splitted = el.split(" ")
                        ref = [word for word in splitted if "http" not in word]
                        ref = " ".join(ref)
                        refs += " " + ref

            result = self.PP.preprocess_text(refs)
        except:
            pass

        return result
    
    def PageProcess(self, title, text):

        title = self.Title(title)
        body  = self.Body(text)
        category = self.Category(text)
        infobox = self.Infobox(text)
        link = self.Links(text)
        reference = self.References(text)

        return title, body, category, infobox, link, reference