from geopy.distance import great_circle

from app.models import Language



class Map:
	"""
	Wrapper around the database, the class handles geo calculations.
	Its methods return lists/sets of ISO codes, not model instances.
	ISO codes match those from .tsv files, i.e. 639-1 ? 639-1 : 639-3
	"""
	
	def __init__(self):
		"""
		Constructor. Loads all relevant data from the database in memory in
		order to avoid unnecessary database calls.
		"""
		self.languages = {}
		
		for lang in Language.objects.all():
			self.languages[lang.iso_code] = (lang.latitude, lang.longitude,)
	
	
	def get_nearest(self, latitude, longitude, k):
		"""
		Returns list of the nearest k languages to the coords given.
		"""
		origin = (latitude, longitude,)
		
		languages = []
		distances = []
		
		for iso_code, coords in self.languages.items():
			d = great_circle(origin, coords).kilometers
			
			if len(distances) < k or d < distances[-1]:
				for i, j in enumerate(distances):
					if d < j:
						distances.insert(i, d)
						languages.insert(i, iso_code)
						break
				else:
					if len(distances) < k:
						distances.append(d)
						languages.append(iso_code)
				
				if len(distances) > k:
					del distances[-1]
					del languages[-1]
			
		return languages
	
	
	def get_in_radius(self, latitude, longitude, r):
		"""
		Returns set of the languages within radius r of the coords given.
		The radius is measured in kilometres.
		"""
		origin = (latitude, longitude,)
		
		s = set()
		
		for iso_code, coords in self.languages.items():
			if great_circle(origin, coords).kilometers <= r:
				s.add(iso_code)
		
		return s



