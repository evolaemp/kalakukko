from django.http import JsonResponse
from django.views.generic.base import View

from app.ling.honeycomb import Honeycomb
from app.ling.word_matrix import WordMatrix

from utils.json import read_json



class HoneycombApiView(View):
	
	def post(self, request):
		"""
		Returns two-dimensional array of temperatures.
		
		POST
			id,			# word matrix id
			cells,		# [] of [latitude, longitude]
			method,		# circle or neighbourhood
			parameter	# circle radius or neighbourhood size
		
		200:
			cells: [] of [latitude, longitude, temperature]
		
		400: error
		404: error		# file not found
		"""
		
		try:
			post = self.validate_post(request.body)
		except ValueError as error:
			return JsonResponse({'error': str(error)}, status=400)
		
		
		matrix = WordMatrix()
		
		try:
			matrix.load(post['id'])
		except ValueError:
			return JsonResponse({
				'error': 'The file has expired. Please re-upload.'
			}, status=404)
		
		
		honeycomb = Honeycomb(post['cells'])
		
		if post['method'] == 'circle':
			honeycomb.calculate_on_circles(matrix, post['parameter'])
		else:
			honeycomb.calculate_on_neighbourhoods(matrix, post['parameter'])
		
		return JsonResponse({'cells': honeycomb.cells}, status=200)
	
	
	def validate_post(self, request_body):
		"""
		Returns validated POST or raises ValueError.
		"""
		post = read_json(request_body)
		
		try:
			assert len(post) == 4
		except AssertionError:
			raise ValueError('You cannot pass!')
		
		try:
			assert 'id' in post
			assert type(post['id']) is str
			assert len(post['id']) > 0
			assert len(post['id']) < 200
		except AssertionError:
			raise ValueError('Invalid id.')
		
		try:
			assert 'cells' in post
			assert type(post['cells']) is list
			assert len(post['cells']) <= 10000
			for cell in post['cells']:
				assert type(cell) is list
				assert len(cell) == 2
		except AssertionError:
			raise ValueError('Invalid cells.')
		
		try:
			assert 'method' in post
			assert type(post['method']) is str
			assert post['method'] in ('circle', 'neighbourhood',)
		except AssertionError:
			raise ValueError('Invalid method.')
		
		try:
			assert 'parameter' in post
			assert type(post['parameter']) is int
			assert post['parameter'] > 0
		except AssertionError:
			raise ValueError('Invalid parameter.')
		
		return post



