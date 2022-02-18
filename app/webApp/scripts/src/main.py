""" Main script to infer a PG schema of any database using a clustering method """

# Imports
from typing import Dict
from termcolor import colored
import csv
import time

# Neo4j imports
from neo4j import GraphDatabase

# File imports
from .lecture_graph import lecture_graph
from .node import Node, Graph, Cluster
from .clustering_algo import clustering
from .sampling import sampling
from .storing import storing


def algorithm_script(params: Dict[str, str]) -> Dict[str, float]:
    print(colored("Schema inference using Gaussian Mixture Model clustering on PG\n", "red"))

    print(params)
    #{'dataset': 'ldbc', 'method': 'k-mean', 'has_limit': True, 'limit_to': 1, 'use_incremental': True, 'runs': 1}
    
    DBname = ""
    uri = ""
    user = ""
    passwd = ""

    if (params['dataset'] == 'ldbc'):
        DBname = "ldbc" 
        uri = "bolt://localhost:7687" 
        user = "neo4j"
        passwd = "1234"
    elif (params['dataset'] == 'covid-19'):
        DBname = "covid19"
        uri = "bolt://db.covidgraph.org:7687"
        user = "public"
        passwd = "corona"
    elif (params['dataset'] == 'fib25'):
        DBname = "fib25" 
        uri = "bolt://localhost:7687" 
        user = "neo4j"
        passwd = "1234"
    else:
        exit(1)
        
    # Connection a la base de donnée Neo4j
    # set encrypted to False to avoid possible errors
    driver = GraphDatabase.driver(uri, auth=(user, passwd), encrypted=False)

    print(colored("Starting to query on ", "red"),
          colored(DBname, "red"), colored(":", "red"))
    t1 = time.perf_counter()
    graph, edges = lecture_graph(driver)
    t1f = time.perf_counter()

    step1 = t1f - t1  # time to complete step 1
    print(colored("Queries are done.", "green"))
    print("Step 1: Preprocessing was completed in ", step1, "s")

    print("---------------")

    print(colored("Data sampling : ", "blue"))
    ts = time.perf_counter()
    trainning_graph = sampling(graph, params["has_limit"] , int(params["limit_to"]))
    tsf = time.perf_counter()
    steps = tsf - ts  # time to complete the sampling step
    print(colored("Separating done.", "green"))
    print("The sampling step was processed in ", steps, "s")

    print("---------------")

    print(colored("Starting to cluster data using GMM :", "red"))
    t2 = time.perf_counter()
    cluster = clustering(trainning_graph)
    t2f = time.perf_counter()

    step2 = t2f - t2  # time to complete step 2
    print(colored("Clustering done.", "green"))
    print("Step 2: Clustering was completed in ", step2, "s")

    print("---------------")

    print(colored("Writing file and identifying subtypes :", "red"))
    t3 = time.perf_counter()
    file = storing(cluster, edges, params['dataset'])
    t3f = time.perf_counter()

    step3 = t3f - t3  # time to complete step 3
    print(colored("Writing done.", "green"))
    print("Step 3: Identifying subtypes and storing to file was completed in", step3, "s")
    return {
        "t_pre": step1,
        "t_cluster": step2,
        "t_write": step3,
    }
