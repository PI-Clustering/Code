from rand_index import *
from mutual_information import *
import hdbscan
from GMM_clustering import *
from neo4j import GraphDatabase
import csv

def hdbscan_indexes(validate,distinct_labels,len_X):

    list_of_distinct_nodes = list(set(validate))

    amount_dict = {}

    for node in list_of_distinct_nodes:
        amount_dict[node] = validate.count(node)

    correct_nodes = list_of_distinct_nodes

    ref_node = max_labs_props(amount_dict, correct_nodes, 1, distinct_labels)

    similarities_dict = compute_similarities(correct_nodes, ref_node)

    X = to_format(similarities_dict, amount_dict, correct_nodes)

    all_nodes = []
    for node in correct_nodes:
        amount = amount_dict[node]
        amount_dict[node] = 1
        for i in range(amount):
            all_nodes.append(node)

    print("hdbscan model:")
    predictions = hdbscan.HDBSCAN().fit_predict(X)
    print("done.")

    #print(set(predictions))

    S = set(correct_nodes)
    X = [set() for _ in range(len_X)]
    Y = [set() for _ in range(len(set(predictions)))]
    Z = {}

    for node in correct_nodes:
        node_split = node.split(" ")
        labels = list(set(distinct_labels) & set(node_split))
        properties = list(set(node_split) - set(distinct_labels))

        with open('data.csv') as f:
            reader = csv.reader(f, delimiter=',')
            i=0
            for row in reader:
                if i==0:
                    i+=1
                else:
                    cluster_labels = row[1].split(":")
                    Z[int(row[0])-1] = len(cluster_labels)
                    cluster_labels = [x for x in cluster_labels if not x.startswith('?')]
                    cluster_props = row[2].split(":")
                    Z[int(row[0])-1] += len(cluster_props)
                    cluster_props = [x for x in cluster_props if not x.startswith('?')]

                    max_Z = 0
                    check = False

                    for l in range(len_X):
                        if node in X[l]:
                            max_X = Z[l]
                            if max_Z < max_X:
                                max_Z = max_X
                            check = True

                    # check if the node already exists in a cluster
                    if check:
                        # if it has the same labels, has common properties and is the more precise cluster then chose to add the node to this cluster
                        if set(cluster_labels) == set(labels) and set(cluster_props).issubset(set(properties)) and max_Z == Z[int(row[0])-1]:
                            for l in range(len_X):
                                X[l].discard(node)
                            X[int(row[0])-1].add(node)
                    else:
                        if set(cluster_labels) == set(labels) and set(cluster_props).issubset(set(properties)):
                            for l in range(len_X):
                                X[l].discard(node)
                            X[int(row[0])-1].add(node)


        Y[predictions[all_nodes.index(node)]].add(node)

    X = list(filter(lambda a: a != set(), X))

    ARI = adjusted_random_index(S,X,Y)
    EMI = normalized_mutual_info(S,X,Y)

    return ARI,EMI