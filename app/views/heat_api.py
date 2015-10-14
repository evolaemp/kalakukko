from django.http import JsonResponse
from django.views.generic.base import View

from app.ling.heat import Heat
from app.ling.word_matrix import WordMatrix

from utils.json import read_json



class HeatApiView(View):
	
	def post(self, request):
		"""
		Returns two-dimensional array of temperatures.
		
		POST
			id,			# word matrix id
			north, south, east, west	# heat boundary coords
			method,		# circle or neighbourhood
			parameter	# circle radius or neighbourhood size
		
		200:
			points: [] of [latitude, longitude, temperature]
		
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
		
		heat = Heat()
		heat.set_area(
			(post['north'], post['west'],),
			(post['south'], post['east'],)
		)
		points = heat.calculate(matrix, post['method'], post['parameter'])
		
		return JsonResponse({'points': points}, status=200)
	
	
	def validate_post(self, request_body):
		"""
		Returns validated POST or raises ValueError.
		"""
		post = read_json(request_body)
		
		try:
			assert len(post) == 7
		except AssertionError:
			raise ValueError('You cannot pass!')
		
		try:
			assert 'id' in post
			assert type(post['id']) is str
			assert len(post['id']) > 0
			assert len(post['id']) < 200
		except AssertionError:
			raise ValueError('Invalid id.')
		
		for cardinal_point in ('north', 'south', 'east', 'west',):
			try:
				assert cardinal_point in post
				post[cardinal_point] = float(post[cardinal_point])
			except (AssertionError, TypeError):
				raise ValueError('Invalid cardinal point: '+cardinal_point+'.')
		
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



