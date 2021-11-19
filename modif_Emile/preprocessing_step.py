""" Step 1 : Preprocessing data """

##### Imports
from termcolor import colored

def preprocessing(driver):
    """  Queries a property graph using the driver to get all needed labels',properties' and nodes' information

    Parameters
    ----------
    driver : GraphDatabase.driver object
        Driver used to access the PG stored in a Neo4j database.

    Returns
    -------
    amount_dict : Python dict
        A dictionary with node strings as keys and the number of occurrences of the node as a value
        Its format is : {'Label1 Label2 Label3 prop1 prop2 prop3 ...': int, ...}
    list_of_distinct_nodes : Python list
        A list of node strings
        Its format is : ['Label1 Label2 prop1', 'Label1 Label3 prop2', 'prop4 prop5', ...]
    distinct_labels : Python list
        A list of labels
        Its format is : ['Label1', 'Label2', 'Label3', ...]
    labs_sets : Python list of list
        A list of all labels sets
        Its format is : [['Label 1','Label2'],['Label1'],['Label3'],...]
    """
    
    print(colored("Querying neo4j to get all distinct labels:", "yellow"))
    
"""    with open("test.txt", "r") as f:
        s = f.read()
        distinct_nodes = ""
        for i in s:
            if i == "\n":
                distinct_nodes += ", "
            else:
                distinct_nodes += i
        
        distinct_nodes = eval(distinct_nodes)[0]"""
    distinct_nodes = [(['Comment'], ['browserUsed', 'content', 'creationDate', 'id', 'length', 'locationIP'], 2052169), (['Organisation'], ['id', 'name', 'type', 'url'], 7955), (['Post'], ['browserUsed', 'content', 'creationDate', 'id', 'language', 'length', 'locationIP'], 206972), (['Post'], ['browserUsed', 'creationDate', 'id', 'imageFile', 'length', 'locationIP'], 796633), (['Tag'], ['id', 'name', 'url'], 16080), (['TagClass'], ['id', 'name', 'url'], 71), (['Person'], ['birthday', 'browserUsed', 'creationDate', 'firstName', 'gender', 'id', 'lastName', 'locationIP'], 9892), (['Place'], ['id', 'name', 'type', 'url'], 1460), (['Forum'], ['creationDate', 'id', 'title'], 90492)]
    
    
    distinct_labels = list(set([lab for ls in distinct_nodes for lab in ls[0]]))
    labels_sets = [ls[0] for ls in distinct_nodes]
    labs_sets = []
    for x in labels_sets:
        if x not in labs_sets:
            labs_sets.append(x)
    
    # Storing the number of repetitions of the node
    amount_dict = {}

    # transform neo4j dict to python list of string
    list_of_distinct_nodes=[]

    for node in distinct_nodes:
        #get a list of labels
        labels = sorted(node[0])

        #get a list of properties
        properties = sorted(node[1])

#        labels_properties = labels+properties
#        labels_properties_str = ' '.join(labels_properties)
        if (tuple(labels), tuple(properties)) in list_of_distinct_nodes:
            amount_dict[(tuple(labels), tuple(properties))] += node[2]
        else:
            list_of_distinct_nodes.append((tuple(labels), tuple(properties))) 
            amount_dict[(tuple(labels), tuple(properties))] = node[2]
    print(colored("Done.", "green"))

    
    return amount_dict,list_of_distinct_nodes,distinct_labels,labs_sets
