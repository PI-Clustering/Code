import numpy as np
import random

import csv
import os 

from sklearn.semi_supervised import LabelSpreading

from webApp.scripts.src.debug import print_dict_node

from .eval_quality import eval_quality
from .clustering_algo import *
from .node import *
from copy import deepcopy
from ...models import Benchmark, DataPoint
from ..settings import global_variable
from .storing import storing

from .debug import *

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
            labs = labs.union(node.get_labels())
            props = props.union(node.get_properties())
        
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
        algo_type=data['method'],
        data_set= name_data,
        n_iterations=0,
        size=sum(global_variable("cluster").get_nodes().values()) + sum(add_data.values()),
        t_pre = 0,
        t_cluster = 0,
        t_write = 0
    )

    global_variable("bm", bm)

    global_variable("history", [])
    t = time()
    global_variable("time_start", t)
    if data['method'] == "I-GMM-D":
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

    elif data['method'] == 'GMM-D':
        add_node_exact(add_data)

    step2 = time() - t

    t = time()
    storing_incr(global_variable("cluster"), global_variable("edges"))
    if data['evaluate']:
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

    bm = global_variable("bm")
    Benchmark.objects.filter(pk=bm.pk).update(n_iterations = bm.n_iterations + 1)
    bm.refresh_from_db()

    cluster = global_variable("cluster")
    cluster.add_node(node)
    cluster._modification += 1

    labs = node.get_labels()

    fils = cluster.get_son()
    first_cluster = cluster._cutting_values
    
    print(node)
    print(first_cluster)

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
    
    bm = global_variable("bm")
    Benchmark.objects.filter(pk=bm.pk).update(n_iterations = bm.n_iterations + 1)
    bm.refresh_from_db()

    t = time()
    b = deepcopy(global_variable("cluster"))
    global_variable("history").append((t, b))

    cluster.add_node(node)

    d = dist(node, cluster._ref_node)

    cuts = cluster._cutting_values
    list_son = cluster.get_son()

    print(cuts)
    print(list_son)

    if len(list_son)>0:

        # We set this value in order to be sure to find a place for the node
        cuts[0] = 0
        
        for i in range(len(cuts)-1, -1, -1):
            if d >= cuts[i]:
                add_node_rec(list_son[i], node)
                break


def add_node_exact(dict_node, nb_cluster = 2):
    """
    The point of this function is to insert a node, exactly as if we were recomputing everything,
    computing only the part we didn't already compute.
    """

    bm = global_variable("bm")
    Benchmark.objects.filter(pk=bm.pk).update(n_iterations = bm.n_iterations + 1)
    bm.refresh_from_db()

    cluster = global_variable("cluster")

    pre_computed = dict()
    get_all_cluster(cluster, pre_computed)

    for node in dict_node:
        cluster.add_node(node, dict_node[node])

    graph = Graph()
    dico = cluster.get_nodes()
    for node in dico:
        graph.add_node(node, dico[node])


    cluster = Cluster("Main")
    global_variable("cluster", cluster)
    cluster._nodes = graph._node_occurs
    
    for lab_set in graph.get_sets_labels():
        new_cluster = Cluster()
        correct_nodes = dict()
        # iterate through each different node
        for node in graph.distinct_node():

            if lab_set.issubset(node.get_labels()):
                correct_nodes[node] = graph.occurs(node)

        # search for all subclusters
        new_cluster._nodes = correct_nodes
        if len(correct_nodes) != 0:
            cluster._cutting_values.append(lab_set)
            cluster.add_son(new_cluster)
            add_node_exact_rec(new_cluster, pre_computed)
            new_cluster._name = ":".join(list(lab_set))


    return cluster
 

def add_node_exact_rec(cluster, pre_computed, nb_cluster = 2):

    bm = global_variable("bm")
    Benchmark.objects.filter(pk=bm.pk).update(n_iterations = bm.n_iterations + 1)
    bm.refresh_from_db()

    t = time()
    b = deepcopy(global_variable("cluster"))
    global_variable("history").append((t, b))

    correct_nodes = cluster.get_nodes()
    ref_node = max_labs_props(correct_nodes)

    cluster._name = str(ref_node)
    cluster._ref_node = ref_node
    similarities_dict = compute_similarities(correct_nodes, ref_node)

    computed_measures, ecrasage = to_format(similarities_dict, correct_nodes)

    print(1)

    if len(correct_nodes) >= nb_cluster and nb_cluster > 0:

        print(len(computed_measures))
        bgmm = BayesianGaussianMixture(n_components=nb_cluster, tol=1, max_iter=10).fit(computed_measures)
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
                print(7)
            elif len(id) > 0:
                cluster.add_son(new_clusters[i])
                print(8)
                add_node_exact_rec(new_clusters[i], pre_computed)
            else:
                print(9)
                

                


