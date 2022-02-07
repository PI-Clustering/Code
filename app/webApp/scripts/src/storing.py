""" Write clusters into a file """

##### Imports
import csv
from threading import main_thread

from numpy.core.arrayprint import DatetimeFormat

from node import Cluster, Node

def storing(cluster,schema):

    data = []
    run_clusters = []
    i=1

    main_node = dict()

    with open("../graph/node.csv","w") as f:
        writer = csv.writer(f)
        header = ["id","labels","properties","profondeur"]
        writer.writerow(header)

        # iterate through each basic type clusters
        for basic_type in cluster.get_son():
            parent_id = i

            data_line = [str(parent_id)] # line id
            labels = basic_type.get_name()

            data_line.append(labels) # labels
            data_line.append("") # no properties for base types
            data_line.append("1") # the name of the infered type

            writer.writerow(data_line)
            main_node[labels] = i

            i+=1
            k = 2

            # search for subtypes
            for sous_cluster in basic_type.get_son():
                if sous_cluster is not None: ##inutile
                    i,_ = rec_storing(sous_cluster, writer, i, parent_id, run_clusters, k)

    with open("../graph/edge.csv","w") as f:
        writer = csv.writer(f)
        header = ["id1", "id2", "types"]
        writer.writerow(header)

        node = schema["nodes"]
        rel = schema["relationships"]
        
        

    return "node.csv et edge.csv"


def rec_storing(cluster, writer, i, parent_id, run_clusters, k):
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
        labels = ":".join(sorted(list(always_labels)))+":?"+":?".join(sorted(list(optional_labels)))
    else:
        labels = ":".join(sorted(list(always_labels)))

    if optional_properties != set():
        properties = ":".join(sorted(list(always_properties)))+":?"+":?".join(sorted(list(optional_properties)))
    else:
        properties = ":".join(sorted(list(always_properties)))

    # if the formed cluster does not exist
    if labels+properties not in run_clusters:

        # line id
        data_line = [str(i)]
        data_line.append(labels)
        data_line.append(properties)
        data_line.append(str(k))

        writer.writerow(data_line)

        run_clusters.append(labels+properties)

        new_parent_id = i

        k+=1

        i+=1

        # search for more subtypes
        for sous_cluster in cluster.get_son():
            if sous_cluster is not None: ##inutile
                i,_ = rec_storing(sous_cluster, writer, i, parent_id, run_clusters, k)

    return i,k