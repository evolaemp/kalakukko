from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase

from app.ling.word_matrix import WordMatrix
from utils.json import make_json, read_json



class HeatApiTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		matrix = WordMatrix()
		
		with open('app/fixtures/berg.tsv', 'r') as f:
			matrix.load_raw(f)
		
		file_id = matrix.save()
		
		self.post = {
			'id': file_id,
			'north': 0,
			'south': 32,
			'east': 32,
			'west': 0,
			'method': 'circle',
			'parameter': 500
		}
	
	def tearDown(self):
		cache.clear()
	
	def test_good_circle(self):
		response = self.client.post(
			reverse('heat_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		self.assertEqual(response.status_code, 200)
		
		content = read_json(response.content)
		self.assertEqual(len(content), 1)
		self.assertIn('points', content)
	
	def test_good_neighbourhood(self):
		self.post['method'] = 'neighbourhood'
		self.post['parameter'] = 4
		
		response = self.client.post(
			reverse('heat_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		self.assertEqual(response.status_code, 200)
		
		content = read_json(response.content)
		self.assertEqual(len(content), 1)
		self.assertIn('points', content)



