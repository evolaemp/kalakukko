from django.core.cache import cache
from django.test import TestCase

from app.ling.heat import Heat
from app.ling.word_matrix import WordMatrix

from datetime import datetime, timedelta



class HeatTestCase(TestCase):
	fixtures = ['languages.json']
	
	def tearDown(self):
		cache.clear()
	
	
	def test_set_area(self):
		heat = Heat()
		
		heat.set_area([0, 0], [32, 32])
		self.assertEqual(len(heat.points), 1024)
		self.assertEqual(heat.points[0], [0, 0])
		self.assertEqual(heat.points[1023], [32, 32])
		
		heat.set_area([-32, -32], [0, 0])
		self.assertEqual(len(heat.points), 1024)
		self.assertEqual(heat.points[0], [-32, -32])
		self.assertEqual(heat.points[1023], [0, 0])
		
		heat.set_area([-16, -16], [16, 16])
		self.assertEqual(len(heat.points), 1024)
		self.assertEqual(heat.points[0], [-16, -16])
		self.assertEqual(heat.points[1023], [16, 16])
	
	
	def test_calculate(self):
		matrix = WordMatrix()
		with open('app/fixtures/berg.tsv', 'r') as f:
			matrix.load_raw(f)
		
		heat = Heat()
		heat.set_area([0, 0], [32, 32])
		
		a = datetime.now()
		heat.calculate(matrix, 'circle', 500)
		b = datetime.now()
		c = b - a
		print(c.total_seconds())



