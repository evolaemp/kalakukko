from django.test import TestCase

from app.ling.map import Map
from app.ling.map import RangeTree



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
	
	def test_get_single_nearest(self):
		iberia = self.map.get_single_nearest(40, 0, 500)
		self.assertEqual(iberia, 'es')
		
		elbrus = self.map.get_single_nearest(43, 42, 500)
		self.assertEqual(elbrus, 'ab')
		
		iceland = self.map.get_single_nearest(65, -22, 500)
		self.assertEqual(iceland, 'is')
		
		volga = self.map.get_single_nearest(55, 50, 500)
		self.assertEqual(volga, 'tt')
		
		andes = self.map.get_single_nearest(-15, -70, 500)
		self.assertEqual(andes, None)
	
	def test_get_in_radius(self):
		iceland = self.map.get_in_radius(65, -22, 1000)
		self.assertEqual(iceland, set(['is']))
		
		volga = self.map.get_in_radius(55, 50, 1000)
		self.assertEqual(volga, set([
			'ba', 'cv', 'mdf', 'mhr', 'myv', 'tt', 'udm'
		]))
		
		andes = self.map.get_in_radius(-15, -70, 1000)
		self.assertEqual(andes, set())



class RangeTreeTestCase(TestCase):
	def test_init(self):
		data_raw = [(3, 'three'), (1, 'one'), (2, 'two')]
		data_gut = [(1, 'one'), (2, 'two'), (3, 'three')]
		tree = RangeTree(data_raw)
		self.assertEqual(tree.tree, RangeTree.create_tree(data_gut))
		
		data_raw = [(42.0, 'float'), (-42, 'negative'), (0, 'zero')]
		data_gut = [(-42, 'negative'), (0, 'zero'), (42.0, 'float')]
		tree = RangeTree(data_raw)
		self.assertEqual(tree.tree, RangeTree.create_tree(data_gut))
	
	def test_create_tree_of_three(self):
		data = [(1, 'one'), (2, 'two'), (3, 'three')]
		tree = RangeTree.create_tree(data)
		
		self.assertEqual(tree['left']['left'], {
			'left': None, 'right': None, 'value': 1, 'item': 'one'
		})
		
		self.assertEqual(tree['right']['left'], {
			'left': None, 'right': None, 'value': 2, 'item': 'two'
		})
		self.assertEqual(tree['right']['right'], {
			'left': None, 'right': None, 'value': 3, 'item': 'three'
		})
		self.assertEqual(tree['right'], {
			'left': tree['right']['left'],
			'right': tree['right']['right'],
			'value': 2
		})
		
		self.assertEqual(tree, {
			'left': tree['left'],
			'right': tree['right'],
			'value': 1
		})
	
	def test_create_tree_of_four(self):
		data = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
		tree = RangeTree.create_tree(data)
		
		self.assertEqual(tree['left']['left'], {
			'left': None, 'right': None, 'value': 1, 'item': 'one'
		})
		self.assertEqual(tree['left']['right'], {
			'left': None, 'right': None, 'value': 2, 'item': 'two'
		})
		self.assertEqual(tree['left'], {
			'left': tree['left']['left'],
			'right': tree['left']['right'],
			'value': 1
		})
		
		self.assertEqual(tree['right']['left'], {
			'left': None, 'right': None, 'value': 3, 'item': 'three'
		})
		self.assertEqual(tree['right']['right'], {
			'left': None, 'right': None, 'value': 4, 'item': 'four'
		})
		self.assertEqual(tree['right'], {
			'left': tree['right']['left'],
			'right': tree['right']['right'],
			'value': 3
		})
		
		self.assertEqual(tree, {
			'left': tree['left'],
			'right': tree['right'],
			'value': 2
		})
	
	def test_search_tree_of_three(self):
		data = [(1, 'one'), (2, 'two'), (3, 'three')]
		tree = RangeTree.create_tree(data)
		
		items = RangeTree.search_tree(tree, 1.5, 2.5)
		self.assertEqual(items, set(['two']))
		
		items = RangeTree.search_tree(tree, 0, 4)
		self.assertEqual(items, set(['one', 'two', 'three']))
		
		items = RangeTree.search_tree(tree, 42, 60)
		self.assertEqual(items, set())
	
	def test_search_tree_of_four(self):
		data = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
		tree = RangeTree.create_tree(data)
		
		items = RangeTree.search_tree(tree, 1.5, 2.5)
		self.assertEqual(items, set(['two']))
		
		items = RangeTree.search_tree(tree, 1, 4)
		self.assertEqual(items, set(['one', 'two', 'three', 'four']))
		
		items = RangeTree.search_tree(tree, 42, 60)
		self.assertEqual(items, set())



