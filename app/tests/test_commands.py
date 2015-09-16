from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from app.management.commands import extract_languages
from app.models import Language



class ExtractLanguagesTestCase(TestCase):
	def setUp(self):
		self.stdout = StringIO()
		self.stderr = StringIO()
		
		self.args = ['app/fixtures/berg.tsv']
		self.opts = {'stdout': self.stdout, 'stderr': self.stderr}
	
	def test_nargs(self):
		for args in (
				[],
				['app/fixtures/berg.tsv'] * 3,
			):
			with self.assertRaises(CommandError):
				call_command('extract_languages', *args, **self.opts)
			self.assertEqual(Language.objects.count(), 0)
		
		args = [
			'app/fixtures/berg.tsv',
			'app/fixtures/iso-639-3.tab'
		]
		call_command('extract_languages', *args, **self.opts)
		self.assertEqual('', self.stderr.getvalue())
	
	def test_get_iso_639_3(self):
		command = extract_languages.Command()
		command.iso_codes_file = 'app/fixtures/iso-639-3.tab'
		
		self.assertEqual(command.get_iso_639_3('bg'), 'bul')
		self.assertEqual(command.get_iso_639_3('de'), 'deu')
		self.assertEqual(command.get_iso_639_3('en'), 'eng')
		self.assertEqual(command.get_iso_639_3('et'), 'est')
		self.assertEqual(command.get_iso_639_3('fi'), 'fin')
		
		for code in ('', 'k', 'krl',):
			with self.assertRaises(ValueError):
				command.get_iso_639_3(code)
	
	def test_command(self):
		call_command('extract_languages', *self.args, **self.opts)
		self.assertEqual('', self.stderr.getvalue())
		
		self.assertEqual(Language.objects.count(), 69)
		self.assertIn('Languages added: 69', self.stdout.getvalue())
		
		fin = Language.objects.get(iso_639_3='fin')
		self.assertEqual(fin.iso_639_1, 'fi')
		
		isl = Language.objects.get(iso_639_3='isl')
		self.assertEqual(isl.iso_639_1, 'is')
		
		krl = Language.objects.get(iso_639_3='krl')
		self.assertEqual(krl.iso_639_1, None)



class HarvestLanguageInfoTestCase(TestCase):
	def setUp(self):
		out = StringIO()
		
		args = ['app/fixtures/berg.tsv']
		opts = {'stdout': out}
		
		call_command('extract_languages', *args, **opts)
		
		self.stdout = StringIO()
		self.stderr = StringIO()
		
		self.args = ['app/fixtures/languages.tab']
		self.opts = {'stdout': self.stdout, 'stderr': self.stderr}
	
	def test_nargs(self):
		for args in (
				[],
				['app/fixtures/languages.tab'] * 2,
				['app/fixtures/languages.tab'] * 3,
			):
			with self.assertRaises(CommandError):
				call_command('harvest_language_info', *args, **self.opts)
	
	def test_command(self):
		call_command('harvest_language_info', *self.args, **self.opts)
		self.assertEqual('', self.stderr.getvalue())
		
		self.assertEqual(Language.objects.count(), 69)
		
		ain = Language.objects.get(iso_639_3='ain')
		self.assertEqual(ain.latitude, 43.0)
		self.assertEqual(ain.longitude, 143.0)
		
		fin = Language.objects.get(iso_639_3='fin')
		self.assertEqual(fin.latitude, 62.0)
		self.assertEqual(fin.longitude, 25.0)
		
		isl = Language.objects.get(iso_639_3='isl')
		self.assertEqual(isl.latitude, 65.0)
		self.assertEqual(isl.longitude, -17.0)
		
		krl = Language.objects.get(iso_639_3='krl')
		self.assertEqual(krl.latitude, 64.0)
		self.assertEqual(krl.longitude, 32.0)



