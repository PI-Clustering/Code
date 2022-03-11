""" Main script to infer a PG schema of any database using a clustering method """

# Imports
from typing import Dict
from termcolor import colored
import csv
import time
import os

# Neo4j imports
from neo4j import GraphDatabase

# File imports
from .lecture_graph import lecture_graph
from .node import Node, Graph, Cluster
from .clustering_algo import clustering
from .sampling import sampling
from .storing import storing
from .eval_quality import eval_quality
from ...models import Benchmark, DataPoint
from ..settings import global_variable

from .debug import *

def algorithm_script(params: Dict[str, str]):

    print(colored("Schema inference using Gaussian Mixture Model clustering on PG\n", "red"))

    #{'dataset': 'ldbc', 'method': 'k-mean', 'has_limit': False, 'limit_to': 5, 'use_incremental': False, 'nb_subcluster': 1}
    DBname = ""
    uri = ""
    user = ""
    passwd = ""

    if params['use_precomputed']:
    
        dirname = os.path.dirname(__file__)
        
        if (params['dataset'] == 'ldbc'):
            os.system("cp " + str(os.path.join(dirname, "../graph/node_ldbc.csv")) + " " + str(os.path.join(dirname, "../graph/node.csv")))
            os.system("cp " + str(os.path.join(dirname, "../graph/edge_ldbc.csv")) + " " + str(os.path.join(dirname, "../graph/edge.csv")))            
            os.system("cp " + str(os.path.join(dirname, "../graph/db_ldbc.sqlite3"))+ " " + str(os.path.join(dirname, "../../../db.sqlite3")))

        elif (params['dataset'] == 'covid-19'):
            os.system("cp " + str(os.path.join(dirname, "../graph/node_covid-19.csv")) + " " + str(os.path.join(dirname, "../graph/node.csv")))
            os.system("cp " + str(os.path.join(dirname, "../graph/edge_covid-19.csv")) + " " + str(os.path.join(dirname, "../graph/edge.csv")))
            os.system("cp " + str(os.path.join(dirname, "../graph/db_covid-19.sqlite3"))+ " " + str(os.path.join(dirname, "../../../db.sqlite3")))
        elif (params['dataset'] == 'fib25'):
            os.system("cp " + str(os.path.join(dirname, "../graph/node_fib25.csv")) + " " + str(os.path.join(dirname, "../graph/node.csv")))
            os.system("cp " + str(os.path.join(dirname, "../graph/edge_fib25.csv")) + " " + str(os.path.join(dirname, "../graph/edge.csv")))
            os.system("cp " + str(os.path.join(dirname, "../graph/db_fib25.sqlite3"))+ " " + str(os.path.join(dirname, "../../../db.sqlite3")))

        else:
            exit(1)
        
        return (0,0,0)
        

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
    graph, edges = lecture_graph(driver, params['query_edge'])
    t1f = time.perf_counter()

    global_variable("edges", edges)

    step1 = t1f - t1  # time to complete step 1
    print(colored("Queries are done.", "green"))
    print("Step 1: Preprocessing was completed in ", step1, "s")

    print("---------------")

    print(colored("Data sampling : ", "blue"))
    ts = time.perf_counter()
    trainning_graph = sampling(graph, int(params["limit_to"]))
    tsf = time.perf_counter()
    steps = tsf - ts  # time to complete the sampling step
    print(colored("Separating done.", "green"))
    print("The sampling step was processed in ", steps, "s")

    print("---------------")

    bm = Benchmark.objects.create(
        algo_type='Compute cluster',
        data_set=params['dataset'],
        n_iterations=0,
        size=sum(trainning_graph._node_occurs.values()),
        t_pre = 0,
        t_cluster = 0,
        t_write = 0
    )

    global_variable("bm", bm)

    print(colored("Starting to cluster data using GMM :", "red"))
    t2 = time.perf_counter()
    cluster = clustering(trainning_graph, int(params["nb_subcluster"]))
    t2f = time.perf_counter()

    step2 = t2f - t2  # time to complete step 2
    print(colored("Clustering done.", "green"))
    print("Step 2: Clustering was completed in ", step2, "s")

    print("---------------")
    print(colored("Writing file and identifying subtypes :", "red"))
    t3 = time.perf_counter()
    file = storing(cluster, edges, params['dataset'])
    if params["evaluate"]:
        eval_quality()
    t3f = time.perf_counter()

    step3 = t3f - t3  # time to complete step 3
    print(colored("Writing done.", "green"))
    print("Step 3: Identifying subtypes and storing to file was completed in", step3, "s")
    
    Benchmark.objects.filter(pk=bm.pk).update(t_pre = step1+steps, t_cluster = step2, t_write = step3)

    print_dict_node(cluster)

    return {
        "t_pre": step1,
        "t_cluster": step2,
        "t_write": step3,
    }

