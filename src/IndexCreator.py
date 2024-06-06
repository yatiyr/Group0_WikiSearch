import re
from collections import defaultdict

from Settings import *
class IndexCreator():

    def __init__(self, writeData):
        self.WriteData = writeData

    def Index(self, title, body, category, infobox, link, reference):

        wS, tD, bD, cD, iD, lD, rD = set(), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)

        wS.update(title)
        for word in title:
            tD[word]+=1

        wS.update(body)
        for word in body:
            bD[word]+=1

        wS.update(category)
        for word in category:
            cD[word]+=1

        wS.update(infobox)
        for word in infobox:
            iD[word]+=1

        wS.update(link)
        for word in link:
            lD[word]+=1

        wS.update(reference)
        for word in reference:
            rD[word]+=1

        for word in wS:
            temp = re.sub(r'^((.)(?!\2\2\2))+$',r'\1', word)
            is_rep = len(temp)==len(word)

            if not is_rep:
                posting = str(Settings.pageNumber)+':'

                if tD[word]:
                    posting += 't'+str(tD[word])

                if bD[word]:
                    posting += 'b'+str(bD[word])

                if cD[word]:
                    posting += 'c'+str(cD[word])

                if iD[word]:
                    posting += 'i'+str(iD[word])

                if lD[word]:
                    posting += 'l'+str(lD[word])

                if rD[word]:
                    posting += 'r'+str(rD[word])

                posting+=';'

                Settings.indexMap[word]+=posting

        Settings.pageNumber+=1
        print(Settings.pageNumber)

        if not Settings.pageNumber%40000:
            
            self.WriteData.IntermediateIndex()
            self.WriteData.IdTitleMap()
            
            Settings.indexMap = defaultdict(str)
            Settings.idTitleMap = {}                       