from Settings import *
import linecache

class FileTraverser():

	def __init__(self):

		pass

	def bsT(self, high, filename, inp_token):
		
		low = 0
		while low < high:
			
			mid = (low + high)//2
			line = linecache.getline(filename, mid)
			token = line.split('-')[0]

			if inp_token == token:
				token_info = line.split('-')[1:-1]
				return token_info
			
			elif inp_token > token:
				low = mid + 1
			
			else:
				high = mid

		return None

	def title_search(self, page_id):

		title = linecache.getline(f'{Settings.outputPath}/index/id_title_map.txt', int(page_id)+1).strip()
		title = title.split('-', 1)[1]

		return title


	def search_field_file(self, field, file_num, line_num):
		
		if line_num != '':
			line = linecache.getline(f'{Settings.outputPath}/index/{field}_data_{str(file_num)}.txt', int(line_num)).strip()
			postings = line.split('-')[1]

			return postings

		return ''

	def get_token_info(self, token):

		char_list = [chr(i) for i in range(97,123)]
		num_list = [str(i) for i in range(0,10)]

		if token[0] in char_list:
			with open(f'{Settings.outputPath}/index/tokens_info_{token[0]}_count.txt', 'r') as f:
				num_tokens = int(f.readline().strip())

			tokens_info_pointer =f'{Settings.outputPath}/index/tokens_info_{token[0]}.txt'
			token_info = self.bsT(num_tokens, tokens_info_pointer, token)

		elif token[0] in num_list:
			with open(f'{Settings.outputPath}/index/tokens_info_{token[0]}_count.txt', 'r') as f:
				num_tokens = int(f.readline().strip())

			tokens_info_pointer = f'{Settings.outputPath}/index/tokens_info_{token[0]}.txt'
			token_info = self.bsT(num_tokens, tokens_info_pointer, token)

		else:
			with open(f'{Settings.outputPath}/index/tokens_info_others_count.txt', 'r') as f:
				num_tokens = int(f.readline().strip())

			tokens_info_pointer = f'{Settings.outputPath}/index/tokens_info_others.txt'
			token_info = self.bsT(num_tokens, tokens_info_pointer, token)

		return token_info