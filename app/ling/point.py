from app.ling.map import Map


class Point:
	"""
	Main purpose: to calculate its own swadeshness, done in 3 steps:
	(1) Get the relevant languages, where relevance is determined by the
	parameter. This is delegated to app.ling.Map.
	(2) Get the linguistic distance values for those languages from the
	relevant app.ling.WordMatrix.
	(3) Process those values using an app.ling.Correlator.
	"""
	
	def __init__(self, latitude, longitude):
		pass
	
	def get_swadeshness(self):
		"""
		"""
		pass



