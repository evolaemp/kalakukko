from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase

from hypothesis.strategies import floats, integers, lists, sampled_from, tuples
from hypothesis import given

from app.ling.word_matrix import WordMatrix
from utils.json import make_json, read_json



class HoneycombApiTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		matrix = WordMatrix()
		
		with open('app/fixtures/berg.tsv', 'r') as f:
			matrix.load_raw(f)
		
		file_id = matrix.save()
		
		self.post = {
			'id': file_id,
			'cells': [[65, -22], [55, 50], [-15, -70]],
			'method': 'circle',
			'parameter': 1000
		}
	
	def tearDown(self):
		cache.clear()
	
	
	def test_good_circle(self):
		response = self.client.post(
			reverse('honeycomb_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		self.assertEqual(response.status_code, 200)
		
		content = read_json(response.content)
		self.assertEqual(len(content), 1)
		self.assertIn('cells', content)
		self.assertEqual(len(content['cells']), len(self.post['cells']))
		
		for key, cell in enumerate(content['cells']):
			self.assertEqual(len(cell), 3)
			self.assertEqual(cell[0], self.post['cells'][key][0])
			self.assertEqual(cell[1], self.post['cells'][key][1])
			self.assertGreaterEqual(cell[2], -1)
			self.assertLessEqual(cell[2], 1)
	
	
	def test_good_neighbourhood(self):
		self.post['method'] = 'neighbourhood'
		self.post['parameter'] = 4
		
		response = self.client.post(
			reverse('honeycomb_api'),
			make_json(self.post),
			content_type='application/octet-stream'
		)
		self.assertEqual(response.status_code, 200)
		
		content = read_json(response.content)
		self.assertEqual(len(content), 1)
		self.assertIn('cells', content)
		self.assertEqual(len(content['cells']), len(self.post['cells']))
		
		for key, cell in enumerate(content['cells']):
			self.assertEqual(len(cell), 3)
			self.assertEqual(cell[0], self.post['cells'][key][0])
			self.assertEqual(cell[1], self.post['cells'][key][1])
			self.assertGreaterEqual(cell[2], -1)
			self.assertLessEqual(cell[2], 1)
	
	
	@given(
		lists(max_size=500, elements=tuples(
			floats(min_value=-90.0, max_value=90.0),
			floats(min_value=-180.0, max_value=180.0)
		)),
		sampled_from(('circle', 'neighbourhood', 'nonsense')),
		integers(min_value=1)
	)
	def test_it_does_not_break(self, cells, method, parameter):
		self.post['cells'] = cells
		self.post['method'] = method
		self.post['parameter'] = parameter
		
		response = self.client.post(
			reverse('honeycomb_api'),
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
		
		else:
			content = read_json(response.content)
			self.assertEqual(len(content), 1)
			
			self.assertIn('cells', content)
			self.assertEqual(len(content['cells']), len(cells))
			
			for key, cell in enumerate(content['cells']):
				self.assertEqual(len(cell), 3)
				self.assertEqual(cell[0], cells[key][0])
				self.assertEqual(cell[1], cells[key][1])
				self.assertGreaterEqual(cell[2], -1)
				self.assertLessEqual(cell[2], 1)



