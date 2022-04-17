# DiscoPG: Property Graph Schema and Exploration

## About the project

DiscoPG is a property graph schema discovery and exploration system. It leverages hierarchical clustering, using a Gaussian Mixture Model (GMM), which accounts for both node labels and properties, i.e., the [GMMSchema method](https://openproceedings.org/2022/conf/edbt/paper-139.pdf).
DiscoPG consists of the following modules:

   * **Schema Discovery**:  Given a property graph dataset, the system performs data pre-processing and applies a GMM-based schema discovery algorithm, GMM-S.  Upon updates to the base input dataset, the computed schema can be maintained using either an incremental algorithm (I-GMM-D) or an algorithm performing memoization-based recomputation (GMM-D).
   * **Schema Exploration**: Users can navigate the discovered schema graphs, by examining the labels and properties associated to both its nodes and edges. Moreover, they can visualize the proportion of node instances for each node type, as these are reflected by the cluster sizes. In the dynamic case, the individual impact of the changes to the relevant clusters is represented through their custom color coding.
   * **Schema Dashboard**: Users can inspect the performance of DiscoPG's algorithms and the quality of its produced schemas. As an additional functionality, providing a wider view of the computed metrics, the module also enables users to log the results obtained with various parameter configurations, across several datasets

## Dependencies

Use pip to install these 3 python modules : 
- termcolor
- hdbscan==0.8.27
- neo4j==4.3.4

Neo4j :
- Neo4j Desktop 1.4.8
- Add local DBMS with a Neo4j version of 3.5.3 or more

Django : 4.0

## Imports for LDBC, fib25 and mb6

Download the csv files from the databases folder.

Follow [these instructions](https://github.com/connectome-neuprint/neuPrint/blob/master/neo4j_desktop_load.md) to import LDBC, fib25 or mb6 (steps 1 to 6 are already done).

At step 10 of the previous page for LDBC and fib25, you will need a command to load the data.

For LDBC :
```
./bin/neo4j-admin import --database=ldbc.db --delimiter='|' --nodes=Comment=import/comment_0_0.csv --nodes=Forum=import/forum_0_0.csv --nodes=Person=import/person_0_0.csv --nodes=Post=import/post_0_0.csv --nodes=Place=import/place_0_0.csv --nodes=Organisation=import/organisation_0_0.csv --nodes=TagClass=import/tagclass_0_0.csv --nodes=Tag=import/tag_0_0.csv --relationships=HAS_CREATOR=import/comment_hasCreator_person_0_0.csv --relationships=HAS_TAG=import/comment_hasTag_tag_0_0.csv --relationships=IS_LOCATED_IN=import/comment_isLocatedIn_place_0_0.csv --relationships=REPLY_OF=import/comment_replyOf_comment_0_0.csv --relationships=REPLY_OF=import/comment_replyOf_post_0_0.csv --relationships=CONTAINER_OF=import/forum_containerOf_post_0_0.csv --relationships=HAS_MEMBER=import/forum_hasMember_person_0_0.csv --relationships=HAS_MODERATOR=import/forum_hasModerator_person_0_0.csv --relationships=HAS_TAG=import/forum_hasTag_tag_0_0.csv --relationships=HAS_INTEREST=import/person_hasInterest_tag_0_0.csv --relationships=IS_LOCATED_IN=import/person_isLocatedIn_place_0_0.csv --relationships=KNOWS=import/person_knows_person_0_0.csv --relationships=LIKES=import/person_likes_comment_0_0.csv --relationships=LIKES=import/person_likes_post_0_0.csv --relationships=STUDIES_AT=import/person_studyAt_organisation_0_0.csv --relationships=WORKS_AT=import/person_workAt_organisation_0_0.csv --relationships=HAS_CREATOR=import/post_hasCreator_person_0_0.csv --relationships=HAS_TAG=import/post_hasTag_tag_0_0.csv --relationships=IS_LOCATED_IN=import/post_isLocatedIn_place_0_0.csv --relationships=IS_LOCATED_IN=import/organisation_isLocatedIn_place_0_0.csv --relationships=IS_PART_OF=import/place_isPartOf_place_0_0.csv --relationships=HAS_TYPE=import/tag_hasType_tagclass_0_0.csv --relationships=IS_SUBCLASS_OF=import/tagclass_isSubclassOf_tagclass_0_0.csv
```

For fib25 : 
```
/bin/neo4j-admin import --database=fib25.db --nodes=import/Neuprint_Meta_fib25.csv --nodes=import/Neuprint_Neurons_fib25.csv --relationships=ConnectsTo=import/Neuprint_Neuron_Connections_fib25.csv --nodes=import/Neuprint_SynapseSet_fib25.csv --relationships=ConnectsTo=import/Neuprint_SynapseSet_to_SynapseSet_fib25.csv --relationships=Contains=import/Neuprint_Neuron_to_SynapseSet_fib25.csv --nodes=import/Neuprint_Synapses_fib25.csv --relationships=SynapsesTo=import/Neuprint_Synapse_Connections_fib25.csv --relationships=Contains=import/Neuprint_SynapseSet_to_Synapses_fib25.csv
```

## Running the project

```console
$python manage.py makemigrations polls

$python manage.py migrate

$python manage.py collectstatic

$python manage.py runserver
```
Then, in your browser, go to [http://localhost:8000](http://localhost:8000).

## Project structure

The graphic part is in templates/

The part to render the graph is in static/

The IO part of the wepApp is in wepApp/

The algithmic part of the programm is in the webApp/scripts/src/

main.py : main file for GMM-S launching the different part of the algorithm
node.py : datastructure used in the project
lecture_graph.py : in GMM-S, read the graph
sampling.py : do the sampling of the read graph
clustering_algo.py : run the GMM-S algorithm
storing.py : store the inferred graph of the GMM-S algorithm
incremental_scheme.py : run the GMM-D and the I-GMM-D from getting the data to the output
eval_quality.py : do the evaluation of cluster stored in the global variables
../settings.py : used to store global variable over the whole programm

The raw output is in webApp/scripts/db.py and webApp/graph/

