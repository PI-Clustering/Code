""" Step 2 : Clustering step """

##### Imports
from sklearn.mixture import BayesianGaussianMixture
from termcolor import colored
import warnings
import random
import math
import hdbscan

def to_format(similarities_dict, amount_dict, list_of_distinct_nodes):
    """ Format data to a correct input for the Gaussian Model
    
    Parameters
    ----------
    similarities_dict : Python dict
        A dictionary with node strings as keys and a float representing their similarity measure as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': float, ...}
    amount_dict : Python dict
        A dictionary with node strings as keys and the number of occurrences of the node as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': int, ...}
    list_of_distinct_nodes :Python list
        A list of node strings
        Its format is : ['Label1 Label2 prop1', 'Label1 Label3 prop2', 'prop4 prop5', ...]

    Returns
    -------
    data : Python list of lists
        A list with each element representing the similarity measure of a node
        Its format is : [[float1],[float2],[float1],...]
    """
    data = []

    for node in list_of_distinct_nodes: # iterate through each different node
        amount = amount_dict[node] # the occurrences of the current node

        for i in range(amount):
            data.append([similarities_dict[node]]) # data must be a list of lists

    return data

def count_labs_props(amount_dict, list_of_distinct_nodes, distinct_labels):
    """ Computes the number of occurrences of each label and property in the dataset
    
    Parameters
    ----------
    amount_dict : Python dict
        A dictionary with node strings as keys and the number of occurrences of the node as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': int, ...}
    list_of_distinct_nodes : Python list
        A list of node strings
        Its format is : ['Label1 Label2 prop1', 'Label1 Label3 prop2', 'prop4 prop5', ...]
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]

    Returns
    -------
    labs : Python list
        A list representing all the labels found in this dataset
        Its format is : ["Label1","Label2","Label3",...]
    values_labs : Python list
        A list representing the number of occurrences of the labels of labs
        Its format is : [int1,int2,int3,int4,...]
    props : Python list
        A list representing all the properties found in this dataset
        Its format is : ["prop1","prop2","prop3",...]
    values_props : Python list
        A list representing the number of occurrences of the properties of props
        Its format is : [int1,int2,int3,int4,...]
    """
    labs = []
    values_labs = []
    props = []
    values_props = []

    # iterate through each different node
    for node in list_of_distinct_nodes:

            
        # We iterate over each label of the node
        for word in node[0]:

            # test if the label was already found
            if word not in labs: 
                labs.append(word)

                # increment considering the repeated nodes
                values_labs.append(1*amount_dict[node])
            else:
                # increment considering the repeated nodes
                values_labs[labs.index(word)]+=(1*amount_dict[node])
         
        for word in node[1]:
            # test if the property was already found
            if word not in props:
                props.append(word)

                # increment considering the repeated nodes
                values_props.append(1*amount_dict[node])
            else:
                # increment considering the repeated nodes
                values_props[props.index(word)]+=(1*amount_dict[node])

    return labs,values_labs,props,values_props

def max_labs_props(amount_dict, list_of_distinct_nodes, n, distinct_labels):
    """ Finds the most frequent label and the n most frequent properties in this dataset

    Parameters
    ----------
    amount_dict : Python dict
        A dictionary with node strings as keys and the number of occurrences of the node as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': int, ...}
    list_of_distinct_nodes : Python list
        A list of node strings
        Its format is : ['Label1 Label2 prop1', 'Label1 Label3 prop2', 'prop4 prop5', ...]
    n : Int
        An int representing the number of most frequent properties to search for
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]

    Returns
    -------
    s : String
        A string representing formed with the most frequent label and the n most frequent properties
        Its format is : "Label1 prop1 prop2 ... propn"

    """

    # get the number of occurrences of each label and property in the dataset
    labs,values_labs,props,values_props = count_labs_props(amount_dict,list_of_distinct_nodes, distinct_labels)

    # get the most frequent label if there are labels
    try:
        freq_lab = labs[values_labs.index(max(values_labs))]
    except:
        freq_lab = ""
    freq_prop = []

    # get the n most frequent properties if they exist
    for i in range(n):
        try:
            # get the argmax of the most frequent property
            ind = values_props.index(max(values_props))

            # add the corresponding property
            freq_prop.append(props[ind])

            # remove the most frequent property
            props.remove(props[ind])
            values_props.remove(values_props[ind])
        except:
            pass
    
    return (tuple(freq_lab),  tuple(freq_prop))

