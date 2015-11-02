from django.core.cache import cache
from django.test import TestCase

from hypothesis.strategies import floats, integers, lists, tuples
from hypothesis import given

from app.ling.honeycomb import Honeycomb
from app.ling.word_matrix import WordMatrix



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
		
		for key, cell in enumerate(honeycomb.cells):
			self.assertEqual(len(cell), 3)
			self.assertEqual(cell[0], self.cells[key][0])
			self.assertEqual(cell[1], self.cells[key][1])
			self.assertGreaterEqual(cell[2], -1)
			self.assertLessEqual(cell[2], 1)
	
	
	def test_calculate_on_neighbourhoods(self):
		honeycomb = Honeycomb(self.cells)
		
		honeycomb.calculate_on_neighbourhoods(self.matrix, 20)
		self.assertEqual(len(honeycomb.cells), len(self.cells))
		
		for key, cell in enumerate(honeycomb.cells):
			self.assertEqual(len(cell), 3)
			self.assertEqual(cell[0], self.cells[key][0])
			self.assertEqual(cell[1], self.cells[key][1])
			self.assertGreaterEqual(cell[2], -1)
			self.assertLessEqual(cell[2], 1)
	
	
	@given(
		lists(
			elements=tuples(
				floats(min_value=-90.0, max_value=90.0),
				floats(min_value=-180.0, max_value=180.0)
			),
			min_size=0,
			max_size=500
		).map(
			lambda x: [list(i) for i in x]
		),
		integers(min_value=1, max_value=5000)
	)
	def test_circle_does_not_break(self, empty_cells, radius):
		honeycomb = Honeycomb(empty_cells)
		honeycomb.calculate_on_circles(self.matrix, radius)
		
		self.assertEqual(len(honeycomb.cells), len(empty_cells))
		
		for key, cell in enumerate(honeycomb.cells):
			self.assertEqual(len(cell), 3)
			self.assertEqual(cell[0], empty_cells[key][0])
			self.assertEqual(cell[1], empty_cells[key][1])
			self.assertGreaterEqual(cell[2], -1)
			self.assertLessEqual(cell[2], 1)
	
	
	@given(
		lists(
			elements=tuples(
				floats(min_value=-90.0, max_value=90.0),
				floats(min_value=-180.0, max_value=180.0)
			),
			min_size=0,
			max_size=500
		).map(
			lambda x: [list(i) for i in x]
		),
		integers(min_value=1, max_value=20)
	)
	def test_neighbourhood_does_not_break(self, empty_cells, k):
		honeycomb = Honeycomb(empty_cells)
		honeycomb.calculate_on_neighbourhoods(self.matrix, k)
		
		self.assertEqual(len(honeycomb.cells), len(empty_cells))
		
		for key, cell in enumerate(honeycomb.cells):
			self.assertEqual(len(cell), 3)
			self.assertEqual(cell[0], empty_cells[key][0])
			self.assertEqual(cell[1], empty_cells[key][1])
			self.assertGreaterEqual(cell[2], -1)
			self.assertLessEqual(cell[2], 1)



