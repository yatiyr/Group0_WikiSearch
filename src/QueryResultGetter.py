from collections import defaultdict
from FileTraverser import FileTraverser

class QueryResultsGetter():

	def __init__(self, file_traverser):

		self.file_traverser = file_traverser

	def SQ(self, preprocessed_query):

		page_freq, page_postings = {}, defaultdict(dict)
		
		for token in preprocessed_query:
			token_info = self.file_traverser.get_token_info(token)

			if token_info:
				file_num, freq, title_line, body_line, category_line, infobox_line, link_line, reference_line = token_info
				line_map = {
						'title' : title_line, 'body' : body_line, 'category' : category_line, 'infobox' : infobox_line, 'link' : link_line, 'reference' : reference_line
					}

				for field_name, line_num in line_map.items():
					
					if line_num!='':
						posting = self.file_traverser.search_field_file(field_name, file_num, line_num)

						page_freq[token] = len(posting.split(';'))
						page_postings[token][field_name] = posting


		return page_freq, page_postings


	def FQ(self, preprocessed_query):

		page_freq, page_postings = {}, defaultdict(dict)

		for field, token in preprocessed_query:
			token_info = self.file_traverser.get_token_info(token)

			if token_info:
				file_num, freq, title_line, body_line, category_line, infobox_line, link_line, reference_line = token_info
				line_map = {
					'title':title_line, 'body':body_line, 'category':category_line, 'infobox':infobox_line, 'link':link_line, 'reference':reference_line
				}
				field_map = {
					't':'title', 'b':'body', 'c':'category', 'i':'infobox', 'l':'link', 'r':'reference'
				}

				field_name = field_map[field]
				line_num = line_map[field_name]

				posting = self.file_traverser.search_field_file(field_name, file_num, line_num)
				page_freq[token] = len(posting)
				page_postings[token][field_name] = posting

		return page_freq, page_postings