def compute_similarities(list_of_distinct_nodes, ref_node):
    """ Computes the similarity measure value with a reference node for each node in the dataset

    Parameters
    ----------
    list_of_distinct_nodes : Python list
        A list of node strings
        Its format is : ['Label1 Label2 prop1', 'Label1 Label3 prop2', 'prop4 prop5', ...]
    ref_node : String
        A string representing formed with the most frequent label and the n most frequent properties
        Its format is : "Label1 prop1 prop2 ... propn"

    Returns
    -------
    similarities_dict : Python dict
        A dictionary with node strings as keys and a float representing their similarity measure as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': float, ...}

    """
    similarities_dict = {}

    # iterate through each different node
    for node in list_of_distinct_nodes:

        # get the similarity measure value between a reference node and the current node
        distance = dist(ref_node,node)

        # add the value to the dictionary
        similarities_dict[node] = distance

    return similarities_dict

def iter_gmm(amount_dict, list_of_distinct_nodes, distinct_labels, all_sets_labels):
    """ Makes a cluster computation, call rec_clustering to find subclusters

    Parameters
    ----------
    amount_dict : Python dict
        A dictionary with node strings as keys and the number of occurrences of the node as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': int, ...}
    list_of_distinct_nodes : Python list
        A list of node strings
        Its format is : ['Label1 Label2 prop1', 'Label1 Label3 prop2', 'prop4 prop5', ...]
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]
    all_sets_labels : Python list of list
        A list of all labels sets
        Its format is : [['Label 1','Label2'],['Label1'],['Label3'],...]

    Returns
    -------
    all_clusters : Python list of sets
        Each set of this list represents a different cluster,
        they may contain one element or more,
        an element is a string node that was clustered in this cluster
        Its format is : [{'Label1 prop1', 'Label1', 'Label1 prop1 prop2'}, {'Label3', 'Label3 prop1 prop4'}, ...]
    """

    # ignore all convergence warnings
    warnings.filterwarnings("ignore")

    all_clusters = []
    hierarchy_tree = []
    
    # iterate through each different sets of labels
    for lab_set in all_sets_labels:
        correct_nodes = []

        # iterate through each different node
        for node in list_of_distinct_nodes:

            if set(lab_set) == set(node[0]):
                # it has not every labels and just this labels we are in the right place
                correct_nodes.append(node)

        # search for all subclusters
        all_clusters, hierarchy = rec_clustering(amount_dict, correct_nodes, distinct_labels, all_clusters, [set(lab_set),None,None])
        hierarchy_tree.append(hierarchy)
    return all_clusters, hierarchy_tree

