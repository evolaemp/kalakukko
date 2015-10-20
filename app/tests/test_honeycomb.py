from django.core.cache import cache
from django.test import TestCase

from app.ling.honeycomb import Honeycomb
from app.ling.word_matrix import WordMatrix

from datetime import datetime, timedelta



class HoneycombTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		self.matrix = WordMatrix()
		with open('app/fixtures/berg.tsv', 'r') as f:
			self.matrix.load_raw(f)
		
		self.cells = [[65, -22], [55, 50], [-15, -70]]
	
	def tearDown(self):
		cache.clear()
	
	def test_calculate_on_circles(self):
		honeycomb = Honeycomb(self.cells)
		
		honeycomb.calculate_on_circles(self.matrix, 1000)
		self.assertEqual(len(honeycomb.cells), len(self.cells))
		
		for cell in honeycomb.cells:
			self.assertEqual(len(cell), 3)
	
	def test_calculate(self):
		honeycomb = Honeycomb(self.cells)
		
		honeycomb.calculate(self.matrix, 'neighbourhood', 1000)
		self.assertEqual(len(honeycomb.cells), len(self.cells))
	
	def skip_calculate(self):
		cells = [[i, j] for i in range(-45, 46) for j in range(0, 90)]
		print(len(cells))
		honeycomb = Honeycomb(cells)
		
		a = datetime.now()
		honeycomb.calculate(self.matrix, 'circle', 500)
		b = datetime.now()
		c = b - a
		print(c.total_seconds())



