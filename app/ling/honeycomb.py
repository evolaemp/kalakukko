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
	
	
	def calculate_on_circles(self, word_matrix, radius):
		"""
		Calculates the swadeshness of each cell using the circles method.
		"""
		planet = Map()
		
		for cell in self.cells:
			languages = planet.get_in_radius(cell[0], cell[1], radius)
			
			if len(languages) < 6:
				cell.append(0)
				continue
			
			global_d, local_d = [], []
			
			for lang_a in languages:
				for lang_b in languages:
					if lang_a >= lang_b:
						continue
					
					if (lang_a, lang_b) not in word_matrix.d:
						continue
					
					global_d.append(word_matrix.d[(lang_a, lang_b)][0])
					local_d.append(word_matrix.d[(lang_a, lang_b)][1])
			
			cell.append(get_correlation(global_d, local_d))
		
		return self.cells
	
	
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



