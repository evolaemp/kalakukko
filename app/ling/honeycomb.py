from app.ling.map import Map, MapError
from app.ling.math import get_correlation



class Honeycomb:
	"""
	Calculates the swadeshness of each honeycomb cell.
	Unlike class Point, Honeycomb should not raise errors.
	"""
	
	def __init__(self, cells):
		"""
		Constructor.
		"""
		self.cells = cells
	
	
	def calculate_on_circles(self, word_matrix, radius):
		"""
		Calculates the swadeshness of each cell using the circles method.
		Cells with less than 6 relevant languages have swadeshness of 0.
		"""
		planet = Map()
		
		for cell in self.cells:
			try:
				languages = planet.get_in_radius(cell[0], cell[1], radius)
			except MapError:
				cell.append(0)
				continue
			
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
	
	
	def calculate_on_neighbourhoods(self, word_matrix, k):
		"""
		Calculates the swadeshness of each cell using the neighbourhood method.
		Cells with less than 6 relevant languages have swadeshness of 0.
		"""
		planet = Map()
		
		for cell in self.cells:
			try:
				languages = planet.get_nearest(cell[0], cell[1], k+1)
			except MapError:
				cell.append(0)
				continue
			
			if len(languages) < 6:
				cell.append(0)
				continue
			
			origin = languages[0]
			languages = languages[1:]
			
			global_d, local_d = [], []
			for language in languages:
				distance_pair = word_matrix.get_distances(origin, language)
				if distance_pair is not None:
					global_d.append(distance_pair[0])
					local_d.append(distance_pair[1])
			
			cell.append(get_correlation(global_d, local_d))
		
		return self.cells



