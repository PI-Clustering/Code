""" Script used to make the sampling of data """

# Imports
import random
from termcolor import colored
from .node import Graph, Node
from numpy.random import binomial
from ..settings import global_variable
from math import ceil, floor

def sampling(graph, percent):
    new_graph = Graph()
    unused = dict()
    for node in graph.get_nodes():
        new_graph.add_node(node, ceil(graph.occurs(node)*percent/100.))
        unused[node] = max(graph.occurs(node)  - floor(graph.occurs(node)*percent/100.), 0)
    global_variable("unused", unused)
    return new_graph
