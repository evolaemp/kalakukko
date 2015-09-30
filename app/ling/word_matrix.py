from django.core.cache import cache

import codecs
import csv
import uuid


PREFIX = 'matrix_'


class WordMatrix:
	"""
	Wrapper for the information of a .tsv file.
	Also handles between-requests storage.
	"""
	
	def __init__(self):
		"""
		Constructor.
		"""
		self.d = {}
		self.storage_id = None
	
	
	def load_raw(self, file_handler):
		"""
		Parses the file into a dictionary in which:
		* the keys are tuples of ISO codes ordered alphabetically;
		* the values are tuples of the respective (global, real) distances.
		Raises ValueError if the file does not conform to expected format.
		"""
		if hasattr(file_handler, 'encoding'):  # 'rt'
			reader = csv.reader(file_handler, delimiter='\t')
		else:  # 'rb' --- this is what django's UploadedFile gives
			reader = csv.reader(codecs.iterdecode(file_handler, 'utf-8'), delimiter='\t')
		
		count = -1
		
		for row in reader:
			count += 1
			if count == 0:
				continue
			
			try:
				assert row[2].find(':') > 0
				assert row[3].find(':') > 0
			except AssertionError:
				self.d = None
				raise ValueError('File does not conform to format.')
			
			key = [
				row[2].split(':')[0],
				row[3].split(':')[0],
			]
			key.sort()
			key = tuple(key)
			
			value = (
				float(row[0]),
				float(row[1]),
			)
			
			self.d[key] = value
	
	
	def load(self, storage_id):
		"""
		Retrieves the word matrix corresponding to the id given.
		Raises ValueError if there is nothing in storage.
		"""
		self.d = cache.get(storage_id)
		if self.d is None:
			self.d = {}
			raise ValueError('Matrix not found.')
		
		try:
			assert type(self.d) is dict
		except AssertionError:
			self.d = {}
			raise ValueError('Matrix found but useless.')
	
	
	def save(self):
		"""
		Stores the word matrix for later retrieval.
		Sets self.storage_id.
		"""
		while True:
			key = PREFIX + str(uuid.uuid4())
			if cache.get(key) is None:
				break
		
		cache.set(key, self.d)
		
		self.storage_id = key
		return self.storage_id
	
	
	def get_distances(self, lang_one, lang_two):
		"""
		Returns the (global, real) distance tuple for the language pair.
		"""
		key = [lang_one, lang_two]
		key.sort()
		key = tuple(key)
		
		if key in self.d:
			return self.d[key]
		else:
			return None



