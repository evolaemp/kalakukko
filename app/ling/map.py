from geopy.distance import EARTH_RADIUS

from app.ling.range_tree import RangeTree
from app.models import Language

from math import pi, sin, cos, acos, degrees, radians



class MapError(ValueError):
	pass



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
		
		latitudes = []
		longitudes = []
		
		for lang in Language.objects.all():
			if lang.latitude is None or lang.longitude is None:
				continue
			
			self.languages[lang.iso_code] = (lang.latitude, lang.longitude,)
			latitudes.append((lang.latitude, lang.iso_code))
			longitudes.append((lang.longitude, lang.iso_code))
		
		self.latitude_tree = RangeTree(latitudes)
		self.longitude_tree = RangeTree(longitudes)
	
	
	@staticmethod
	def great_circle(A, B):
		"""
		Calculates the great circle distance between the points given.
		The distance returned is in kilometres.
		"""
		d = acos(
			sin(radians(A[0])) * sin(radians(B[0]))
			+ cos(radians(A[0])) * cos(radians(B[0])) * cos(radians(abs(A[1] - B[1])))
		)
		return d * EARTH_RADIUS
	
	
	@staticmethod
	def make_tetragon(latitude, longitude, x):
		"""
		Makes a tetragon: two of its sides are parallels, two are meridians,
		and each side is supposedly at distance x from the centre.
		"""
		delta_latitude = 360 * x / (2 * pi * EARTH_RADIUS)
		
		try:
			delta_longitude = acos(
				( cos(radians(360 * x / (2 * pi * EARTH_RADIUS))) - sin(radians(latitude)) ** 2 )
				/ cos(radians(latitude)) ** 2
			)
			delta_longitude = degrees(delta_longitude)
		except ValueError:
			"""
			If the latitude is too close to the ±90 the last cos() will be
			close to 0 and the division will fail.
			"""
			raise MapError('Avoid the (ant)arctic chill.')
		
		tetragon = {
			'north': latitude + delta_latitude,
			'south': latitude - delta_latitude,
			'east': longitude + delta_longitude,
			'west': longitude - delta_longitude,
		}
		
		try:
			assert tetragon['north'] <= 90
			assert tetragon['south'] >= -90
		except AssertionError:
			raise MapError('Avoid the (ant)arctic chill.')
		
		return tetragon
	
	
	def get_in_tetragon(self, latitude, longitude, h):
		"""
		Returns set of languages located within the tetragon defined as:
		* its centre is (latitude, longitude);
		* the perpendicular between its centre and each of its sides is h (km).
		Encapsulates the search call to the class' range trees.
		"""
		centre = (latitude, longitude)
		
		tetragon = Map.make_tetragon(latitude, longitude, h)
		
		south_north = self.latitude_tree.search(tetragon['south'], tetragon['north'])
		
		if tetragon['west'] >= -180 and tetragon['east'] <= 180:
			west_east = self.longitude_tree.search(tetragon['west'], tetragon['east'])
		elif tetragon['west'] >= -180 and tetragon['east'] > 180:
			west_east = self.longitude_tree.search(tetragon['west'], 180)
			east = self.longitude_tree.search(-180, tetragon['east']-360)
			west_east = west_east.union(east)
		elif tetragon['west'] < -180 and tetragon['east'] <= 180:
			west = self.longitude_tree.search(tetragon['west']+360, 180)
			west_east = self.longitude_tree.search(-180, tetragon['east'])
			west_east = west_east.union(west)
		else:
			raise MapError('Tetragon ate the Earth.')
		
		return south_north.intersection(west_east)
	
	
	def get_nearest(self, latitude, longitude, k):
		"""
		Returns list of the nearest k languages to the coords given.
		Assumes that nearest languages do not lie further than 2000 kilometers.
		"""
		origin = (latitude, longitude,)
		
		possible_lang = self.get_in_radius(latitude, longitude, 2000)
		
		languages = []
		distances = []
		
		for iso_code in possible_lang:
			coords = self.languages[iso_code]
			d = Map.great_circle(origin, coords)
			
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
	
	
	def get_single_nearest(self, latitude, longitude, radius=2000):
		"""
		Returns the nearest language (if such) within the radius given.
		The radius is measured in kilometers.
		Assumes that nearest languages do not lie further than 2000 kilometers.
		"""
		origin = (latitude, longitude)
		
		possible_lang = self.get_in_radius(latitude, longitude, radius)
		
		nearest_lang = None
		smallest_dist = None
		
		for iso_code in possible_lang:
			coords = self.languages[iso_code]
			d = Map.great_circle(origin, coords)
			
			if smallest_dist is None or d < smallest_dist:
				smallest_dist = d
				nearest_lang = iso_code
		
		return nearest_lang
	
	
	def get_in_radius(self, latitude, longitude, radius):
		"""
		Returns set of the languages within radius r of the coords given.
		The radius is measured in kilometres.
		"""
		origin = (latitude, longitude,)
		
		possible_lang = self.get_in_tetragon(latitude, longitude, radius)
		
		s = set()
		
		for iso_code in possible_lang:
			coords = self.languages[iso_code]
			if Map.great_circle(origin, coords) <= radius:
				s.add(iso_code)
		
		return s



