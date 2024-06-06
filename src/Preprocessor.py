import re

from Settings import *
'''
We need to get rid of unnecessary parts of words while indexing, this class
handles:
    - Stemming the text
    - Removing the stopwords
    - Remove non ascii
    - Remove html tags
    - Remove special characters if exists
'''
class Prep():
	def __init__(self, html_tags, stemmer, stop_words):
		
		self.html_tags=html_tags
		self.stemmer=stemmer
		self.stop_words=stop_words

	def remove_stopwords(self, text_data):
		
		cleaned_text = [word for word in text_data if word not in self.stop_words]
		
		return cleaned_text

	def stem_text(self, text_data):
		
		cleaned_text = self.stemmer.stemWords(text_data)
		
		return cleaned_text

	def remove_non_ascii(self, text_data):

		cleaned_text = ''.join([i if ord(i) < 128 else ' ' for i in text_data])
		
		return cleaned_text

	def remove_html_tags(self, text_data):
		
		cleaned_text = re.sub(self.html_tags, ' ', text_data)
		
		return cleaned_text

	def remove_special_chars(self, text_data):
		
		cleaned_text = ''.join(ch if ch.isalnum() else ' ' for ch in text_data)
		
		return cleaned_text

	def remove_select_keywords(self, text_data):
		
		text_data = text_data.replace('\n', ' ').replace('File:', ' ')
		text_data = re.sub('(http://[^ ]+)', ' ', text_data)
		text_data = re.sub('(https://[^ ]+)', ' ', text_data)
		
		return text_data

	def tokenize_sentence(self, text_data, flag=False):
		
		if flag:
			text_data = self.remove_select_keywords(text_data)
			text_data = re.sub('\{.*?\}|\[.*?\]|\=\=.*?\=\=', ' ', text_data)
		cleaned_text = self.remove_non_ascii(text_data)
		cleaned_text = self.remove_html_tags(cleaned_text)
		cleaned_text = self.remove_special_chars(cleaned_text)
		
		return cleaned_text.split()

	def preprocess_text(self, text_data, flag=False):

		cleaned_data = self.tokenize_sentence(text_data.lower(), flag)
		cleaned_data = self.remove_stopwords(cleaned_data)
		cleaned_data = self.stem_text(cleaned_data)
		
		return cleaned_data
        
        