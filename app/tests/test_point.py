from django.core.cache import cache
from django.test import TestCase

from hypothesis.strategies import floats, integers
from hypothesis import given

from app.ling.map import MapError
from app.ling.point import Point
from app.ling.word_matrix import WordMatrix



class PointTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		self.matrix = WordMatrix()
		with open('app/fixtures/berg.tsv', 'r') as f:
			self.matrix.load_raw(f)
	
	
	def test_swadeshness_in_radius(self):
		elbrus = Point(43, 42)
		s = elbrus.get_swadeshness_in_radius(self.matrix, 500)
		
		self.assertEqual(len(s), 2)
		d, p = s
		
		self.assertEqual(len(d), 8*7/2)
		
		lang = ('ab', 'os', 'ka', 'ady', 'ddo', 'ce', 'hy', 'dar')
		for i in lang:
			for j in lang:
				if i == j:
					continue
				key = [i, j]
				key.sort()
				key = key[0] +','+ key[1]
				self.assertIn(key, d)
		
		self.assertLessEqual(p, 1)
		self.assertGreaterEqual(p, -1)
	
	
	def test_neighbourhood_swadeshness(self):
		elbrus = Point(43, 42)
		s = elbrus.get_swadeshness_by_nearest(self.matrix, 7)
		
		self.assertEqual(len(s), 3)
		origin, d, p = s
		
		self.assertEqual(origin, 'ab')
		
		lang = ('os', 'ka', 'ady', 'ddo', 'ce', 'hy', 'dar')
		for i in lang:
			self.assertIn(i, d)
		
		self.assertLessEqual(p, 1)
		self.assertGreaterEqual(p, -1)
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		integers(min_value=1, max_value=5000)
	)
	def test_circle_does_not_break(self, latitude, longitude, radius):
		point = Point(latitude, longitude)
		
		try:
			d, p = point.get_swadeshness_in_radius(self.matrix, radius)
		except Exception as error:
			self.assertIsInstance(error, MapError)
		else:
			self.assertIs(type(d), dict)
			self.assertLessEqual(p, 1)
			self.assertGreaterEqual(p, -1)
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		integers(min_value=1, max_value=42)
	)
	def test_neighbourhood_does_not_break(self, latitude, longitude, k):
		point = Point(latitude, longitude)
		
		try:
			origin, d, p = point.get_swadeshness_by_nearest(self.matrix, k)
		except Exception as error:
			self.assertIsInstance(error, MapError)
		else:
			self.assertIs(type(d), dict)
			self.assertLessEqual(p, 1)
			self.assertGreaterEqual(p, -1)



