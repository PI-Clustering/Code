""" Step 2 : Clustering step """

# Imports
from sklearn.mixture import BayesianGaussianMixture
from termcolor import colored
import warnings
import random
import math
import hdbscan
from time import sleep

from .node import Node, Graph, Cluster


def clustering(graph):
    cluster = Cluster("Main")
    # warnings.filterwarnings("ignore")

    # iterate through each different sets of labels
    for lab_set in graph.get_sets_labels():
        new_cluster = Cluster()
        correct_nodes = dict()
        cluster._cutting_values.append(lab_set)
        # iterate through each different node
        for node in graph.distinct_node():

            if lab_set.issubset(node.get_labels()):
                correct_nodes[node] = graph.occurs(node)

        # search for all subclusters
        new_cluster._nodes = correct_nodes
        if len(correct_nodes) != 0:
            rec_clustering(new_cluster)
            cluster.add_son(new_cluster)
            new_cluster._name = ":".join(list(lab_set))

    return cluster


def rec_clustering(cluster, nb_cluster=2):
    correct_nodes = cluster.get_nodes()
    # get a reference node
    ref_node = max_labs_props(correct_nodes)
    cluster._name = str(ref_node)
    cluster._ref_node = ref_node
    # compute all similarity measures according to the reference node
    similarities_dict = compute_similarities(correct_nodes, ref_node)

    # create a list of lists with the number of occurrences of each node respected and that can be used by a Gaussian Mixture Model
    computed_measures, ecrasage = to_format(similarities_dict, correct_nodes)

    # BayesianGaussianMixture cannot cluter one node
    if len(correct_nodes) >= nb_cluster:

        # Train the model with some parameters to speed the process
        bgmm = BayesianGaussianMixture(
            n_components=nb_cluster, tol=1, max_iter=10).fit(computed_measures)
        predictions = bgmm.predict(computed_measures)

        # variable to keep track on the index of the node in the list 'predictions'
        j = 0
        new_clusters = [Cluster("Oh") for _ in range(nb_cluster)]
        cluster._cutting_values = cutting_value(computed_measures, predictions)
        # iterate through each different nodes in this dataset
        for node in correct_nodes:
            amount = correct_nodes[node] // (10**ecrasage)
            for i in range(amount):
                if node in new_clusters[predictions[j]]._nodes:
                    new_clusters[predictions[j]]._nodes[node] += 10**ecrasage
                else:
                    print("&", end="")
                    new_clusters[predictions[j]]._nodes[node] = 10**ecrasage
                j += 1

        count = 0
        for c in new_clusters:
            count += len(c.get_nodes()) != 0
        if (count < 2):
            return

        # For each cluster cluster
        for i in range(nb_cluster):
            set_cluster = set(new_clusters[i]._nodes)

        # if the cluster is new and if not empty (ie. there are two found clusters)
            if set_cluster != set():
                # search for more subclusters in this subcluster
                rec_clustering(new_clusters[i], nb_cluster)
                cluster.add_son(new_clusters[i])


def max_labs_props(correct_node, n=1):
    # create a fictive node, which should be in the middle of the data set

    # get the most frequent label
    freq_lab = dict()
    for node in correct_node:
        for l in node.get_labels():
            if (l not in freq_lab):
                freq_lab[l] = correct_node[node]
            else:
                freq_lab[l] += correct_node[node]
    dominant_label = set(max(freq_lab, key=freq_lab.get))

    # get the n most frequent propretries
    freq_prop = dict()
    for node in correct_node:
        for l in node.get_proprety():
            if (l not in freq_prop):
                freq_prop[l] = correct_node[node]
            else:
                freq_prop[l] += correct_node[node]

    dominant_prop = set()
    for i in range(n):
        try:
            # get the argmax of the most frequent property
            temp_prop = max(freq_prop, key=freq_prop.get)
            dominant_prop.add(temp_prop)
            freq_prop.pop(temp_prop)
        except:
            pass

    return Node(dominant_label, dominant_prop)


def compute_similarities(nodes, ref_node):
    similarities_dict = dict()
    # iterate through each different node
    for node in nodes:
        # get the similarity measure value between a reference node and the current node
        distance = dist(ref_node, node)
        # add the value to the dictionary
        similarities_dict[node] = distance

    return similarities_dict


def to_format(similarities_dict, nodes):
    data = []

    pre_ecrasage = math.inf  # Parce que c'est beaucoup
    for node in nodes:
        pre_ecrasage = min(pre_ecrasage, math.floor(math.log(nodes[node], 10)))

    for node in nodes:  # iterate through each different node
        # the occurrences of the current node
        amount = nodes[node] // (10**(max(0, pre_ecrasage - 2)))

        for i in range(amount):
            # data must be a list of lists
            data.append([similarities_dict[node]])

    return data, max(pre_ecrasage-2, 0)


def cutting_value(distances, prediction):
    """ Calculate what are the floating values that are the separation between the different clusters."""
    n = max(prediction)

    res = [0]*(n+1)
    for i in range(len(distances)):
        if distances[i][0] > res[prediction[i]]:
            res[prediction[i]] = distances[i][0]

    return res


def dist(a, b):
    """ Compute a similiarity measure value between two node"""

    s = len(a.get_labels().intersection(b.get_labels())) + \
        len(a.get_proprety().intersection(b.get_proprety()))

    return 2*s / (len(a.get_labels()) + len(a.get_proprety()) + len(b.get_labels()) + len(b.get_proprety()))


def dice_coefficient(a, b):
    # if a and b are equal, return 1.0
    if a == b:
        return 1.0

    # if a and b are single caracters then they cannot possibly match
    if len(a) == 1 or len(b) == 1:
        return 0.0

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
