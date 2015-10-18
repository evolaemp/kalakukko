from geopy.distance import great_circle

from app.models import Language

import math



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
	
	
	def get_in_tetragon(self, latitude, longitude, h):
		"""
		Returns set of languages located within the tetragon defined as:
		* its centre is (latitude, longitude);
		* the perpendicular between its centre and each of its sides is h (km).
		Encapsulates the search call to the class' range trees.
		"""
		centre = (latitude, longitude)
		
		north = latitude
		while great_circle(centre, (north, longitude)).km < h:
			north = north + 1
		
		south = latitude
		while great_circle(centre, (south, longitude)).km < h:
			south = south - 1
		
		east = longitude
		while great_circle(centre, (latitude, east)).km < h:
			east = east + 1
		west = longitude - (east - longitude)
		
		possible_lang = self.latitude_tree.search(south, north).union(
						self.longitude_tree.search(west, east))
		
		return possible_lang
	
	
	def get_nearest(self, latitude, longitude, k):
		"""
		Returns list of the nearest k languages to the coords given.
		Assumes that nearest languages do not lie further than 1000 kilometers.
		"""
		origin = (latitude, longitude,)
		
		possible_lang = self.get_in_tetragon(latitude, longitude, 1000)
		
		languages = []
		distances = []
		
		for iso_code in possible_lang:
			coords = self.languages[iso_code]
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
	
	
	def get_single_nearest(self, latitude, longitude, r):
		"""
		Returns the nearest language (if such) within the radius given.
		The radius is measured in kilometers.
		"""
		origin = (latitude, longitude)
		
		possible_lang = self.get_in_tetragon(latitude, longitude, r)
		
		nearest_lang = None
		smallest_dist = None
		
		for iso_code in possible_lang:
			coords = self.languages[iso_code]
			d = great_circle(origin, coords).kilometers
			
			if smallest_dist is None or d < smallest_dist:
				smallest_dist = d
				nearest_lang = iso_code
		
		return nearest_lang
	
	
	def get_in_radius(self, latitude, longitude, r):
		"""
		Returns set of the languages within radius r of the coords given.
		The radius is measured in kilometres.
		"""
		origin = (latitude, longitude,)
		
		possible_lang = self.get_in_tetragon(latitude, longitude, r)
		
		s = set()
		
		for iso_code in possible_lang:
			coords = self.languages[iso_code]
			if great_circle(origin, coords).kilometers <= r:
				s.add(iso_code)
		
		return s



class RangeTree:
	"""
	node: {'left': node, 'right': node, 'value': 42, 'item': None}
	"""
	
	def __init__(self, d):
		"""
		Constructor.
		"""
		try:
			leaves = sorted(d)
		except TypeError:
			raise ValueError('Unorderable values.')
		
		self.tree = RangeTree.create_tree(leaves)
	
	
	def create_tree(leaves):
		"""
		Recursively create a tree out of the leaves given.
		The leaves must be [] of (value, item,) tuples.
		"""
		if len(leaves) in (1, 2,):
			left = {
				'value': leaves[0][0],
				'item': leaves[0][1],
				'left': None,
				'right': None
			}
			
			if len(leaves) == 2:
				right = {
					'value': leaves[1][0],
					'item': leaves[1][1],
					'left': None,
					'right': None
				}
			else:
				right = None
			
			value = leaves[0][0]
		
		else:
			half = int(len(leaves) / 2)
			
			left = RangeTree.create_tree(leaves[:half])
			right = RangeTree.create_tree(leaves[half:])
			
			value = left['value']
			if left['right'] is not None:
				if left['right']['value'] > value:
					value = left['right']['value']
		
		return {
			'left': left,
			'right': right,
			'value': value
		}
	
	
	def search_tree(tree, a, b):
		"""
		Recursively search the tree given.
		"""
		if tree['value'] < a:
			if tree['right'] is None:
				return set()
			return RangeTree.search_tree(tree['right'], a, b)
		
		if tree['value'] > b:
			if tree['left'] is None:
				return set()
			return RangeTree.search_tree(tree['left'], a, b)
		
		
		if tree['left'] is None and tree['right'] is None:
			return set([tree['item']])
		
		
		items_left = set()
		if tree['left'] is not None:
			items_left = RangeTree.search_tree(tree['left'], a, b)
		
		items_right = set()
		if tree['right'] is not None:
			items_right = RangeTree.search_tree(tree['right'], a, b)
		
		return items_left.union(items_right)
	
	
	def search(self, a, b):
		"""
		Wrapper for the static method.
		"""
		try:
			assert a < b
		except AssertionError:
			return set()
		
		return RangeTree.search_tree(self.tree, a, b)



