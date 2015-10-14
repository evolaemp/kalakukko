import math



def get_correlation(a, b):
	"""
	Calculates the Pearson correlation coefficient for the populations given.
	Returns 0 if the populations cannot be correlated.
	"""
	try:
		assert len(a) == len(b) > 0
	except AssertionError:
		return 0
	
	size = len(a)
	
	mean_a = sum(a) / size
	mean_b = sum(b) / size
	
	"""
	cov(X, Y) = E[(X - µX)(Y - µY)]
	var(X) = E[(X - µ)^2]
	In our case the probablities = 1/size.
	"""
	cov = 0
	
	var_a = 0
	var_b = 0
	
	for i in range(0, size):
		cov += (a[i] - mean_a) * (b[i] - mean_b)
		var_a += pow(a[i] - mean_a, 2)
		var_b += pow(b[i] - mean_b, 2)
	
	cov = cov / size
	
	var_a = var_a / size
	var_b = var_b / size
	
	"""
	σ(X) = sqrt(var(X))
	When 0, there is no correlation.
	"""
	sigma_a = math.sqrt(var_a)
	sigma_b = math.sqrt(var_b)
	
	try:
		assert sigma_a > 0
		assert sigma_b > 0
	except AssertionError:
		return 0
	
	"""
	p(X, Y) = cov(X, Y) / σ(X)σ(Y)
	"""
	p = cov / (sigma_a * sigma_b)
	return p



