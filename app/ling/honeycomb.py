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
		planet = Map()
		
		if method == 'circle':
			radius = parameter
			find = planet.get_in_radius
		else:
			radius = 500
			parameter = parameter + 1
			find = planet.get_nearest
		
		
		for cell in self.cells:
			origin = planet.get_single_nearest(cell[0], cell[1], radius)
			if origin is None:
				cell.append(0)
				continue
			
			languages = find(cell[0], cell[1], parameter)
			
			a, b = [], []
			for language in languages:
				distance_pair = word_matrix.get_distances(origin, language)
				if distance_pair is not None:
					a.append(distance_pair[0])
					b.append(distance_pair[1])
			
			cell.append(get_correlation(a, b))
		
		return self.cells



