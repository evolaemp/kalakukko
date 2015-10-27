from django.test import TestCase

from geopy.distance import great_circle

from hypothesis.strategies import floats, integers, tuples
from hypothesis import given, assume

from app.ling.map import Map, MapError



class MapStaticTestCase(TestCase):
	"""
	For Map's static methods.
	"""
	def test_great_circle(self):
		a, b = (41.49008, -71.312796), (41.499498, -81.695391)
		self.assertEqual(
			round(Map.great_circle(a, b)),
			round(great_circle(a, b).km)
		)
		
		a, b = (42.01, 42.01), (42.02, 42.02)
		self.assertEqual(
			round(Map.great_circle(a, b)),
			round(great_circle(a, b).km)
		)
	
	
	@given(
		tuples(
			floats(min_value=-90.0, max_value=90.0), floats(min_value=-180.0, max_value=180)
		),
		tuples(
			floats(min_value=-90.0, max_value=90.0), floats(min_value=-180.0, max_value=180)
		)
	)
	def test_great_circle_hypothetically(self, a, b):
		self.assertEqual(
			round(Map.great_circle(a, b)),
			round(great_circle(a, b).km)
		)
	
	
	def test_make_tetragon(self):
		for latitude, longitude, x in [
			(0, 0, 1000), (70, 0, 2000), (42, 42, 1500),
			(-42, -42, 1500), (42, -42, 1500), (-42, 42, 1500),
		]:
			centre = (latitude, longitude)
			tetragon = Map.make_tetragon(latitude, longitude, x)
			
			self.assertGreater(tetragon['north'], latitude)
			self.assertLess(tetragon['north'], 90)
			d = great_circle(centre, (tetragon['north'], longitude)).km
			self.assertEqual(round(d), x)
			
			self.assertLess(tetragon['south'], latitude)
			self.assertGreater(tetragon['south'], -90)
			d = great_circle(centre, (tetragon['south'], longitude)).km
			self.assertEqual(round(d), x)
			
			self.assertGreater(tetragon['east'], longitude)
			self.assertLess(tetragon['east'], 180)
			d = great_circle(centre, (latitude, tetragon['east'])).km
			self.assertEqual(round(d), x)
			
			self.assertLess(tetragon['west'], longitude)
			self.assertGreater(tetragon['west'], -180)
			d = great_circle(centre, (latitude, tetragon['west'])).km
			self.assertEqual(round(d), x)
		
		for latitude, longitude, x in [(80, 0, 1500), (-80, 0, 1500)]:
			with self.assertRaises(MapError):
				Map.make_tetragon(latitude, longitude, x)
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		integers(min_value=1, max_value=5000)
	)
	def test_make_tetragon_hypothetically(self, latitude, longitude, x):
		centre = (latitude, longitude)
		
		try:
			tetragon = Map.make_tetragon(latitude, longitude, x)
		except Exception as error:
			self.assertIsInstance(error, MapError)
		else:
			self.assertGreater(tetragon['north'], latitude)
			self.assertLess(tetragon['north'], 90)
			d = great_circle(centre, (tetragon['north'], longitude)).km
			self.assertEqual(round(d), x)
			
			self.assertLess(tetragon['south'], latitude)
			self.assertGreater(tetragon['south'], -90)
			d = great_circle(centre, (tetragon['south'], longitude)).km
			self.assertEqual(round(d), x)
			
			self.assertGreater(tetragon['east'], longitude)
			d = great_circle(centre, (latitude, tetragon['east'])).km
			self.assertEqual(round(d), x)
			
			self.assertLess(tetragon['west'], longitude)
			d = great_circle(centre, (latitude, tetragon['west'])).km
			self.assertEqual(round(d), x)



class MapTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		self.map = Map()
	
	
	def test_get_nearest(self):
		iberia = self.map.get_nearest(40, 0, 3)
		self.assertEqual(iberia, ['es', 'eu', 'pt'])
		
		elbrus = self.map.get_nearest(43, 42, 8)
		self.assertEqual(elbrus, [
			'ab', 'os', 'ka', 'ady', 'ddo', 'ce', 'hy', 'dar'
		])
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		integers(min_value=1, max_value=42)
	)
	def test_get_nearest_returns(self, latitude, longitude, k):
		try:
			lang = self.map.get_in_radius(latitude, longitude, k)
		except Exception as error:
			self.assertIsInstance(error, MapError)
		else:
			self.assertIs(type(lang), set)
	
	
	def test_get_single_nearest(self):
		iberia = self.map.get_single_nearest(40, 0, 500)
		self.assertEqual(iberia, 'es')
		
		elbrus = self.map.get_single_nearest(43, 42, 500)
		self.assertEqual(elbrus, 'ab')
		
		iceland = self.map.get_single_nearest(65, -22, 500)
		self.assertEqual(iceland, 'is')
		
		volga = self.map.get_single_nearest(55, 50, 500)
		self.assertEqual(volga, 'tt')
		
		andes = self.map.get_single_nearest(-15, -70, 500)
		self.assertEqual(andes, None)
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		integers(min_value=1, max_value=5000)
	)
	def test_get_single_nearest_returns(self, latitude, longitude, radius):
		try:
			lang = self.map.get_single_nearest(latitude, longitude, radius)
		except Exception as error:
			self.assertIsInstance(error, MapError)
		else:
			try:
				self.assertIs(type(lang), str)
			except AssertionError:
				self.assertIsNone(lang)
	
	
	def test_get_in_radius(self):
		iceland = self.map.get_in_radius(65, -22, 1000)
		self.assertEqual(iceland, set(['is']))
		
		volga = self.map.get_in_radius(55, 50, 1000)
		self.assertEqual(volga, set([
			'ba', 'cv', 'mdf', 'mhr', 'myv', 'tt', 'udm'
		]))
		
		andes = self.map.get_in_radius(-15, -70, 1000)
		self.assertEqual(andes, set())
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		integers(min_value=1, max_value=5000)
	)
	def test_get_in_radius_returns(self, latitude, longitude, radius):
		try:
			lang = self.map.get_in_radius(latitude, longitude, radius)
		except Exception as error:
			self.assertIsInstance(error, MapError)
		else:
			self.assertIs(type(lang), set)



