from django.core.cache import cache
from django.test import TestCase

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



