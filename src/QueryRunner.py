import time
import argparse
import linecache
import re
from collections import Counter
from Preprocessor import Prep
from FileTraverser import FileTraverser
from QueryResultGetter import QueryResultsGetter
from Ranker import Ranker
from Stemmer import Stemmer
from nltk.corpus import stopwords
from Settings import Settings
from QueryResultGetter import QueryResultsGetter

class RunQuery():

    def __init__(self, text_pre_processor, file_traverser, ranker, query_results):

        self.file_traverser = file_traverser
        self.text_pre_processor = text_pre_processor
        self.ranker = ranker
        self.query_results = query_results

    def QueryType(self, query):
        
        field_replace_map = {
                ' t:':';t:',
                ' b:':';b:',
                ' c:':';c:',
                ' i:':';i:',
                ' l:':';l:',
                ' r:':';r:',
            }

        if ('t:' in query or 'b:' in query or 'c:' in query or 'i:' in query or 'l:' in query or 'r:' in query) and query[0:2] not in ['t:', 'b:', 'i:', 'c:', 'r:', 'l:']:

            for k, v in field_replace_map.items():
                if k in query:
                    query = query.replace(k, v)

            query = query.lstrip(';')

            return query.split(';')[0], query.split(';')[1:]

        elif 't:' in query or 'b:' in query or 'c:' in query or 'i:' in query or 'l:' in query or 'r:' in query:

            for k, v in field_replace_map.items():
                if k in query:
                    query = query.replace(k, v)

            query = query.lstrip(';')

            return query.split(';'), None

        else:
            return query, None

    def QueryResults(self, query, query_type):

        if query_type=='field':
            preprocessed_query = [[qry.split(':')[0], self.text_pre_processor.preprocess_text(qry.split(':')[1])] for qry in query]
        else:
            preprocessed_query = self.text_pre_processor.preprocess_text(query)

        if query_type == 'field':

            preprocessed_query_final = []
            for field, words in preprocessed_query:
                for word in words:
                    preprocessed_query_final.append([field, word])

            page_freq, page_postings = self.query_results.FQ(preprocessed_query_final)
        
        else:
            
            page_freq, page_postings = self.query_results.SQ(preprocessed_query)

        ranked_results = self.ranker.Rank(page_freq, page_postings)

        return ranked_results

    def UserInput(self, num_results):

        start = time.time()

        while True:
            query = input('Search Documents:- ')

            s = time.time()

            query = query.strip()
            query1, query2 = self.QueryType(query)

            if query == "!exit":
                break

            if query2:
                ranked_results1 = self.QueryResults(query1, 'simple')

                ranked_results2 = self.QueryResults(query2, 'field')

                ranked_results = Counter(ranked_results1) + Counter(ranked_results2)
                results = sorted(ranked_results.items(), key = lambda item : item[1], reverse=True)
                results = results[:num_results]

                for id, _ in results:
                    title= self.file_traverser.title_search(id)
                    print(id+',', title)

            elif type(query1)==type([]):

                ranked_results = self.QueryResults(query1, 'field')

                results = sorted(ranked_results.items(), key = lambda item : item[1], reverse=True)
                results = results[:num_results]

                for id, _ in results:
                    title= self.file_traverser.title_search(id)
                    print(id+',', title)

            else:
                ranked_results = self.QueryResults(query1, 'simple')

                results = sorted(ranked_results.items(), key = lambda item : item[1], reverse=True)
                results = results[:num_results]

                for id, _ in results:
                    title= self.file_traverser.title_search(id)
                    print(id+',', title)

            e = time.time()
            print('Search utility has finished in', e-s, 's')
            print()

def Run(resultNumber):
    stop_words = (set(stopwords.words("english")))
    html_tags = re.compile('&amp;|&apos;|&gt;|&lt;|&nbsp;|&quot;')
    stemmer = Stemmer('english')

    with open(f'{Settings.outputPath}/index/num_pages.txt', 'r') as f:
        num_pages = float(f.readline().strip())

    text_pre_processor = Prep(html_tags, stemmer, stop_words)
    file_traverser = FileTraverser()
    ranker = Ranker(num_pages)
    query_results = QueryResultsGetter(file_traverser)
    run_query = RunQuery(text_pre_processor, file_traverser, ranker, query_results)

    temp = linecache.getline(f'{Settings.outputPath}/index/id_title_map.txt', 0)

    print('------- Query Search and Ranking is Starting --------')

    start = time.time()

 
    run_query.UserInput(resultNumber)


    print('********** Query has evaluated in', time.time() - start, 'seconds **********')	
if __name__ == '__main__':
	
    start = time.time()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--filename', action='store', type=str)
    arg_parser.add_argument('--num_results', action='store', default=10, type=int)

    args = arg_parser.parse_args()

    fileName = args.filename
    resultNumber = args.num_results

    Run(fileName, resultNumber)