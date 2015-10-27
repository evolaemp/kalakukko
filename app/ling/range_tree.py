


class RangeTree:
	"""
	node: {'left': node, 'right': node, 'value': 42, 'item': None}
	"""
	
	def __init__(self, d):
		"""
		Constructor.
		"""
		try:
			leaves = sorted(d)
		except TypeError:
			raise ValueError('Unorderable values.')
		
		if len(leaves) == 0:
			raise ValueError('No values.')
		
		self.tree = RangeTree.create_tree(leaves)
	
	
	@staticmethod
	def create_tree(leaves):
		"""
		Recursively create a tree out of the leaves given.
		The leaves must be [] of (value, item,) tuples.
		"""
		if len(leaves) in (1, 2,):
			left = {
				'value': leaves[0][0],
				'item': leaves[0][1],
				'left': None,
				'right': None
			}
			
			if len(leaves) == 2:
				right = {
					'value': leaves[1][0],
					'item': leaves[1][1],
					'left': None,
					'right': None
				}
			else:
				right = None
			
			value = leaves[0][0]
		
		else:
			half = int(len(leaves) / 2)
			
			left = RangeTree.create_tree(leaves[:half])
			right = RangeTree.create_tree(leaves[half:])
			
			value = left['value']
			node = left['right']
			
			while node is not None:
				if node['value'] > value:
					value = node['value']
				node = node['right']
		
		return {
			'left': left,
			'right': right,
			'value': value
		}
	
	
	@staticmethod
	def search_tree(tree, a, b):
		"""
		Recursively search the tree given.
		"""
		if tree['value'] < a:
			if tree['right'] is None:
				return set()
			return RangeTree.search_tree(tree['right'], a, b)
		
		if tree['value'] > b:
			if tree['left'] is None:
				return set()
			return RangeTree.search_tree(tree['left'], a, b)
		
		
		if tree['left'] is None and tree['right'] is None:
			return set([tree['item']])
		
		
		items_left = set()
		if tree['left'] is not None:
			items_left = RangeTree.search_tree(tree['left'], a, b)
		
		items_right = set()
		if tree['right'] is not None:
			items_right = RangeTree.search_tree(tree['right'], a, b)
		
		return items_left.union(items_right)
	
	
	def search(self, a, b):
		"""
		Wrapper for the static method.
		"""
		try:
			assert a < b
		except AssertionError:
			return set()
		
		return RangeTree.search_tree(self.tree, a, b)



