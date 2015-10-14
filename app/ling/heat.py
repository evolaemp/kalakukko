from app.ling.map import Map
from app.ling.math import get_correlation

import math



class Heat:
	"""
	Main purpose: to calculate the heat in an area, done in 4 steps:
	(1) Calculate the dimensions of the rectangle that will be heated.
	(2) Create list of points, each with its coordinates.
	(3) Loop over the points and calculate the temperature of each.
	"""
	
	def __init__(self):
		"""
		Constructor.
		"""
		self.points_on_side = 32  # 1024 points
		self.points = []
	
	
	def set_area(self, A, B):
		"""
		Sets the area of the rectangle which is to be heated.
		A is the upper left corner and B is the lower right corner.
		Performs steps (1) and (2).
		"""
		A = (math.ceil(A[0]), math.floor(A[1]),)
		B = (math.floor(B[0]), math.ceil(B[1]),)
		
		width = abs(B[1] - A[1])
		height = abs(B[0] - A[0])
		
		assert width > 0
		assert height > 0
		
		bigger_side = width if width > height else height
		d = bigger_side / (self.points_on_side - 1)
		
		if bigger_side == width:
			start_latitude = A[0] - (width - height) / 2
			start_longitude = A[1]
		else:
			start_latitude = A[0]
			start_longitude = A[1] - (height - width) / 2
		
		self.points = []
		
		for i in range(0, self.points_on_side):
			for j in range(0, self.points_on_side):
				self.points.append([
					start_latitude + i * d,
					start_longitude + j * d
				])
		
		assert len(self.points) == pow(self.points_on_side, 2)
	
	
	def calculate(self, word_matrix, method, parameter):
		"""
		Performs step (3).
		"""
		try:
			assert method in ('circle', 'neighbourhood',)
		except AssertionError:
			raise ValueError('Swadeshness needs its parameter.')
		
		planet = Map()
		
		for point in self.points:
			origin = planet.get_nearest(point[0], point[1], 1)[0]
			
			if method == 'circle':
				languages = planet.get_in_radius(point[0], point[1], parameter)
			else:
				languages = planet.get_nearest(point[0], point[1], parameter+1)
			
			a, b = [], []
			for language in languages:
				distance_pair = word_matrix.get_distances(origin, language)
				if distance_pair is not None:
					a.append(distance_pair[0])
					b.append(distance_pair[1])
			
			point.append(get_correlation(a, b))
		
		return self.points



