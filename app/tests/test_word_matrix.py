from django.core.cache import cache
from django.test import TestCase

from app.ling.word_matrix import WordMatrix



class WordMatrixTestCase(TestCase):
	def setUp(self):
		self.f = open('app/fixtures/berg.tsv', 'r')
	
	def tearDown(self):
		self.f.close()
		cache.clear()
	
	def test_load_raw(self):
		matrix = WordMatrix()
		matrix.load_raw(self.f)
		
		self.assertEqual(matrix.d[('sjd', 'sms')], (0.3487, 0.4035))
		self.assertEqual(matrix.d[('kv', 'mhr')], (0.5314, 0.2624))
		self.assertEqual(matrix.d[('mhr', 'udm')], (0.5314, 0.1520))
		self.assertEqual(matrix.d[('ddo', 'sq')], (1.0000, 0.1144))
		
		for key, value in matrix.d.items():
			self.assertIs(type(key), tuple)
			self.assertEqual(len(key), 2)
			self.assertIs(type(value), tuple)
			self.assertEqual(len(value), 2)
		
		self.assertEqual(len(matrix.d), 2346)
	
	def test_load_raw_error(self):
		matrix = WordMatrix()
		f = open('app/fixtures/languages.tab', 'r')
		
		with self.assertRaises(ValueError):
			matrix.load_raw(f)
	
	def test_save_and_load(self):
		matrix = WordMatrix()
		matrix.load_raw(self.f)
		storage_id = matrix.save()
		
		matrix = WordMatrix()
		self.assertEqual(len(matrix.d), 0)
		
		matrix.load(storage_id)
		self.assertEqual(len(matrix.d), 2346)
		
		cache.clear()
		self.assertEqual(len(matrix.d), 2346)
		
		matrix = WordMatrix()
		with self.assertRaises(ValueError):
			matrix.load(storage_id)
	
	def test_get_distances(self):
		matrix = WordMatrix()
		matrix.load_raw(self.f)
		
		self.assertEqual(matrix.get_distances('sjd', 'sms'), (0.3487, 0.4035))
		self.assertEqual(matrix.get_distances('sms', 'sjd'), (0.3487, 0.4035))
		
		self.assertEqual(matrix.get_distances('kv', 'mhr'), (0.5314, 0.2624))
		self.assertEqual(matrix.get_distances('mhr', 'kv'), (0.5314, 0.2624))
		
		self.assertEqual(matrix.get_distances('mhr', 'udm'), (0.5314, 0.1520))
		self.assertEqual(matrix.get_distances('udm', 'mhr'), (0.5314, 0.1520))
		
		self.assertEqual(matrix.get_distances('ddo', 'sq'), (1.0000, 0.1144))
		self.assertEqual(matrix.get_distances('sq', 'ddo'), (1.0000, 0.1144))



