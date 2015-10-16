from app.ling.map import Map
from app.ling.math import get_correlation

import random



class Honeycomb:
	"""
	Calculates the swadeshness of each honeycomb cell.
	"""
	
	def __init__(self, cells):
		"""
		Constructor.
		"""
		self.cells = cells
	
	
	def calculate(self, word_matrix, method, parameter):
		"""
		The workhorse.
		"""
		try:
			assert method in ('circle', 'neighbourhood',)
		except AssertionError:
			raise ValueError('Swadeshness needs its parameter.')
		
		is_circle = True if method == 'circle' else False
		
		planet = Map()
		
		for cell in self.cells:
			origin = planet.get_nearest(cell[0], cell[1], 1)
			if len(origin) > 0:
				origin = origin[0]
			else:
				cell.append(0)
				continue
			
			if is_circle:
				languages = planet.get_in_radius(cell[0], cell[1], parameter)
			else:
				languages = planet.get_nearest(cell[0], cell[1], parameter+1)
			
			a, b = [], []
			for language in languages:
				distance_pair = word_matrix.get_distances(origin, language)
				if distance_pair is not None:
					a.append(distance_pair[0])
					b.append(distance_pair[1])
			
			cell.append(get_correlation(a, b))
		
		return self.cells



