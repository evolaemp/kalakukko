from django.core.management.base import BaseCommand, CommandError

from app.models import Language

import csv


class Command(BaseCommand):
	
	help = (
		"Extracts the ISO codes present in the .tsv file "
		"that is supplied as an argument to the command. "
		"For each ISO code a language entry is created in the database, "
		"unless such already exists. "
		"It also takes care of the ISO code problem: "
		"while the language info files use ISO 639-3, "
		"the .tsv files use ISO 639-1 where available. "
		"That is why when a two-letter ISO code is encountered, "
		"it is looked up in the iso codes file, "
		"specified in the second (optional) command argument, "
		"the default value of which is `app/fixtures/iso-639-3.tab`."
	)
	
	def add_arguments(self, parser):
		parser.add_argument(
			'tsv_file',
			nargs = 1,
			type = str
		)
		parser.add_argument(
			'iso_codes_file',
			nargs = '?',
			default = 'app/fixtures/iso-639-3.tab',
			type = str
		)
	
	def handle(self, *args, **options):
		"""
		The command's main.
		"""
		
		"""Some input validation."""
		try:
			assert type(options['tsv_file']) is list
			assert len(options['tsv_file']) == 1
			assert type(options['tsv_file'][0]) is str
		except AssertionError:
			raise CommandError("Please refer to --help")
		else:
			tsv_file = options['tsv_file'][0]
		
		try:
			assert type(options['iso_codes_file']) is str
			assert len(options['iso_codes_file']) > 0
		except AssertionError:
			raise CommandError("Please refer to --help")
		else:
			self.iso_codes_file = options['iso_codes_file']
		
		
		"""Extract languages."""
		extracted = set()
		
		with open(tsv_file, 'r') as f:
			reader = csv.reader(f, delimiter='\t')
			count = -1
			
			for row in reader:
				count += 1
				if count == 0:
					continue
				
				try:
					assert row[2].find(':') > 0
					assert row[3].find(':') > 0
				except AssertionError:
					raise CommandError("File does not conform to format.")
				
				extracted.add(row[2].split(':')[0])
				extracted.add(row[3].split(':')[0])
		
		self.stdout.write("Input file is OK")
		
		
		"""Add them to the database."""
		count = 0
		
		for iso_code in extracted:
			
			if len(iso_code) == 2:  # iso 639-1
				iso_639_1 = iso_code
				try:
					iso_639_3 = self.get_iso_639_3(iso_639_1)
				except ValueError:
					self.stderr.write("Skipped "+ iso_639_1 +": ISO 639-3 code not found.")
					continue
			
			else:  # iso 639-3
				iso_639_1 = None
				iso_639_3 = iso_code
			
			try:
				Language.objects.get(iso_639_3=iso_639_3)
			except Language.DoesNotExist:
				lang = Language()
				lang.iso_639_1 = iso_639_1
				lang.iso_639_3 = iso_639_3
				lang.save()
				
				count += 1
				self.stdout.write("Added " + iso_639_3 +" to database.")
			else:
				self.stdout.write("Skipped "+ iso_639_3 +": already in database.")
		
		self.stdout.write("Done. Languages added: " + str(count))
	
	
	def get_iso_639_3(self, iso_639_1):
		"""
		Returns the ISO 639-3 code corresponding to the ISO 639-1 code given.
		Raises ValueError if the code is not found.
		"""
		iso_639_3 = None
		
		with open(self.iso_codes_file, 'r') as f:
			reader = csv.reader(f, delimiter='\t')
			count = -1
			
			for row in reader:
				count += 1
				if count == 0:
					continue
				
				if row[3] == iso_639_1:
					iso_639_3 = row[0]
					break
		
		try:
			assert iso_639_3 is not None
			assert len(iso_639_3) == 3
			assert len(iso_639_1) == 2
		except AssertionError:
			raise ValueError('Code not found.')
		
		return iso_639_3



