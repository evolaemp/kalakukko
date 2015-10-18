from django.core.management.base import BaseCommand, CommandError

from app.models import Language



class Command(BaseCommand):
	
	help = (
		"Collects and stores to the database the geographical locations "
		"for the languages currently in the database. "
		"This command wants to be fed with lines of whitespace-separated "
		"ISO 639-3 code, latitude, and longitude. "
		"If you want to use another input format, "
		"use this command's code as a starting point. "
		"Warning: this command overwrites other latlng info in the database."
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
		try:
			assert type(options['file_name']) is list
			assert len(options['file_name']) == 1
			assert type(options['file_name'][0]) is str
		except AssertionError:
			raise CommandError("Please refer to --help")
		else:
			file_name = options['file_name'][0]
		
		
		with open(file_name, 'r') as f:
			
			for line in f:
				items = line.split()
				
				try:
					assert len(items) == 3
					iso_code = str(items[0])
					latitude = float(items[1])
					longitude = float(items[2])
				except (AssertionError, TypeError):
					self.stdout.write("Skipped incomprehensible line")
					continue
				
				try:
					language = Language.objects.get(iso_639_3=iso_code)
				except Language.DoesNotExist:
					self.stdout.write("Skipped "+ iso_code +": no database entry")
					continue
				
				language.latitude = latitude
				language.longitude = longitude
				language.save()
				self.stdout.write("Updated location of "+ iso_code)
		
		self.stdout.write("Harvest done")



