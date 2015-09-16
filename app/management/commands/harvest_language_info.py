"""
The data source file can be found in `app/fixtures/languages.tab`.
"""
from django.core.management.base import BaseCommand, CommandError

from app.models import Language

import csv


class Command(BaseCommand):
	
	help = (
		"Collects and stores to the database the geographical locations "
		"for the languages currently in the database. "
		"Languages which are not in the database are ignored. "
		"If there is a discrepancy between file and database, "
		"the user is notified."
	)
	
	def add_arguments(self, parser):
		parser.add_argument(
			'file_name',
			nargs = 1,
			type = str
		)
	
	def handle(self, *args, **options):
		"""
		The command's main.
		"""
		"""Some input validation."""
		try:
			assert type(options['file_name']) is list
			assert len(options['file_name']) == 1
			assert type(options['file_name'][0]) is str
		except AssertionError:
			raise CommandError("Please refer to --help")
		else:
			file_name = options['file_name'][0]
		
		
		"""Do the heavy work."""
		with open(file_name, 'r') as f:
			
			count_lines = 0
			headings = []
			iso_codes = set()
			
			for line in csv.reader(f, delimiter='\t'):
				
				if count_lines:
					d = {}
					for i, heading in enumerate(headings):
						d[heading] = line[i]
					
					if not d['iso']:
						continue
					
					if d['iso'] not in iso_codes:
						self.enrich(d)
						iso_codes.add(d['iso'])
				
				else:
					headings = line
				
				count_lines += 1
		
		"""Done."""
		self.stdout.write("Harvest done")
	
	
	def enrich(self, d):
		"""
		If the database contains an entry for the language in d,
		then the entry is enriched.
		"""
		try:
			language = Language.objects.get(iso_639_3=d['iso'])
		except Language.DoesNotExist:
			return
		
		is_updated = False
		
		"""Latitude."""
		try:
			assert float(d['lat']) == language.latitude
		except AssertionError:
			if language.latitude is None:
				language.latitude = float(d['lat'])
				is_updated = True
			else:
				self.stderr.write((
					"Discrepancy found: language " + language.iso_639_3 + " "
					"has latitude of "+ str(language.latitude) +" in the database "
					"but latitude of "+ str(d['lat']) +" in the file. "
					"You will have to fix that manually."
				))
		
		"""Longitude."""
		try:
			assert float(d['long']) == language.longitude
		except AssertionError:
			if language.longitude is None:
				language.longitude = float(d['long'])
				is_updated = True
			else:
				self.stderr.write((
					"Discrepancy found: language " + language.iso_639_3 + " "
					"has longitude of "+ str(language.longitude) +" in the database "
					"but longitude of "+ str(d['long']) +" in the file. "
					"You will have to fix that manually."
				))
		
		"""Be friendly to humanoid users."""
		if is_updated:
			language.save()
			self.stdout.write("Updated language " + language.iso_639_3)