def rec_clustering(amount_dict, correct_nodes, distinct_labels, all_clusters, hierarchy):
    """

    Parameters
    ----------
    amount_dict : Python dict
        A dictionary with node strings as keys and the number of occurrences of the node as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': int, ...}
    correct_nodes : Python list
        A list of node strings representing all nodes from a cluster that we try to cluster more
        Its format is : ['Label1 prop1 prop2 prop3', 'Label1 prop1 prop2', 'Label1 prop1 prop2 prop4', ...]
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]
    all_clusters : Python list of sets
        Each set of this list represents a different cluster,
        they may contain one element or more,
        an element is a string node that was clustered in this cluster
        Its format is : [{'Label1 prop1', 'Label1', 'Label1 prop1 prop2'}, {'Label3', 'Label3 prop1 prop4'}, ...]

    Returns
    -------
    all_clusters : The same all_clusters as in parameters but with new clusters added
    """

    # get a reference node
    ref_node = max_labs_props(amount_dict, correct_nodes, 1, distinct_labels)

    # compute all similarity measures according to the reference node
    similarities_dict = compute_similarities(correct_nodes, ref_node)

    # create a list of lists with the number of occurrences of each node respected and that can be used by a Gaussian Mixture Model
    computed_measures = to_format(similarities_dict, amount_dict, correct_nodes)

    # BayesianGaussianMixture cannot cluter one node
    if len(computed_measures)>1:

        # Train the model with some parameters to speed the process
        bgmm = BayesianGaussianMixture(n_components=2, tol=1, max_iter=10).fit(computed_measures)

        # Make the clustering
        predictions = bgmm.predict(computed_measures)

        # variable to keep separated nodes of the two clusters
        clusters = [[],[]]

        # variable to keep track on the index of the node in the list 'predictions'
        j = 0

        # iterate through each different nodes in this dataset
        for node in correct_nodes:

            # get the number of occurrences of each of the current node
            amount = amount_dict[node]

            # add "amount" times the node to its predicted cluster
            for i in range(amount):
                clusters[predictions[j]].append(node)
                j+=1

        ### First cluster
        set_cluster_1 = set(clusters[0])

        # if the cluster is new and if not empty (ie. there are two found clusters)
        if set_cluster_1 not in all_clusters and set_cluster_1 != set():
            # add the cluster to our main variable
            all_clusters.append(set_cluster_1)

            # make a new dataset with all nodes found in the subcluster
            correct_nodes = list(set_cluster_1)

            # search for more subclusters in this subcluster
            all_clusters,hierarchy1 = rec_clustering(amount_dict, correct_nodes, distinct_labels, all_clusters, [set_cluster_1,None,None])
            hierarchy[1] = hierarchy1

        ### Second cluster
        set_cluster_2 = set(clusters[1])

        # if the cluster is new and if not empty (ie. there are two found clusters)
        if set_cluster_2 not in all_clusters and set_cluster_2 != set():
            # add the cluster to our main variable
            all_clusters.append(set_cluster_2)

            # make a new dataset with all nodes found in the subcluster
            correct_nodes = list(set_cluster_2)

            # search for more subclusters in this subcluster
            all_clusters,hierarchy2 = rec_clustering(amount_dict, correct_nodes, distinct_labels, all_clusters, [set_cluster_2,None,None])
            hierarchy[2] = hierarchy2

    return all_clusters,hierarchy

def dist(a,b):
    """ Compute a similiarity measure value between two node"""
    
    s = len(set(a[0]).intersection(set(b[0]))) + len(set(a[1]).intersection(set(b[1])))
    
    return 2*s / (len(a[0]) + len(a[1]) + len(b[0]) + len(b[1]))
    
def dice_coefficient(a,b):
    """ Compute the similarity measure value between two strings

    Parameters
    ----------
    a,b : Strings

    Returns
    -------
    score : Float
        Float representing the similarity between a and b (the bigger it is the more similar a and b are)

    """

    # if a and b are equal, return 1.0
    if a == b: return 1.0
    
    # if a and b are single caracters then they cannot possibly match
    if len(a) == 1 or len(b) == 1: return 0.0
    
    # two lists representing all bigrams found in a and b
    a_bigram_list = [a[i:i+2] for i in range(len(a)-1)]
    b_bigram_list = [b[i:i+2] for i in range(len(b)-1)]
    
    # sort lists alphabetically to help the iteration step
    a_bigram_list.sort()
    b_bigram_list.sort()
    
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)

    matches = i = j = 0
    while (i < lena and j < lenb):

        # if they are equal then increment matches
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 1
            i += 1
            j += 1

        # alphabetical sort helps us earn time in theses cases
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1
    
    # use a 'dice_coefficient' formula
    score = float(2*matches)/float(lena + lenb)
    
    return score