def get_all_cluster(cluster,res):
    nodes = frozenset(cluster.get_nodes().items())
    res[nodes] = deepcopy(cluster)
    for son in cluster.get_son():
        get_all_cluster(son, res)



def add_node_hybrid(node):
    """Insert a node in our cluster not recalculating GMM as long as the reference node shoudl not change"""

    bm = global_variable("bm")
    Benchmark.objects.filter(pk=bm.pk).update(n_iterations = bm.n_iterations + 1)
    bm.refresh_from_db()

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

    bm = global_variable("bm")
    Benchmark.objects.filter(pk=bm.pk).update(n_iterations = bm.n_iterations + 1)
    bm.refresh_from_db()

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
    else:
        rec_clustering(cluster)





# Now we are going to do the storing for the incremental graphs

def storing_incr(cluster, edges):
    global old_node, old_edge, dict_ind
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "../graph/node.csv")) as f:
        reader = csv.reader(f, delimiter=',')
    
        old_node = np.array(list(reader))
    

    with open(os.path.join(dirname, "../graph/edge.csv")) as f:
        reader = csv.reader(f, delimiter=',')
    
        old_edge = np.array(list(reader))

    run_clusters = []
    i = 1

    main_node = dict()
    cluster_list = [cluster]
    esubtype = []

    dict_ind = dict() #This dictionnary shall store the link between the previous and the current indexes

    with open(os.path.join(dirname, "../graph/node.csv"), "w")as f:
        writer = csv.writer(f)
        header = ["id", "labels", "properties", "depth", "number", "new", "old_number"]
        writer.writerow(header)

        # iterate through each basic type clusters
        for basic_type in cluster.get_son():
            parent_id = i
            dict_ind[i] = i
            data_line = [str(parent_id)]  # line id
            labels = basic_type.get_name()

            data_line.append(labels)  # labels
            data_line.append("")  # no properties for base types
            data_line.append("1")  # the name of the infered type
            data_line.append(str(basic_type.get_number_node())) # nombre de noeud
            
            #We then look if we already have seen this line
            if data_line[1:5] in old_node[:, 1:5].tolist():
                data_line.append("0") # The cluster is not to be new
                data_line.append("Nan")
                ind = old_node[:, 1:5].tolist().index(data_line[1:5])
                dict_ind[i] = old_node[ind][0]
            elif data_line[1:4] in old_node[:, 1:4].tolist(): #Then the cluster exists but with different number of nodes
                ind = old_node[:, 1:4].tolist().index( data_line[1:4] )
                data_line.append("1")
                data_line.append(old_node[ind][4])
                dict_ind[i] = old_node[ind][0]
            else:
                data_line.append("2")
                data_line.append("Nan")
                

            writer.writerow(data_line)
            cluster_list.append(basic_type)

            main_node[labels] = i

            h = i

            i += 1
            k = 2

            # search for subtypes
            for sous_cluster in basic_type.get_son():
                if sous_cluster is not None:  # inutile

                    i, _ = rec_storing_incr(sous_cluster, writer,
                                       i, parent_id, run_clusters, k, cluster_list, esubtype, h)

    with open(os.path.join(dirname, "../graph/edge.csv"), "w") as f:

        writer = csv.writer(f)
        header = ["id1", "id2", "types", "new"]
        writer.writerow(header)

        if edges != None:

            N = len(cluster_list)
            tab = [[0 for _ in range(N)] for _ in range(N)]

            for edge in edges:
                ln = set(edge["labels(n)"])
                pn = set(edge["keys(n)"])
                n = Node(ln,pn)
                cn = 0
                for i in range(1,N):
                    if cluster_list[i].get_son() == [] and n in cluster_list[i]._nodes:
                        cn = i

                lm = set(edge["labels(m)"])
                pm = set(edge["keys(m)"])
                m = Node(lm,pm)
                cm = 0
                for i in range(1,N):
                    if cluster_list[i].get_son() == [] and m in cluster_list[i]._nodes:
                        cm = i

                t = edge["type(r)"]
                tab[cn][cm] = t



            for i in range(1,N):
                for j in range(1,N):
                    if tab[i][j] != 0 and i != j:
                        if [str(dict_ind[i]), str(dict_ind[j]), tab[i][j]] in old_edge[:, :3].tolist():
                            writer.writerow([str(i),str(j),tab[i][j], "0"])
                        else:
                            writer.writerow([str(i),str(j),tab[i][j], "1"])

        for p in esubtype:
            if [str(dict_ind[p[0]]), str(dict_ind[p[1]]), "SUBTYPE_OF"] in old_edge[:, :3].tolist():
                writer.writerow([str(p[0]), str(p[1]), "SUBTYPE_OF", "0"])
            else:
                writer.writerow([str(p[0]), str(p[1]), "SUBTYPE_OF", "1"])


    return "node.csv,edge.csv"


