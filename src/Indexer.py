from DataWriter import *
from FileMerger import *
from IndexCreator import *
from Preprocessor import *
from WikiPageProcessor import *
from XMLParser import *

from Settings import *
import os
import re
import sys
import time
from tqdm import tqdm
import xml.sax
from nltk.corpus import stopwords
from Stemmer import Stemmer


def Run(inputFile):
    start = time.time()

    html_tags = re.compile('&amp;|&apos;|&gt;|&lt;|&nbsp;|&quot;')
    stemmer = Stemmer('english')
    stop_words = (set(stopwords.words("english")))

    text_pre_processor = Prep(html_tags, stemmer, stop_words)
    page_processor     = WikiPageProcessor(text_pre_processor)
    write_data         = DataWriter()
    create_index       = IndexCreator(write_data)

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,False)
    xml_parser = XMLParser(page_processor, create_index)
    parser.setContentHandler(xml_parser)
    output=parser.parse(inputFile)

    write_data.IntermediateIndex()
    write_data.IdTitleMap()

    merge_files = FileMerger(Settings.fileNumber, write_data)
    num_files_final = merge_files.Merge()

    with open(f'{Settings.outputPath}/index/num_pages.txt', 'w') as f:
        f.write(str(Settings.pageNumber))

    num_tokens_final = 0
    with open(f'{Settings.outputPath}/index/tokens_info.txt', 'r') as f:
        for line in f:
            num_tokens_final+=1

    with open(f'{Settings.outputPath}/index/num_tokens.txt', 'w') as f:
        f.write(str(num_tokens_final))

    char_list = [chr(i) for i in range(97,123)]
    num_list = [str(i) for i in range(0,10)]

    with open(f'{Settings.outputPath}/index/tokens_info.txt', 'r') as f:
        for line in tqdm(f):
            if line[0] in char_list:
                with open(f'{Settings.outputPath}/index/tokens_info_{line[0]}.txt', 'a') as t:
                    t.write(line.strip())
                    t.write('\n')
            
            elif line[0] in num_list:
                with open(f'{Settings.outputPath}/index/tokens_info_{line[0]}.txt', 'a') as t:
                    t.write(line.strip())
                    t.write('\n')

            else:
                with open(f'{Settings.outputPath}/index/tokens_info_others.txt', 'a') as t:
                    t.write(line.strip())
                    t.write('\n')

    for ch in tqdm(char_list):
        tok_count = 0
        with open(f'{Settings.outputPath}/index/tokens_info_{ch}.txt', 'r') as f:
            for line in f:
                tok_count+=1

        with open(f'{Settings.outputPath}/index/tokens_info_{ch}_count.txt', 'w') as f:
            f.write(str(tok_count))

    for num in tqdm(num_list):
        tok_count = 0
        with open(f'{Settings.outputPath}/index/tokens_info_{num}.txt', 'r') as f:
            for line in f:
                tok_count+=1

        with open(f'{Settings.outputPath}/index/tokens_info_{num}_count.txt', 'w') as f:
            f.write(str(tok_count))

    try:
        tok_count = 0
        with open(f'{Settings.outputPath}/index/tokens_info_others.txt', 'r') as f:
            tok_count+=1

        with open(f'{Settings.outputPath}/index/tokens_info_others_count.txt', 'w') as f:
            f.write(str(tok_count))
    except:
        pass

    os.remove(f'{Settings.outputPath}/index/tokens_info.txt')
    print('Total finished tokens are',num_tokens_final)
    print('Number of final files are', num_files_final)

    end = time.time()

    print('Indexing has finished in -', end-start)

if __name__ == "__main__":
    Run(sys.argv[1])
