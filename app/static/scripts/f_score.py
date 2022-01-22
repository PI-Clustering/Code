""" Compute the f-score for LDBC's database """

##### Imports
from sklearn.metrics import f1_score
import csv

def construct(file,list_of_distinct_nodes,distinct_labels):
    """ Create the ground truth and the predictions' vectors
    
    Parameters
    ----------
    file : String
        Name of the file with the clusters
    list_of_distinct_nodes : Python list
        A list of node strings representing all unique nodes in the test set
        Its format is : ['Label1 prop1 prop2 prop3', 'Label1 prop1 prop2', 'Label1 prop1 prop2 prop4', ...]
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]

    Returns
    -------
    ground_truth : Python list
        A list of the base types representing the nodes
    predictions : Python list
        A list of the inferred base types for the same nodes as in ground_truth

    """

    ### Construct the predictions list
    row_dict = {}
    type_dict = {}
    j=0

    # iterate through each different node
    for node in list_of_distinct_nodes:

        type_dict_list = []
        node_list = node.split(" ")

        with open(file,newline="") as f:
            reader=csv.reader(f,delimiter=",")
            i=0

            # iterate through each different inferred types
            for row in reader:
                is_type = True

                # header
                if i==0:
                    i+=1
                else:
                    if j==0:
                        row_dict[row[0]] = row
                    labs = row[1].split(":")
                    props = row[2].split(":")

                    # if the node is labelled
                    if labs != []:
                        for elt in labs:
                            if elt not in node_list:
                                is_type=False
                                break

                    # if the node has the correct labels
                    if is_type:
                        if props != []:
                            for elt in props:
                                if elt not in node_list:
                                    is_type=False
                                    break

                    # if the node has the correct properties
                    if is_type:
                        # get the id of a possible parent type
                        type_dict_list.append(row[0])
        type_dict[node] = type_dict_list
        j+=1


    predictions = []

    # iterate through each different node
    for node in list_of_distinct_nodes:

        # chose a parent type for the cluster
        m = min(type_dict[node])

        # get the base type
        labs = row_dict[m][1]

        predictions.append(labs)

    ### Construct the ground truth list
    ground_truth = []

    # iterate through each different node
    for node in list_of_distinct_nodes:
        cur_labels = []
        node_list = node.split(" ")

        # iterate through each label or property in the node
        for lab_prop in node_list:

            # if it is a label
            if lab_prop in distinct_labels:
                cur_labels.append(lab_prop)

        # the base type is its labels
        ground_truth.append(":".join(cur_labels))

    return ground_truth,predictions

def compute_f_score(test, distinct_labels, file):
    """ Computes a f1-score in the test set

    Parameters
    ----------
    test : Python list
        A list of node strings representing all unique nodes in the test set
        Its format is : ['Label1 prop1 prop2 prop3', 'Label1 prop1 prop2', 'Label1 prop1 prop2 prop4', ...]
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]
    file : String
        Name of the file with the clusters

    Returns
    -------
    f1_score : 

    """
    list_of_distinct_nodes = list(set(test))
    ground_truth,predictions = construct(file,list_of_distinct_nodes,distinct_labels)
    return f1_score(ground_truth, predictions, average='micro')