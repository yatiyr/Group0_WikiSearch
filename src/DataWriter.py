from tqdm import tqdm
from collections import defaultdict
import re

from Settings import *
# Integrated from https://medium.com/analytics-vidhya/search-engine-in-python-from-scratch-c3f7cc453250
class DataWriter():

    def __init__(self):
        pass

    def IdTitleMap(self):

        tidTitle = []

        idTitle = sorted(Settings.idTitleMap.items(), key = lambda item: int(item[0]))
        print(idTitle)

        for el in tqdm(idTitle):
            id = el[0]
            title = el[1]
            t = str(id) + "-" + title.strip()
            tidTitle.append(t)

        with open(Settings.outputPath + "/index/id_title_map.txt", 'a', encoding = "utf-8") as file:
            file.write("\n".join(tidTitle))
            file.write("\n")

    def IntermediateIndex(self):

        iM = sorted(Settings.indexMap.items(), key = lambda item : item[0])

        tI = []

        for w, p in tqdm(iM):
            tI.append(w + "-" + p)

        with open(f"{Settings.outputPath}/index/index_{Settings.fileNumber}.txt", "w") as file:
            file.write("\n".join(tI))

        Settings.fileNumber += 1

    def WriteFiles(self, mergeData, fileNumFinal):
        tD, bD, cD, iD, lD, rD = defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)

        tokenInfoU = {}

        sortedD = sorted(mergeData.items(), key = lambda item : item[0])

        for i, (token, postings) in tqdm(enumerate(sortedD)):
            for posting in postings.split(";")[:-1]:
                id = posting.split(':')[0]

                fields = posting.split(':')[1]

                if 't' in fields:
                    tD[token][id] = re.search(r'.*t([0-9]*).*', fields).group(1)

                if 'b' in fields:
                    bD[token][id] = re.search(r'.*b([0-9]*).*', fields).group(1)

                if 'c' in fields:
                    cD[token][id] = re.search(r'.*c([0-9]*).*', fields).group(1)

                if 'i' in fields:
                    iD[token][id] = re.search(r'.*i([0-9]*).*', fields).group(1)

                if 'l' in fields:
                    lD[token][id] = re.search(r'.*l([0-9]*).*', fields).group(1)

                if 'r' in fields:
                    rD[token][id] = re.search(r'.*r([0-9]*).*', fields).group(1)

            tokenInfo = "-".join([token, str(fileNumFinal), str(len(postings.split(';')[:-1]))])
            tokenInfoU[token] = tokenInfo + "-"

        fT, fB, fC, fI, fL, fR = [], [], [], [], [], []

        for i, (token, _) in tqdm(enumerate(sortedD)):

            if token in tD.keys():
                posting = tD[token]
                fT = self.DiffPostings(token, posting, fT)
                t = len(fT)
                tokenInfoU[token]+=str(t)+'-'
            else:
                tokenInfoU[token]+='-'

            if token in bD.keys():
                posting = bD[token]
                fB = self.DiffPostings(token, posting, fB)
                t = len(fB)
                tokenInfoU[token]+=str(t)+'-'
            else:
                tokenInfoU[token]+='-'

            if token in cD.keys():
                posting = cD[token]
                fC = self.DiffPostings(token, posting, fC)
                t = len(fC)
                tokenInfoU[token]+=str(t)+'-'
            else:
                tokenInfoU[token]+='-'

            if token in iD.keys():
                posting = iD[token]
                fI = self.DiffPostings(token, posting, fI)
                t = len(fI)
                tokenInfoU[token]+=str(t)+'-'
            else:
                tokenInfoU[token]+='-'

            if token in lD.keys():
                posting = lD[token]
                fL = self.DiffPostings(token, posting, fL)
                t = len(fL)
                tokenInfoU[token]+=str(t)+'-'
            else:
                tokenInfoU[token]+='-'

            if token in rD.keys():
                posting = rD[token]
                fR = self.DiffPostings(token, posting, fR)
                t = len(fR)
                tokenInfoU[token]+=str(t)+'-'
            else:
                tokenInfoU[token]+='-'

        with open(f'{Settings.outputPath}/index/tokens_info.txt', 'a') as f:
            f.write('\n'.join(tokenInfoU.values()))
            f.write('\n')

        self.DiffPostingsW('title', fT, fileNumFinal)

        self.DiffPostingsW('body', fB, fileNumFinal)

        self.DiffPostingsW('category', fC, fileNumFinal)

        self.DiffPostingsW('infobox', fI, fileNumFinal)

        self.DiffPostingsW('link', fL, fileNumFinal)

        self.DiffPostingsW('reference', fR, fileNumFinal)

        fileNumFinal+=1

        return fileNumFinal

    def DiffPostings(self, token, postings, final_tag):

        postings = sorted(postings.items(), key = lambda item : int(item[0]))

        final_posting = token+'-'
        for id, freq in postings:
            final_posting+=str(id)+':'+freq+';'

        final_tag.append(final_posting.rstrip(';'))

        return final_tag

    def DiffPostingsW(self, tag_type, final_tag, num_files_final):

        with open(f'{Settings.outputPath}/index/{tag_type}_data_{str(num_files_final)}.txt', 'w') as f:
            f.write('\n'.join(final_tag))              