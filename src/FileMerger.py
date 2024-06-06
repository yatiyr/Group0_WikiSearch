import os
from collections import defaultdict

from Settings import *
# integrated from https://medium.com/analytics-vidhya/search-engine-in-python-from-scratch-c3f7cc453250
class FileMerger():

    def __init__(self, num_itermed_files, write_data):

        self.num_itermed_files = num_itermed_files
        self.write_data = write_data

    def Merge(self):
        
        files_data = {}
        line = {}
        postings = {}
        is_file_empty = {i:1 for i in range(self.num_itermed_files)}
        tokens = []

        i = 0
        while i < self.num_itermed_files:
            
            files_data[i] = open(f'{Settings.outputPath}/index/index_{i}.txt', 'r')
            line[i] = files_data[i].readline().strip('\n')
            postings[i] = line[i].split('-')
            is_file_empty[i]=0
            new_token = postings[i][0]
            if new_token not in tokens:
                tokens.append(new_token)
            i+=1

        tokens.sort(reverse=True)
        num_processed_postings=0
        data_to_merge = defaultdict(str)
        num_files_final = 0

        while sum(is_file_empty.values()) != self.num_itermed_files:
            
            token = tokens.pop()
            num_processed_postings+=1

            if num_processed_postings%30000==0:

                num_files_final = self.write_data.WriteFiles(data_to_merge, num_files_final)

                data_to_merge = defaultdict(str)

            i=0
            while i < self.num_itermed_files:

                if is_file_empty[i]==0:
                    
                    if token==postings[i][0]:
                        
                        line[i] = files_data[i].readline().strip('\n')
                        data_to_merge[token]+=postings[i][1]
                        
                        if len(line[i]):
                            postings[i]=line[i].split('-')
                            new_token = postings[i][0]
                            
                            if new_token not in tokens:
                                tokens.append(new_token)
                                tokens.sort(reverse=True)
                        
                        else:
                            is_file_empty[i] = 1
                            files_data[i].close()
                            print(f'Removing file {str(i)}')
                            os.remove(f'{Settings.outputPath}/index/index_{str(i)}.txt')
                i+=1

        num_files_final = self.write_data.WriteFiles(data_to_merge, num_files_final)

        return num_files_final    