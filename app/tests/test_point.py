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
	
	def test_circle_swadeshness(self):
		elbrus = Point(43, 42)
		s = elbrus.get_swadeshness(self.matrix, 'circle', 500)
		
		self.assertEqual(len(s), 3)
		self.assertEqual(s[0], 'ab')
		
		self.assertEqual(len(s[1]), 7)
		
		self.assertLessEqual(s[2], 1)
		self.assertGreaterEqual(s[2], -1)



