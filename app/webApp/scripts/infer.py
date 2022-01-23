""" Script to create a Neo4j graph with """

### Imports
import csv

### Neo4j imports
from neo4j import GraphDatabase

def create_neo4j_graph(driver2, edges=True):
    """ Create a Neo4j graph 

    Parameters
    ----------
    driver2 : GraphDatabase.driver object
        Driver used to access the PG stored in a Neo4j database.
    edges : Boolean.
        If edges is set at True by default.
        When edges is at True, add all edges to the Neo4j graph.
        When edges is at False, only add edges SUBTYPE_OF.

    Returns
    -------
    A Neo4j graph representation of the inferred schema
    """

    if edges:
        with driver2.session() as session:
            query = "MATCH (n)-[r]->(m) \
                RETURN DISTINCT labels(n),keys(n),type(r),labels(m),keys(m)"
            edge_types = session.run(query)

            all_labels_n = []
            all_keys_n = []
            all_type_r = []
            all_keys_m = []
            all_labels_m = []

            for edge_type in edge_types:
                all_labels_n.append(":".join(sorted(edge_type["labels(n)"])))
                all_keys_n.append(":".join(sorted(edge_type["keys(n)"])))
                all_type_r.append(edge_type["type(r)"])
                all_labels_m.append(":".join(sorted(edge_type["labels(m)"])))
                all_keys_m.append(":".join(sorted(edge_type["keys(m)"])))

        print("Arêtes récupérées !")

    uri = input("Neo4j bolt address: ")
    user = input("Neo4j username: ")
    passwd = input('Neo4j password: ')
    file = input('Create the Neo4j graph from which file ? : ')
    driver = GraphDatabase.driver(uri, auth=(user, passwd), encrypted=False)

    with driver.session() as session:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            ind_dict={}
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    label = row[4]
                    labels = ":".join(sorted(row[1].split(":")))
                    props = ":".join(sorted(row[2].split(":")))
                    ind_dict[row[0]] = [label,labels,props]

                    # for base type
                    if row[5] == "yes":

                        # neo4j node creation query
                        query="CREATE (n:"+label+" {labels:'"+labels+"',props:'"+props+"'})"
                        session.run(query)
                    else:
                        parent = row[3]
                        label_parent = ind_dict[parent][0]
                        labels_parent = ind_dict[parent][1]
                        props_parent = ind_dict[parent][2]

                        # neo4j node creation query
                        query = "CREATE (n:"+label+" {labels:'"+labels+"',props:'"+props+"'})"
                        session.run(query)

                        # neo4j subtype_of edge creation query
                        query = "MATCH(n:"+label+"),(m:"+label_parent+")"+"WHERE n.labels='"+labels+"' AND n.props='"+props+"' AND m.labels='"+labels_parent+"' AND m.props='"+props_parent+"' CREATE (n)-[r:SUBTYPE_OF]->(m)"
                        session.run(query)

    if edges:
        with driver.session() as session:
            for i in range(len(all_labels_n)):
                labels_n = all_labels_n[i]
                keys_n = all_keys_n[i]
                type_r = all_type_r[i]
                labels_m = all_labels_m[i]
                keys_m = all_keys_m[i]

                query = "MATCH(n),(m) WHERE n.labels='"+labels_n+"' AND n.props='"+keys_n+"' AND m.labels='"+labels_m+"' AND m.props='"+keys_m+"' CREATE (n)-[r:"+type_r+"]->(m)"
                session.run(query)