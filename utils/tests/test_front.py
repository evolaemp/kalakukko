"""
This TestCase lives in the utils module so that the selenium tests are separate
from the other unit tests. Thus it is easy to only run the selenium tests or
not to run them (as we would not want in a server deployment).
"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver

from utils.json import make_json

import time



class FrontTestCase(StaticLiveServerTestCase):
	fixtures = ['languages.json']
	
	@classmethod
	def setUpClass(cls):
		super(FrontTestCase, cls).setUpClass()
		cls.se = WebDriver()
	
	@classmethod
	def tearDownClass(cls):
		cls.se.quit()
		super(FrontTestCase, cls).tearDownClass()
	
	def _upload_file(self):
		"""
		Hack around Selenium's inability to process our invisible input.
		"""
		with open('app/fixtures/berg.tsv', 'r') as f:
			lines = make_json(f.readlines())
		
		self.se.execute_script((
			'var berg = new File('+ lines +', "berg.tsv"); '
			'var c = app.controllers.getMainController(); '
			'c.uploadFile(berg); '
			'c.fileInput.setSource("berg.tsv"); '
		))
		
		time.sleep(1)
	
	def test_controls(self):
		self.se.get(self.live_server_url)
		
		controls = self.se.find_element_by_css_selector('.controls')
		self.assertEqual(controls.is_displayed(), True)
		controls.find = controls.find_element_by_css_selector
		
		self.assertFalse(controls.find('.parameter-input').is_displayed())
		self.assertFalse(controls.find('.method-select').is_displayed())
		self.assertFalse(controls.find('.mode-select').is_displayed())
		
		self._upload_file()
		
		self.assertTrue(controls.find('.parameter-input').is_displayed())
		self.assertTrue(controls.find('.method-select').is_displayed())
		self.assertTrue(controls.find('.mode-select').is_displayed())
		
		controls.find('.file-button').click()
		
		self.assertFalse(controls.find('.parameter-input').is_displayed())
		self.assertFalse(controls.find('.method-select').is_displayed())
		self.assertFalse(controls.find('.mode-select').is_displayed())
	
	def test_point_mode(self):
		self.se.get(self.live_server_url)
		self.se.find = self.se.find_element_by_css_selector
		self._upload_file()
		
		actions = ActionChains(self.se)
		actions.move_to_element(self.se.find('.map'))
		actions.click()
		actions.perform()
		time.sleep(1)
		
		self.assertTrue(self.se.find('.map .circle').is_displayed())
		self.assertTrue(self.se.find('.draggable').is_displayed())
	
	def test_honeycomb_mode(self):
		self.se.get(self.live_server_url)
		self.se.find = self.se.find_element_by_css_selector
		self._upload_file()
		
		self.se.find('button[data-value=heat]').click()
		time.sleep(1)
		
		self.assertTrue(self.se.find('.honeycomb').is_displayed())



