from django.test import TestCase

from hypothesis.strategies import floats, text, lists, tuples
from hypothesis import given, assume

from app.ling.range_tree import RangeTree



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
		
		with self.assertRaises(ValueError):
			tree = RangeTree([])
		
		with self.assertRaises(ValueError):
			tree = RangeTree([1, 'one'])
	
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
	
	@given(lists(elements=tuples(
		floats(min_value=-180.0, max_value=180.0),
		text(min_size=2, max_size=3)
	)))
	def test_search_tree(self, data):
		assume(len(data) > 0)
		tree = RangeTree(data)
		
		s = set([t[1] for t in data if t[0] >= 0 and t[0] <= 42])
		self.assertEqual(tree.search(0, 42), s)



