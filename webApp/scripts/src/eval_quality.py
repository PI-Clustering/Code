##### Imports
from decimal import Decimal

import numpy as np
import math
import hdbscan

import matplotlib.pyplot as plt

import os
import csv

from ..settings import global_variable
from .clustering_algo import to_format, max_labs_props, compute_similarities, dist
from ...models import DataPoint, Benchmark

def eval_quality():

    """
    This funciton, using global variables, will 
    """

    bm = global_variable("bm")
    cluster = global_variable("cluster")

    # Let's get the data we will use to test the model
    N = 10000 #We take 10000 node as it is sufficient and efficient enough
    unused = global_variable("unused")
    total_unused = sum(unused.values())
    test_data = dict()
    p = min(N / total_unused,1)

    # We then select almost 10 000 node using probability to simulate efficiently
    # the uniform choice over all nodes
    for node in unused:
        nb = np.random.binomial(unused[node], p)
        if nb != 0:
            test_data[node] = nb
            unused[node] -= nb #The data being used, we remove it from the set of unused data
    global_variable("unused", unused)

   
    ref_node = max_labs_props(test_data)
    similarities_dict = compute_similarities(test_data, ref_node)
    computed_measures, ecrasage = to_format(similarities_dict, test_data)

    print(len(computed_measures))
    print("hdbscan model:")
    predictions = hdbscan.HDBSCAN().fit_predict(computed_measures)
    print("done.")

    # We build the clustering of HDBScan
    Y = [set() for _ in range(len(set(predictions)))]
    j = 0
    for node in test_data:
        amount = test_data[node] // (10**ecrasage)
        Y[predictions[j]].add(node)
        j += amount
    
    # Now, for each iteration, we put together the node according to our clustering. For the nodes non existing in the clustering,
    # We put them in the cluster which contains the clother nodes to them

    k = 1
    # We go over all the remembered cluster
    for t,c in global_variable("history"):
        print(k)
        if k ==1:
            k+=1
            continue

        computed_cluster = []
        get_set_cluster(c, computed_cluster)
        X = [set() for _ in range(len(computed_cluster))]
        for node in test_data:
            if node in cluster.get_nodes(): #If the node is in the cluster, we already know the cluster
                for i in range(len(computed_cluster)):
                    if node in computed_cluster[i]:
                        X[i].add(node)
                        break
            else: #Otherwise, we put it in the cluster which have the closest node
                node_cloth = min(cluster.get_nodes(), key = lambda t : dist(node, t))
                for i in range(len(computed_cluster)):
                    if node_cloth in computed_cluster[i]:
                        X[i].add(node)
                        break
    

        a = normalized_mutual_info(set(test_data), X, Y)
        b = adjusted_random_index(set(test_data), X, Y)
        c = t - global_variable("time_start")+0.0001

        try:
            DataPoint.objects.create(
                benchmark = bm,
                iteration_no = k,
                ami = a,
                f_score = b,
                t_pre = 0, #Random values because I can't remove it
                t_cluster = c,
                t_write = 0.5 #Same as t_pre
            )
            
        except:
            pass
        k+=1



def get_set_cluster(cluster, res, lab_set = None):

    """
    This function returns a list of set of nodes, which is the clustering from the variable "cluster"
    
    Parameters
    ----------
    cluster : Cluster variable which gives the clustering
    res : The resultat where we append the clusters
    lab_set : Set of string
    """

    if lab_set == None: #That's is when we are at the root of the cluster
        # We will put in this cluster all the nodes not yet present in the subclusters
        s = set(cluster.get_nodes())
        sons = cluster.get_son()
        for i in range(len(cluster._cutting_values)):
            #We recursively get back the clusters
            get_set_cluster(sons[i], res, cluster._cutting_values[i])
            try:
                s = s - res[-1]
            except:
                pass
        if s != set():
            res.append(s)
    else: # We are here in a "normal" cluster, not at the root
        # We get back all the nodes with the right set of labels
        # (as a node can be in several clusters, we choose the one with the better set of label)
        # which are not in the subclusters
        s = set(filter( lambda node : node.get_labels() == lab_set ,cluster.get_nodes()))
        for c in cluster.get_son():
            get_set_cluster(c, res, lab_set)
            s = s - set(c.get_nodes())
        if s != set():
            res.append(s)


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
Inf
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
        if len(U[i]) != 0:
            HU += (len(U[i])/N)*math.log(len(U[i])/N)
    HU = -HU

    # compute the entropy of V partitioning
    HV = 0
    for i in range(len(V)):
        if len(V[i]) != 0:
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
    if len (U) == 1 or len(V) == 1:
        return 0
    
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

            for ind in range(ind_start, min(a_i,b_j)):
                # approximations with indexes can disturb the final value
                if (a_i-ind) <= 0:
                    fact_ai = 1
                else:
                    fact_ai = math.factorial(a_i-ind)
                if (b_j-ind) <= 0:
                    fact_bj = 1
                else:
                    fact_bj = math.factorial(b_j-ind)
                EMI += Decimal(math.factorial(N-a_i))/Decimal(math.factorial(N))*Decimal(math.factorial(N-b_j))/Decimal(math.factorial(N-a_i-b_j+ind))*Decimal((ind/N)*math.log(N*ind/(a_i*b_j)))*Decimal(math.factorial(a_i)*math.factorial(b_j))/Decimal(math.factorial(ind)*fact_ai*fact_bj)
             
    EMI = float(EMI)
    return ((MI-EMI)/(max(HU,HV)-EMI))



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
