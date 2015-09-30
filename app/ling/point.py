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
	
	def get_swadeshness(self, word_matrix, radius=None, nearest=None):
		"""
		Calculates the swadeshness of the area as defined by the parameter with
		respect to the word matrix given.
		The parameter is either radius or nearest, whichever is not None.
		"""
		globe = Map()
		
		origin = globe.get_nearest(1)[0]
		
		if radius is not None:
			languages = globe.get_in_radius(radius)
		elif nearest is not None:
			languages = globe.get_nearest(nearest)
		else:
			raise ValueError('Swadeshness needs its parameter.')
		
		d = {}
		for language in languages:
			distance_pair = word_matrix.get_distances(origin, language)
			if distance_pair is not None:
				d[language] = distance_pair
		
		return d



