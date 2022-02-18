""" Script used to make the sampling of data """

# Imports
import random
from termcolor import colored
from .node import Graph, Node
from math import ceil


def sampling(graph, boolean, percent):
    if not boolean:
        return graph

    # get the number of occurrences of each node in a variable
    new_graph = Graph()

    for node in graph.get_nodes():
        new_graph.add_node(node, int(graph.occurs(
            node)*percent/100.))

    return new_graph
