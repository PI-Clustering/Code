""" Computation of the Adjusted Mutual Information """

##### Imports
import numpy as np
import math

def mutual_info(S,U,V):
	""" Computes the Adjusted Mutual Information according to this formula : https://en.wikipedia.org/wiki/Adjusted_mutual_information

	Parameters
	----------
	S : Python set
		Represents a dataset, each element is a string
		Its format is : {string1, string2, ...}
	U : Python list of sets
		Represents a partition of S set
		Its format is : [{string1, string4,...}, {string2, string3, ...} ...]
	V : Python list of sets
		Represents another partition of S set
		Its format is : [{string2, string11,...}, {string3, string10, ...} ...]

	Returns
	-------
	M : Float
		Float that is a non-negative quantity upper bounded by the entropies HU and HV. 
		It quantifies the information shared by the two clusterings and thus can be employed as a clustering similarity measure. 
	HU : Float
		Float representing the entropy of the partitioning of U.
		Supposed to upper bound M.
	HV : Float
		Float representing the entropy of the partitioning of V.
		Supposed to upper bound M.
	

	"""

	M = np.empty((len(U), len(V)))
	N = len(S)

	# Creation of the M matrix : contigency table to denote the number of objects common to U[i] and V[j]
	for i in range(len(U)):
		for j in range(len(V)):

			#cardinal of intersection between sets
			M[i][j] = len(U[i] & V[j])

	MI = 0


	for i in range(len(U)):
		for j in range(len(V)):
			PUV = (M[i][j]/N)

			# if PUV is equal to 0 then increment MI of 0 (because x log x tends to 0 when x tends to +inf)
			if PUV != 0:
				PU = len(U[i])/N
				PV = len(V[j])/N

				value = PUV*math.log(PUV/(PU*PV))
				MI+=value

	# compute the entropy of U partitioning
	HU = 0
	for i in range(len(U)):
		HU += (len(U[i])/N)*math.log(len(U[i])/N)
	HU = -HU

	# compute the entropy of V partitioning
	HV = 0
	for i in range(len(V)):
		HV += (len(V[i])/N)*math.log(len(V[i])/N)
	HV = -HV
	
	return MI,HU,HV

def normalized_mutual_info(S,U,V):
	""" Computes a normalized version of the Adjusted Mutual Information according to the formula at the end of this page : https://en.wikipedia.org/wiki/Adjusted_mutual_information

	Parameters
	----------
	S : Python set
		Represents a dataset, each element is a string
		Its format is : {string1, string2, ...}
	U : Python list of sets
		Represents a partition of S set
		Its format is : [{string1, string4,...}, {string2, string3, ...} ...]
	V : Python list of sets
		Represents another partition of S set
		Its format is : [{string2, string11,...}, {string3, string10, ...} ...]

	Returns
	-------
	EMI : Float
		Float that takes a value of 1 when the two partitions are identical and 
		0 when the MI between two partitions equals the value expected due to chance alone
	"""

	MI,HU,HV = mutual_info(S,U,V)

	R = len(U)
	C = len(V)

	M = np.empty((len(U), len(V)))
	N = len(S)

	# Creation of the M matrix : contigency table to denote the number of objects common to U[i] and V[j]
	for i in range(R):
		for j in range(C):

			#cardinal of intersection between sets
			M[i][j] = len(U[i] & V[j])

	A = []
	
	###
	# partial sums of the contigency table (a, b)
	for i in range(R):
		a = 0
		for j in range(C):
			a += M[i][j]
		A.append(a)

	B = []

	for j in range(C):
		b = 0
		for i in range(R):
			b += M[i][j]
		B.append(b)
	###

	EMI = 0

	# computation of the EMI formula
	for i in range(R):
		for j in range(C):
			a_i = int(A[i])
			b_j = int(B[j])
			ind_start = max(1,a_i+b_j-N)

			for ind in range(ind_start, min(a_i,b_j)+1):
				# approximations with indexes can disturb the final value
				if (a_i-ind) <= 0:
					fact_ai = 1
				else:
					fact_ai = math.gamma(a_i-ind)
				if (b_j-ind) <= 0:
					fact_bj = 1
				else:
					fact_bj = math.gamma(b_j-ind)

				EMI += (math.gamma(N-a_i)/math.factorial(N))*(math.gamma(N-b_j)/math.gamma(N-a_i-b_j+ind))*(ind/N)*math.log(N*ind/(a_i*b_j))*(math.gamma(a_i)*math.gamma(b_j))/(math.factorial(ind)*fact_ai*fact_bj)

	return (MI-EMI)/(max(HU,HV)-EMI)