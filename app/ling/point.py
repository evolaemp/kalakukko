from app.ling.map import Map


class Point:
	"""
	Main purpose: to calculate its own swadeshness, done in 4 steps:
	(1) Get the reference language, i.e. the one nearest to the point. This is
	delegated to app.ling.Map.
	(2) Get the other relevant languages, where relevance is determined by the
	parameter. This is delegated to app.ling.Map.
	(3) Get the linguistic distance values for those languages from the
	relevant app.ling.WordMatrix.
	(4) Process those values using an app.ling.Correlator.
	"""
	
	def __init__(self, latitude, longitude):
		"""
		Constructor.
		"""
		self.latitude = latitude
		self.longitude = longitude
	
	def get_swadeshness(self, word_matrix, method, parameter):
		"""
		Calculates the swadeshness of the area as defined by the parameter with
		respect to the word matrix given.
		The method is either 'circle' or 'neighbourhood'.
		The parameter must be positive integer.
		"""
		globe = Map()
		
		origin = globe.get_nearest(self.latitude, self.longitude, 1)[0]
		
		if method == 'circle':
			languages = globe.get_in_radius(self.latitude, self.longitude, parameter)
		elif method == 'neighbourhood':
			languages = globe.get_nearest(self.latitude, self.longitude, parameter+1)
		else:
			raise ValueError('Swadeshness needs its parameter.')
		
		d = {}
		for language in languages:
			distance_pair = word_matrix.get_distances(origin, language)
			if distance_pair is not None:
				d[language] = distance_pair
		
		return origin, d