def rec_storing_incr(cluster, writer, i, parent_id, run_clusters, k, cluster_list, subtype, h):
    """ Write clusters into a file

    Parameters
    ----------
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]
    labs_sets : Python list of list
        A list of all labels sets
        Its format is : [['Label 1','Label2'],['Label1'],['Label3'],...]
    all_clusters : Python list of sets
        Each set of this list represents a different cluster,
        they may contain one element or more,
        an element is a string node that was clustered in this cluster
        Its format is : [{'Label1 prop1', 'Label1', 'Label1 prop1 prop2'}, {'Label3', 'Label3 prop1 prop4'}, ...]

    Returns
    -------
    file : String
        Name of the file clusters were written into.

    """
    global old_node, old_edge

    dict_ind[i]=i

    all_labels = set()
    all_properties = set()
    always_labels = set()
    always_properties = set()

    j = True

    # iterate through each node that forms the cluster
    for node in cluster.get_nodes():
        cur_labels = node.get_labels()
        cur_properties = node.get_proprety()

        all_labels = all_labels.union(cur_labels)
        all_properties = all_properties.union(cur_properties)

        if j:
            always_labels = cur_labels.union(set())
            always_properties = cur_properties.union(set())
        j = False

        always_labels = always_labels.intersection(cur_labels)
        always_properties = always_properties.intersection(cur_properties)

    # identify optionnal labels and properties with the always_labels et and always_properties
    optional_labels = all_labels-always_labels
    optional_properties = all_properties-always_properties

    # add a question mark for optionnal labels and properties
    if optional_labels != set():
        labels = ":".join(sorted(list(always_labels)))+":?" + \
            ":?".join(sorted(list(optional_labels)))
    else:
        labels = ":".join(sorted(list(always_labels)))

    if optional_properties != set():
        properties = ":".join(sorted(list(always_properties))) + \
            ":?"+":?".join(sorted(list(optional_properties)))
    else:
        properties = ":".join(sorted(list(always_properties)))

    # if the formed cluster does not exist
    if labels+properties not in run_clusters:

        subtype.append((i,h))
        # line id
        data_line = [str(i)]
        data_line.append(labels)
        data_line.append(properties)
        data_line.append(str(k))
        data_line.append(str(cluster.get_number_node())) # nombre de noeuds
        
        if data_line[1:5] in old_node[:, 1:5].tolist():
            data_line.append("0") # The cluster is not to be new
            data_line.append("Nan")
            ind = old_node[:, 1:5].tolist().index(data_line[1:5])
            dict_ind[i] = old_node[ind][0]
        elif data_line[1:4] in old_node[:, 1:4].tolist(): #Then the cluster exists but with different number of nodes
            ind = old_node[:, 1:4].tolist().index( data_line[1:4] )
            data_line.append("1")
            data_line.append(old_node[ind][4])
            dict_ind[i] = old_node[ind][0]
        else:
            data_line.append("2")
            data_line.append("Nan")      
        

        writer.writerow(data_line)
        cluster_list.append(cluster)
        

        run_clusters.append(labels+properties)

        h = i
        k += 1

        i += 1

        # search for more subtypes
        for sous_cluster in cluster.get_son():
            if sous_cluster is not None:  # inutile
                i, _ = rec_storing_incr(sous_cluster, writer, i,
                                   parent_id, run_clusters, k, cluster_list, subtype, h)

    return i, k

