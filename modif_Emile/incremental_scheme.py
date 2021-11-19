""" Import what need to be import """


def add_node(node, hierarchy, tree_of_value, start):
    
    pos = -1
    for j in len(start):
        if start[j] == set(node[0]):
            pos = j
    if pos == -1:
        hierarchy.append([node])
        tree_of_value.append([])
        start.append(set(node[0]))
    
    else:
        
        

def add_node_hierarchy(node, hierarchy, tree_of_value):
    
    if type(hierarchy) == type([]):
        s = dist(node, tree_of_value[0])
        if s < tree_of_value[1]:
            return [add_node_hierarchy(node, hierarchy[0], tree_of_value[2]), hierarchy[1]]
        else:
            return [hierarchy[0], add_node_hierarchy(node, hierarchy[1], tree_ov_value[3])]
    
    else :
        return [hierarchy, node]
