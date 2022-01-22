""" Computation of the Adjusted Random Index """

def adjusted_random_index(S, X, Y):
	""" Computes the Adjusted Random Index according to this formula : https://en.wikipedia.org/wiki/Rand_index

	Parameters
	----------
	S : Python set
		Represents a dataset, each element is a string
		Its format is : {string1, string2, ...}
	X : Python list of sets
		Represents a partition of S set
		Its format is : [{string1, string4,...}, {string2, string3, ...} ...]
	Y : Python list of sets
		Represents another partition of S set
		Its format is : [{string2, string11,...}, {string3, string10, ...} ...]

	Returns
	-------
	ari : Float
		Float between 0 and 1 representing the value of the adjusted random index.
		The bigger the value the more similar the clustering between X and Y is.

	"""
	
	a = 0 # the number of pairs of elements in S that are in the same subset in X and in the same subset in Y
	b = 0 # the number of pairs of elements in S that are in different subsets in X and in different subsets in Y
	c = 0 # the number of pairs of elements in S that are in the same subset in X and in different subsets in Y
	d = 0 # the number of pairs of elements in S that are in different subsets in X and in the same subset in Y

	# pairs already run through
	already_pairs = set()

	# iterate through each element of S twice to compare each pairs
	for elt in S:
		for elt2 in S:
			same_X = False
			same_Y = False

			# if this pair was not already run through
			if elt != elt2 and {elt,elt2} not in already_pairs:

				# iterate through each different sets of X
				for x in X:
					if elt in x and elt2 in x:
						same_X = True

				# iterate through each different sets of Y
				for y in Y:
					if elt in y and elt2 in y:
						same_Y = True

				if same_X and same_Y:
					a+=1
				elif not(same_X) and not(same_Y):
					b+=1
				elif same_X and not(same_Y):
					c+=1
				else:
					d+=1

				# add the pair to pairs already run through
				already_pairs.add(frozenset({elt,elt2}))

	# compute Adjusted Rand Index value
	ari = (a+b)/(a+b+c+d)

	return ari