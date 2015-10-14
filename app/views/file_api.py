from django.http import JsonResponse
from django.views.generic.base import View

from app.models import Language
from app.ling.word_matrix import WordMatrix



class FileApiView(View):
	def post(self, request):
		"""
		Creates a new word matrix and stores it for subsequent API calls.
		Returns the ID of the matrix.
		
		POST
			file	# the .tsv file
		
		200:
			id,		# word matrix id
			name	# pretty file name
		
		400: error
		"""
		
		try:
			f = self.validate_file(request)
		except ValueError as error:
			return JsonResponse({'error': str(error)}, status=400)
		
		matrix = WordMatrix()
		
		try:
			matrix.load_raw(f)
		except ValueError as error:
			return JsonResponse({'error': str(error)}, status=400)
		except Exception as error:  # csv.Error
			return JsonResponse({'error': 'File unreadable.'}, status=400)
		
		matrix.save()
		
		return JsonResponse({
			'id': matrix.storage_id,
			'name': f.name
		}, status=200)
	
	
	def validate_file(self, request):
		"""
		Input validation.
		Returns the UploadedFile instance.
		"""
		try:
			assert len(request.FILES) == 1
			assert 'file' in request.FILES
		except AssertionError:
			raise ValueError('One file at a time, please.')
		
		f = request.FILES['file']
		
		try:
			assert f.size > 0
		except AssertionError:
			raise ValueError('The file is empty.')
		
		try:
			assert f.size <= 1024 * 100
		except AssertionError:
			raise ValueError('The file exceeds the 100 KB limit.')
		
		return f



