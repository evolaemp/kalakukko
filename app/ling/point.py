from app.ling.map import Map
from app.ling.math import get_correlation



class Point:
	"""
	Main purpose: to calculate its own swadeshness, done in 3 steps:
	(1) Get the relevant languages, where relevance is determined by the
	parameter. This is delegated to app.ling.map.
	(2) Get the linguistic distance values for those languages from the
	relevant app.ling.word_matrix.
	(3) Process those values using an app.ling.math.
	"""
	
	def __init__(self, latitude, longitude):
		"""
		Constructor.
		"""
		self.latitude = latitude
		self.longitude = longitude
	
	
	def get_swadeshness_in_radius(self, word_matrix, radius):
		"""
		Calculates the swadeshness within the radius given with respect to the
		word matrix given.
		"""
		globe = Map()
		
		languages = globe.get_in_radius(self.latitude, self.longitude, radius)
		
		d = {}
		global_d, local_d = [], []
		
		for lang_a in languages:
			for lang_b in languages:
				if lang_a == lang_b:
					continue
				
				if lang_a > lang_b:
					continue
				
				if (lang_a, lang_b) not in word_matrix.d:
					continue
				
				key = lang_a +','+ lang_b
				d[key] = word_matrix.d[(lang_a, lang_b)]
				
				global_d.append(d[key][0])
				local_d.append(d[key][1])
		
		p = get_correlation(global_d, local_d)
		
		return d, p
	
	
	def get_swadeshness_by_nearest(self, word_matrix, k):
		"""
		Calculates the swadeshness of the k languages nearest to the language
		which is nearest to the point. Only the distances between that nearest
		language (the origin) and each of the others are taken into account. 
		The parameter k must be positive integer.
		"""
		globe = Map()
		
		languages = globe.get_nearest(self.latitude, self.longitude, k+1)
		
		if len(languages) == 0:
			return None, {}, 0
		if len(languages) == 1:
			return languages[0], {}, 0
		
		origin = languages[0]
		languages = languages[1:]
		
		d = {}
		global_d, local_d = [], []
		
		for language in languages:
			distance_pair = word_matrix.get_distances(origin, language)
			if distance_pair is not None:
				d[language] = distance_pair
				global_d.append(distance_pair[0])
				local_d.append(distance_pair[1])
		
		p = get_correlation(global_d, local_d)
		
		return origin, d, p



