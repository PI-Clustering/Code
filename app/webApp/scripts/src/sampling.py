""" Script used to make the sampling of data """

##### Imports
import random
from termcolor import colored
from node import Graph, Node
from math import ceil


def sampling(graph, training_percentage = 100):

    # get the number of occurrences of each node in a variable
    new_graph = Graph()

    for node in graph.get_nodes():
        new_graph.add_node(node, int(graph.occurs(node)*ceil(training_percentage/100.)))

    return new_graph




