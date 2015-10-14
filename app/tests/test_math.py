from django.test import TestCase

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



