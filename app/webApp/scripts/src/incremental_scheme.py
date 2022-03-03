import numpy as np
import random

from sklearn.semi_supervised import LabelSpreading

from .eval_quality import eval_quality
from .clustering_algo import *
from .node import *
from copy import deepcopy
from ...models import Benchmark, DataPoint
from ..settings import global_variable
from .storing import storing

def run_add_node(data):
    
    t = time()

    nb_nodes = data['how_many']

    if data["use_real_data"]:
        unused = global_variable("unused")
        N = sum(unused.values())
        if N >= nb_nodes:
            add_data = dict()
            p = nb_nodes/N
            for node in unused:
                nb = np.random.binomial(unused[node], p)
                if nb != 0:
                    add_data[node] = nb
                    unused[node] -= nb
            global_variable("unused", unused)

        else:
            add_data = unused
            global_variable("unused", dict())
            old_data = global_variable("cluster").get_nodes()
            p = min((N - nb_nodes)/sum(old_data.values()), 1)
            for node in old_data:
                nb = np.random.binomial(old_data[node], p)
                if nb != 0:
                    if node in add_data:
                        add_data[node] += nb
                    else:
                        add_data[node] = nb
    

    else:

        old_data = global_variable("cluster")
        nodes = set(old_data.get_nodes())
        labs = set()
        props = set()
        for node in nodes:
            labs.union(node.get_labels())
            props.union(node.get_properties())
        
        add_data = dict()
        for _ in range(nb_nodes):
            k = np.random.binomial(len(labs), 0.5)
            lab = set(random.sample(labs, k))
            k = np.random.binomial(len(props), 0.5)
            prop = set(random.sample(props, k))
            node = Node(lab, prop)
            if node in add_data:
                add_data[node] += 1
            else:
                add_data[node] = 1

    step1 = t - time()

    bm = global_variable("bm")

    name_data = bm.data_set

    bm = Benchmark.objects.create(
        algo_type='Adding node with ' + data['method'] + ' method',
        data_set= name_data,
        n_iterations=0,
        size=sum(global_variable("cluster").get_nodes().values()) + sum(add_data.values())
    )

    global_variable("bm", bm)

    global_variable("history", [])
    t = time()
    global_variable("time_start", t)
    if data['method'] == "incremental":
        list_add_node = []
        for node in add_data:
            list_add_node += [node]*add_data[node]
        list_add_node = random.sample(list_add_node, len(list_add_node))
        for node in list_add_node:
            add_node(node)

    elif data['method'] == "median":
        list_add_node = []
        for node in add_data:
            list_add_node += [node]*add_data[node]
        list_add_node = random.sample(list_add_node, len(list_add_node))
        for node in list_add_node:
            add_node_hybrid(node)

    elif data['method'] == 'exact':
        add_node_exact(add_data)

    step2 = time() - t

    t = time()
    storing(global_variable("cluster"), None, name_data)
    if data['evalutate']:
        eval_quality()
    step3 = time() - t

    Benchmark.objects.filter(pk=bm.pk).update(t_pre = step1, t_cluster = step2, t_write = step3)

    return {
        "t_pre": step1,
        "t_cluster": step2,
        "t_write": step3,
    }


def add_node(node):
    """ This function add a node to a cluster (it has to be the main one). """

    cluster = global_variable("cluster")
    cluster.add_node(node)
    cluster._modification += 1

    labs = node.get_labels()

    fils = cluster.get_son()
    first_cluster = cluster._cutting_values

    if cluster._modification / sum(cluster.get_nodes().values()) < 0.1:
        for i in range(len(first_cluster)):
            if first_cluster[i].issubset(labs):
                add_node_rec(fils[i], node)

    else:
        nodes = cluster.get_nodes()
        graph = Graph()
        for node in nodes.keys():
            graph.add_node(node, nodes[node])
        cluster = clustering(graph)

    return cluster


def add_node_rec(cluster, node):
    """This function goes recursivly to insert a node, and only take subclusters ( created with gmm, not by the lab_set )  """

    t = time()
    b = deepcopy(global_variable("cluster"))
    global_variable("history").append((t, b))

    cluster.add_node(node)

    d = dist(node, cluster._ref_node)

    cuts = cluster._cutting_values
    list_son = cluster.get_son()

    if cuts != []:

        # We set this value in order to be sure to find a place for the node
        cuts[0] = 0

        for i in range(len(cuts)-1, -1, -1):
            if d >= cuts[i]:
                add_node_rec(list_son[i], node)
                break

        raise Exception(
            "We shouldn't be in this situation, as the minimum distance, 0, is supposed to be reached")


