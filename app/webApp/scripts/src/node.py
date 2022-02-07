from typing import List, Set

class Node:
    def __init__(self, labels, propriete, edge_out = [], edge_in = []) -> None:
        self._labels = labels
        self._proprety = propriete
        self._out = edge_out
        self._in = edge_in

    def get_labels(self) -> Set[str]:
        return self._labels

    def get_proprety(self) -> Set[str]:
        return self._proprety

    def __str__(self) -> str:
        mot = "Labels : "
        for l in self._labels:
            mot += l + ", "
        mot += "  |   Property : "
        for p in self._proprety:
            mot += p + ", "
        return mot
    
    def __eq__(self, other):

        return self._labels == other._labels and self._proprety == other._proprety and self._out == other._out and self._in == other._in
    
    def __hash__(self):

        tuple_retour = (frozenset(self._labels), frozenset(self._out))
        return hash(tuple_retour) 

#------------------------------------------------------------------------------

class Graph:
    def __init__(self, nodes = None) -> None:
        self._nodes = set()
        self._node_occurs = dict()
        self._labels = set()
        self._set_labels = set()
        self._proprety = set()

    def get_nodes(self) -> List[Node]:
        return self._nodes

    def add_node(self, x, n=1) -> None:
        if (x in self._nodes):
            self._node_occurs[x] += n
        else:
            self._nodes.add(x)
            self._node_occurs[x] = n
            for l in x.get_labels():
                self._labels.add(l)
            for p in x.get_proprety():
                self._proprety.add(p)
    
    def del_node(self, x):
        if x in self._nodes:
            self._nodes.pop(x)
        if x in self._node_occurs:
            del self._node_occurs[x]

    def distinct_node(self) -> Set[Node]:
        return self._nodes
    
    def get_sets_labels(self):
        s = list({"#".join(list(n.get_labels())) for n in self._nodes})
        return [set(x.split("#")) for x in s]

    def occurs(self, node):
        return self._node_occurs[node]

    def __str__(self) -> str:
        mot = ""
        for n in self._nodes:
            mot += str(n) + "\n"
        return mot

#------------------------------------------------------------------------------

class Cluster:
    def __init__(self, name = "") -> None:
        self._name = name
        self._ref_node = None
        self._cutting_values = []
        self._nodes = dict()
        self._fils = []
        self._modification = 0
        self._sons_id = None
    
    def get_nodes(self):
        return self._nodes

    def add_son(self, sous_cluster):
        self._fils.append(sous_cluster)

    def get_son(self):
        return self._fils

    def get_name(self):
        return self._name
    
    def add_node(self, node):
        if node in self._nodes:
            self._nodes[node] += 1
        else:
            self._nodes[node] = 1
    
    def get_sons_id(self):
        if self._sons_id == None:
            l = self.get_son()
            return {frozenset(cluster._nodes().items()) : l for cluster in l}
        else:
            return self._sons_id
