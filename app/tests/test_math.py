from django.test import TestCase

from hypothesis.strategies import floats, lists, tuples
from hypothesis import given

from app.ling.math import get_correlation



class CorrelationsTestCase(TestCase):
	def test_pearson(self):
		self.assertEqual(get_correlation(
			[1, 2, 3, 4, 5, 6, 7],
			[1, 2, 3, 4, 5, 6, 7]
		), 1)
		
		self.assertEqual(get_correlation(
			[1, 2, 3, 4, 5, 6, 7],
			[2, 3, 4, 5, 6, 7, 8]
		), 1)
		
		self.assertEqual(get_correlation(
			[1, 2, 3],
			[0, 1, 0.5]
		), 0.5)
	
	def test_edge_cases(self):
		self.assertEqual(get_correlation([], []), 0)
		
		self.assertEqual(get_correlation([42], []), 0)
		self.assertEqual(get_correlation([], [42]), 0)
		
		self.assertEqual(get_correlation([42], [42]), 0)
	
	@given(lists(tuples(
		floats(min_value=0.0, max_value=1.0),
		floats(min_value=0.0, max_value=1.0)
	)))
	def test_hypothetically(self, data):
		a = [i[0] for i in data]
		b = [i[1] for i in data]
		
		p = get_correlation(a, b)
		
		self.assertIn(type(p), (int, float))
		self.assertGreaterEqual(p, -1)
		self.assertLessEqual(p, 1)



