from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase

from app.ling.word_matrix import WordMatrix
from utils.json import make_json, read_json



class PointApiTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		matrix = WordMatrix()
		
		with open('app/fixtures/berg.tsv', 'r') as f:
			matrix.load_raw(f)
		
		file_id = matrix.save()
		
		self.post = {
			'id': file_id,
			'latitude': 43,
			'longitude': 42,
			'method': 'circle',
			'parameter': 500
		}
	
	def tearDown(self):
		cache.clear()
	
	def test_good_circle(self):
		response = self.client.post(
			reverse('point_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		self.assertEqual(response.status_code, 200)
		
		content = read_json(response.content)
		self.assertEqual(len(content), 2)
		self.assertIn('origin', content)
		self.assertIn('d', content)
		
		self.assertEqual(content['origin'], 'ab')
		
		self.assertEqual(len(content['d']), 7)
		self.assertIn('os', content['d'])
		self.assertIn('ka', content['d'])
		self.assertIn('ady', content['d'])
		self.assertIn('ddo', content['d'])
		self.assertIn('ce', content['d'])
		self.assertIn('dar', content['d'])
		self.assertIn('hy', content['d'])
	
	def test_good_neighbourhood(self):
		self.post['method'] = 'neighbourhood'
		self.post['parameter'] = 4
		
		response = self.client.post(
			reverse('point_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		self.assertEqual(response.status_code, 200)
		
		content = read_json(response.content)
		self.assertEqual(len(content), 2)
		self.assertIn('origin', content)
		self.assertIn('d', content)
		
		self.assertEqual(content['origin'], 'ab')
		
		self.assertEqual(len(content['d']), 4)
		self.assertIn('os', content['d'])
		self.assertIn('ka', content['d'])
		self.assertIn('ady', content['d'])
		self.assertIn('ddo', content['d'])



