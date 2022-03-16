""" Script used to make the sampling of data """

# Imports
import random
from termcolor import colored
from .node import Graph, Node
from numpy.random import binomial
from ..settings import global_variable

def sampling(graph, percent):
    new_graph = Graph()
    unused = dict()
    for node in graph.get_nodes():
        nb = binomial(graph.occurs(node), percent/100.)
        if nb != 0:
            new_graph.add_node(node, nb)
        if nb != graph.occurs(node):
            unused[node] = graph.occurs(node)  - nb
    global_variable("unused", unused)
    return new_graph
