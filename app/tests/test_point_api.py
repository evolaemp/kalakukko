from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase

from hypothesis.strategies import floats, integers, sampled_from
from hypothesis import given

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
		self.assertIn('d', content)
		self.assertIn('p', content)
		
		lang = ('ab', 'os', 'ka', 'ady', 'ddo', 'ce', 'hy', 'dar')
		for i in lang:
			for j in lang:
				if i == j:
					continue
				key = [i, j]
				key.sort()
				key = key[0] +','+ key[1]
				self.assertIn(key, content['d'])
		self.assertEqual(len(content['d']), 8*7/2)
		
		self.assertLessEqual(content['p'], 1)
		self.assertGreaterEqual(content['p'], -1)
	
	
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
		self.assertEqual(len(content), 3)
		self.assertIn('origin', content)
		self.assertIn('d', content)
		self.assertIn('p', content)
		
		self.assertEqual(content['origin'], 'ab')
		
		self.assertEqual(len(content['d']), 4)
		self.assertIn('os', content['d'])
		self.assertIn('ka', content['d'])
		self.assertIn('ady', content['d'])
		self.assertIn('ddo', content['d'])
	
	
	@given(
		floats(min_value=-90.0, max_value=90.0),
		floats(min_value=-180.0, max_value=180.0),
		sampled_from(('circle', 'neighbourhood')),
		integers(min_value=1)
	)
	def test_it_does_not_break(self, latitude, longitude, method, parameter):
		self.post['latitude'] = latitude
		self.post['longitude'] = longitude
		self.post['method'] = method
		self.post['parameter'] = parameter
		
		response = self.client.post(
			reverse('point_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		
		try:
			self.assertEqual(response.status_code, 200)
		except AssertionError:
			self.assertEqual(response.status_code, 400)
			content = read_json(response.content)
			self.assertEqual(len(content), 1)
			self.assertIn('error', content)



