from django.http import JsonResponse
from django.views.generic.base import View

from app.ling.point import Point
from app.ling.word_matrix import WordMatrix

from utils.json import read_json



class PointApiView(View):
	
	def post(self, request):
		"""
		Returns the analysis for the requested point.
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
		
		point = Point(post['latitude'], post['longitude'])
		d = point.get_swadeshness(matrix, nearest=5)
		
		return JsonResponse({'d': d}, status=200)
	
	
	def validate_post(self, request_body):
		"""
		Returns validated POST or raises ValueError.
		"""
		post = read_json(request_body)
		
		try:
			assert len(post) == 3
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
			assert 'latitude' in post
			post['latitude'] = float(post['latitude'])
		except (AssertionError, TypeError):
			raise ValueError('Invalid latitude.')
		
		try:
			assert 'longitude' in post
			post['longitude'] = float(post['longitude'])
		except (AssertionError, TypeError):
			raise ValueError('Invalid longitude.')
		
		return post



