from django.test import TestCase

from app.ling.map import Map



class MapTestCase(TestCase):
	fixtures = ['languages.json']
	
	def setUp(self):
		self.map = Map()
	
	def test_get_nearest(self):
		iberia = self.map.get_nearest(40, 0, 3)
		self.assertEqual(iberia, ['es', 'eu', 'pt'])
		
		elbrus = self.map.get_nearest(43, 42, 8)
		self.assertEqual(elbrus, [
			'ab', 'os', 'ka', 'ady', 'ddo', 'ce', 'hy', 'dar'
		])
	
	def test_get_in_radius(self):
		iceland = self.map.get_in_radius(65, -22, 1000)
		self.assertEqual(iceland, set(['is']))
		
		volga = self.map.get_in_radius(55, 50, 1000)
		self.assertEqual(volga, set([
			'ba', 'cv', 'mdf', 'mhr', 'myv', 'tt', 'udm'
		]))
		
		andes = self.map.get_in_radius(-15, -70, 1000)
		self.assertEqual(andes, set())



