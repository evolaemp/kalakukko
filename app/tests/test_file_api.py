from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase

from app.ling.word_matrix import WordMatrix
from utils.json import read_json



class FileApiTestCase(TestCase):
	fixtures = ['languages.json']
	
	def tearDown(self):
		cache.clear()
	
	def test_good_upload(self):
		with open('app/fixtures/berg.tsv', 'r') as f:
			response = self.client.post(
				reverse('file_api'),
				{'file': f}
			)
		
		self.assertEqual(response.status_code, 200)
		
		d = read_json(response.content)
		self.assertEqual(len(d), 2)
		
		self.assertIn('id', d)
		self.assertGreater(len(d['id']), 0)
		
		self.assertIn('name', d)
		self.assertEqual(d['name'], 'berg.tsv')
		
		matrix = WordMatrix()
		matrix.load(d['id'])
		self.assertEqual(len(matrix.d), 2346)
	
	def test_bad_upload(self):
		with open('app/fixtures/languages.json', 'r') as f:
			response = self.client.post(
				reverse('file_api'),
				{'file': f}
			)
		
		self.assertEqual(response.status_code, 400)
		
		d = read_json(response.content)
		self.assertEqual(len(d), 1)
		
		self.assertIn('error', d)
	
	def test_empty_upload(self):
		response = self.client.post(reverse('file_api'))
		self.assertEqual(response.status_code, 400)
		
		d = read_json(response.content)
		self.assertEqual(len(d), 1)
		
		self.assertIn('error', d)



