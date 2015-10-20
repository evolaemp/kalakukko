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
		self.assertEqual(len(s[0]), 8*7/2)
		
		lang = ('ab', 'os', 'ka', 'ady', 'ddo', 'ce', 'hy', 'dar')
		for i in lang:
			for j in lang:
				if i == j:
					continue
				key = [i, j]
				key.sort()
				key = key[0] +','+ key[1]
				self.assertIn(key, s[0])
		
		self.assertLessEqual(s[1], 1)
		self.assertGreaterEqual(s[1], -1)
	
	def test_circle_swadeshness(self):
		elbrus = Point(43, 42)
		s = elbrus.get_swadeshness(self.matrix, 'circle', 500)
		
		self.assertEqual(len(s), 3)
		self.assertEqual(s[0], 'ab')
		
		self.assertEqual(len(s[1]), 7)
		
		self.assertLessEqual(s[2], 1)
		self.assertGreaterEqual(s[2], -1)



