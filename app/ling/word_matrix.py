import csv


class WordMatrix:
	"""
	A WordMatrix is essentially a loaded in memory .tsv file for easy access of
	relevant information.
	Also handles between-requests storage.
	"""
	
	def __init__(self):
		self.storage_id = None
	
	def load_raw(self, file_handler):
		"""
		"""
		pass
	
	def load(self, storage_id):
		pass
	
	def save(self):
		pass
	
	def get_id(self):
		return self.storage_id