def add_node_exact(dict_node):
    """
    The point of this function is to insert a node, exactly as if we were recomputing everything,
    computing only the part we didn't already compute.
    """
    cluster = global_variable("cluster")

    pre_computed = dict()
    get_all_cluster(cluster, pre_computed)

    for node in dict_node:
        cluster.add_node(node, dict_node[node])

    labs = node.get_labels()

    nodes_cluster = cluster.get_nodes()
    fils = cluster.get_son()
    first_cluster = cluster._cutting_values

    for i in range(len(fils)):
        node_to_add = dict()
        for node in dict_node:
            if first_cluster[i].issubset(node.get_labels()):
                node_to_add[node] = dict_node[node]
        add_node_exact_rec(fils[i], node_to_add)

    for node in dict_node:
        labs = node.get_labels()
        if labs not in cluster._cutting_values:  # That mean we have a new type of node with a new set of label
            new_cluster = Cluster()
            correct_nodes = dict()
            cluster._cutting_values.append(labs)
            correct_nodes[node] = 1
            for node_c in nodes_cluster:
                if labs.issubset(node_c.get_labels()):
                    correct_nodes[node_c] = nodes_cluster[node_c]
                    new_cluster._nodes = correct_nodes
            rec_clustering(new_cluster)
            cluster.add_son(new_cluster)
            new_cluster._name = ":".join(list(labs))

    return cluster


def add_node_exact_rec(cluster, pre_computed):

    t = time()
    b = deepcopy(global_variable("cluster"))
    global_variable("history").append((t, b))


    nb_cluster = len(cluster.get_son())

    correct_nodes = cluster.get_nodes()
    ref_node = max_labs_props(correct_nodes)

    cluster._name = str(ref_node)
    cluster._ref_node = ref_node
    similarities_dict = compute_similarities(correct_nodes, ref_node)

    computed_measures, ecrasage = to_format(similarities_dict, correct_nodes)

    if len(correct_nodes) >= nb_cluster and nb_cluster > 0:

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

        cluster._fils=[]

        # For each cluster cluster
        for i in range(nb_cluster):
            id = frozenset(new_clusters[i].get_nodes().items())
            if id in pre_computed:
                cluster.add_son(pre_computed[id])
            elif len(id) > 0:
                cluster.add_son(new_clusters[i])
                add_node_exact_rec(new_clusters[i], pre_computed)
                

                


def get_all_cluster(cluster,res):
    nodes = frozenset(cluster.get_nodes().items())
    res[nodes] = deepcopy(cluster)
    for son in cluster.get_son():
        get_all_cluster(son, res)

def add_node_hybrid(node):
    """Insert a node in our cluster not recalculating GMM as lon as the reference node shoudl not change"""
    cluster = global_variable("cluster")
    cluster.add_node(node)
    cluster.add_node(node)
    labs = node.get_labels()

    nodes_cluster = cluster.get_nodes()
    fils = cluster.get_son()
    first_cluster = cluster._cutting_values

    for i in range(len(first_cluster)):
        if first_cluster[i].issubset(labs):
            add_node_hybrid_rec(fils[i], node)


def add_node_hybrid_rec(cluster, node):

    t = time()
    b = deepcopy(global_variable("cluster"))
    global_variable("history").append((t, b))

    cluster.add_node(node)

    d = dist(node, cluster._ref_node)

    cuts = cluster._cutting_values
    list_son = cluster.get_son()

    correct_nodes = cluster.get_nodes()
    ref_node = max_labs_props(correct_nodes)

    if cuts != [] and ref_node == cluster._ref_node:

        # We set this value in order to be sure to find a place for the node
        cuts[0] = 0

        for i in range(len(cuts)-1, -1, -1):
            if d >= cuts[i]:
                add_node_rec(list_son[i], node)
                break

        raise Exception(
            "We shouldn't be in this situation, as the minimum distance, 0, is supposed to be reached")

    else:
        rec_clustering(cluster)