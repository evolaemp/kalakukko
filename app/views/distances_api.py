from django.http import JsonResponse
from django.views.generic.base import View

from app.models import Language

import csv


class DistancesApiView(View):
	def get(self, request, slug):
		"""
		Renders {} of language: distance; the distances being from the language
		requested to all the other languages.
		Reads berg.tsv each time (for the time being).
		"""
		try:
			language = Language.objects.get(
				iso_639_3 = slug.lower()
			)
		except Language.DoesNotExist:
			return JsonResponse({
				'error': "Language not found."
			}, status=404)
		
		d = {}
		
		file_path = 'app/fixtures/berg.tsv'
		
		with open(file_path, 'r') as f:
			reader = csv.reader(f, delimiter='\t')
			count = -1
			
			for row in reader:
				count += 1
				if count == 0:
					continue
				
				another = self.extract(language, row)
				if another:
					d[another] = float(row[1])
		
		return JsonResponse({
			'distances': d
		}, status=200)
	
	def extract(self, language, row):
		code_one = row[2].split(':')[0]
		code_two = row[3].split(':')[0]
		
		another_lang = None
		
		if language.iso_639_1 == code_one:
			another_lang = self.find_language(code_two)
		elif language.iso_639_1 == code_two:
			another_lang = self.find_language(code_one)
		elif language.iso_639_3 == code_one:
			another_lang = self.find_language(code_two)
		elif language.iso_639_3 == code_two:
			another_lang = self.find_language(code_one)
		
		if another_lang:
			return another_lang.iso_639_3
		else:
			return None
	
	def find_language(self, code):
		if len(code) == 2:
			try:
				language = Language.objects.get(iso_639_1=code)
			except Language.DoesNotExist:
				return None
		else:
			try:
				language = Language.objects.get(iso_639_3=code)
			except Language.DoesNotExist:
				return None
		
		return language



