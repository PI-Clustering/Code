from termcolor import colored
from .node import *

debug = False

def printb(string):
    if (debug):
        print(string)


def print_cutting_value(cluster):

    print(cluster._cutting_values, "          ",cluster.get_son())
    for c in cluster.get_son():
        print_cutting_value(c)

def print_id_son(cluster):
    print(id(cluster), "  :  ", [id(c) for c in cluster.get_son()])
    for c in cluster.get_son():
        print_id_son(c)


def print_dict_node(cluster):

    print(cluster.get_nodes())
    print("\n\n\n")
    for c in cluster.get_son():
        print_dict_node(c)
    