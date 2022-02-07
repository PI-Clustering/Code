""" Step 1 : Preprocessing data """

##### Imports
from termcolor import colored

#### File import
from .debug import printb
from .node import Graph, Node
from time import time

def lecture_graph(driver):
   with driver.session() as session:

        #We do one query to get all differents set of labels
        print(colored("Querying neo4j to get a part of the graph:", "yellow"))
        nodes = session.run(
            "MATCH(n) \
            RETURN DISTINCT labels(n), keys(n), COUNT(n)"
            )

        graph = Graph()
        for node in nodes:
            labels = set(node["labels(n)"])
            properties = set(node["keys(n)"])
            count = node["COUNT(n)"]
            n = Node(labels, properties)

            graph.add_node(n,count)
    
        print(colored("Done.", "green"))
        printb(graph)

        #Query sur le schema du graph
        schema = session.run("CALL db.schema.visualization")
        schema =list(schema)[0]

        return graph,schema
