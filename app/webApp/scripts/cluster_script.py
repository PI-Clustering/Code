""" Main script to infer a PG schema of any database using a clustering method """

##### Imports
from termcolor import colored
import csv
import time

### Neo4j imports
from neo4j import GraphDatabase

### File imports
from preprocessing_step import *
from sampling import *
from GMM_clustering import *
from storing import *
from infer import *
from f_score import *
from hdbscan_indexes import *

if __name__ == "__main__":

    print(colored("Schema inference using Gaussian Mixture Model clustering on PG\n", "red"))

    ### Inputs
#    DBname = input("Name of the database: ")
#    uri = input("Neo4j bolt address: ")
#    user = input("Neo4j username: ")
#    passwd = input('Neo4j password: ')
    driver = None
    
    t1 = time.perf_counter()
    amount_dict,list_of_distinct_nodes,distinct_labels,labs_sets = preprocessing(driver)
    t1f = time.perf_counter()

    step1 = t1f - t1 # time to complete step 1
    print(colored("Queries are done.", "green"))
    print("Step 1: Preprocessing was completed in ", step1, "s")

    print("---------------")

    print(colored("Data sampling : ","blue"))
    ts = time.perf_counter()
    amount_dict,list_of_distinct_nodes,validate,test = sampling(amount_dict,list_of_distinct_nodes, 80)
    tsf = time.perf_counter()
    steps = tsf - ts # time to complete the sampling step
    print(colored("Separating done.", "green"))
    print("The sampling step was processed in ", steps, "s")

    print("---------------")

    print(colored("Starting to cluster data using GMM :","red"))
    t2 = time.perf_counter()
    all_clusters, hierarchy_tree = iter_gmm(amount_dict, list_of_distinct_nodes, distinct_labels, labs_sets)
    t2f = time.perf_counter()

    step2 = t2f - t2 # time to complete step 2
    print(colored("Clustering done.", "green"))
    print("Step 2: Clustering was completed in ", step2, "s")

    print("---------------")

    print(colored("Writing file and identifying subtypes :","red"))
    t3 = time.perf_counter()
    file = storing(distinct_labels,labs_sets,hierarchy_tree)
    t3f = time.perf_counter()

    step3 = t3f - t3 # time to complete step 3
    print(colored("Writing done.", "green"))
    print("Step 3: Identifying subtypes and storing to file was completed in", step3, "s")

    print("---------------")

    ### Uncomment to compute the f-score

    q = input("Do you want to compute the f-score ? (only LDBC) y/n")

    if q == "y":
        f_score = compute_f_score(test, distinct_labels, file)
        print("F-score : ", f_score)
        print("---------------")

    ### Uncomment to compute Rand Index and Adjusted Mutual Information
    q2 = input("Do you want to compute the Adjusted Rand Index/Adjusted Mutual Information between this clustering and Hdbscan's one ? y/n")
    if q2 == "y":
        with open("data.csv", 'r') as f:
            text = f.readlines()
        len_X = len(text)-1 # header and last blank line
        print(len_X)
        ari,ami = hdbscan_indexes(validate, distinct_labels, len_X)
        print("Rand Index : ",ari)
        print("Adjusted Mutual Information : ",ami)

    ### Uncomment to create a Neo4j with the resulting infered schema
    q3 = input("Do you want to create a neo4j graph ? y/n")

    if q3 == "y":
        q4 = input("Do you want to add all edges (ie. also non SUBTYPEOF edges ? y/n")
        t4 = time.perf_counter()
        create_neo4j_graph(driver, q4=="y")
        t4f = time.perf_counter()

        step4 = t4f - t4
        print(colored("Graph created.", "green"))
        print("Step 4: Creating neo4j graph was completed in ", step4, "s")
