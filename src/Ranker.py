import math
from collections import defaultdict

class Ranker():

	def __init__(self, num_pages):

		self.num_pages = num_pages

	def Rank(self, page_freq, page_postings):
		
		result = defaultdict(float)
		weightage_dict = {'title':1.0, 'body':0.85, 'category':0.3, 'infobox':0.65, 'link':0.15, 'reference':0.15}
		
		for token, field_post_dict in page_postings.items():
			
			for field, postings in field_post_dict.items():
				
				weightage = weightage_dict[field]
				
				if len(postings)>0:
					for post in postings.split(';'):
						
						id, post = post.split(':')
						result[id] += weightage*(1+math.log(int(post)))*math.log((self.num_pages-int(page_freq[token]))/int(page_freq[token]))

		return result