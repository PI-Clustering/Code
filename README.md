# DiscoPG: Property Graph Schema and Exploration

## To cite us, use the following BibTex references:

```
@article{DBLP:journals/pvldb/BonifatiDMGJLP22,
  author    = {Angela Bonifati and
               Stefania{-}Gabriela Dumbrava and
               Emile Martinez and
               Fatemeh Ghasemi and
               Malo Jaffr{\'{e}} and
               Pacome Luton and
               Thomas Pickles},
  title     = {DiscoPG: Property Graph Schema Discovery and Exploration},
  journal   = {Proc. {VLDB} Endow.},
  volume    = {15},
  number    = {12},
  pages     = {3654--3657},
  year      = {2022}
}
```

```
@inproceedings{DBLP:conf/edbt/BonifatiDM22,
  author    = {Angela Bonifati and
               Stefania Dumbrava and
               Nicolas Mir},
  title     = {Hierarchical Clustering for Property Graph Schema Discovery},
  booktitle = {{EDBT}},
  pages     = {2:449--2:453},
  publisher = {OpenProceedings.org},
  year      = {2022}
}
```

## About the project

DiscoPG is a property graph schema discovery and exploration system. It leverages hierarchical clustering, using a Gaussian Mixture Model (GMM), which accounts for both node labels and properties, i.e., the [GMMSchema method](https://openproceedings.org/2022/conf/edbt/paper-139.pdf), whose code is here [GMMSchema codebase](https://github.com/naussicaa/pg-schemainference/blob/main/README.md).
DiscoPG consists of the following modules:

   * **Schema Discovery**:  Given a property graph dataset, the system performs data pre-processing and applies a GMM-based schema discovery algorithm, GMM-S.  Upon updates to the base input dataset, the computed schema can be maintained using either an incremental algorithm (I-GMM-D) or an algorithm performing memoization-based recomputation (GMM-D).
   * **Schema Exploration**: Users can navigate the discovered schema graphs, by examining the labels and properties associated to both its nodes and edges. Moreover, they can visualize the proportion of node instances for each node type, as these are reflected by the cluster sizes. In the dynamic case, the individual impact of the changes to the relevant clusters is represented through their custom color coding.
   * **Schema Dashboard**: Users can inspect the performance of DiscoPG's algorithms and the quality of its produced schemas. As an additional functionality, providing a wider view of the computed metrics, the module also enables users to log the results obtained with various parameter configurations, across several datasets

## Dependencies

Use pip to install these 3 python modules : 
- termcolor
- hdbscan==0.8.28
- neo4j==4.3.4
- django==4.1.1
- joblib==0.11 (to do after hdbscan)

(and eventually matplolib and numpy if not already installed)

Neo4j :
- Neo4j Desktop 1.4.8
- Add local DBMS with a Neo4j version of 3.5.3 or more

Django : 4.0

## Imports for LDBC, fib25 and mb6

Download the csv files from the databases folder.

Follow [these instructions](https://github.com/connectome-neuprint/neuPrint/blob/master/neo4j_desktop_load.md) to import LDBC or fib25 

At step 5, put neo4j as graph name and 1234 as password
At step 10, of the previous page for LDBC and fib25, you will need a command to load the data.
At step 11, `mb6.db` can be change by `ldbc.db` or `fib25.db` and (but apparently not necessary) also add the line `dbms.connector.bolt.listen_address=:7687`

For LDBC :
```
./bin/neo4j-admin import --database=ldbc.db --delimiter='|' --nodes=Comment=import/comment_0_0.csv --nodes=Forum=import/forum_0_0.csv --nodes=Person=import/person_0_0.csv --nodes=Post=import/post_0_0.csv --nodes=Place=import/place_0_0.csv --nodes=Organisation=import/organisation_0_0.csv --nodes=TagClass=import/tagclass_0_0.csv --nodes=Tag=import/tag_0_0.csv --relationships=HAS_CREATOR=import/comment_hasCreator_person_0_0.csv --relationships=HAS_TAG=import/comment_hasTag_tag_0_0.csv --relationships=IS_LOCATED_IN=import/comment_isLocatedIn_place_0_0.csv --relationships=REPLY_OF=import/comment_replyOf_comment_0_0.csv --relationships=REPLY_OF=import/comment_replyOf_post_0_0.csv --relationships=CONTAINER_OF=import/forum_containerOf_post_0_0.csv --relationships=HAS_MEMBER=import/forum_hasMember_person_0_0.csv --relationships=HAS_MODERATOR=import/forum_hasModerator_person_0_0.csv --relationships=HAS_TAG=import/forum_hasTag_tag_0_0.csv --relationships=HAS_INTEREST=import/person_hasInterest_tag_0_0.csv --relationships=IS_LOCATED_IN=import/person_isLocatedIn_place_0_0.csv --relationships=KNOWS=import/person_knows_person_0_0.csv --relationships=LIKES=import/person_likes_comment_0_0.csv --relationships=LIKES=import/person_likes_post_0_0.csv --relationships=STUDIES_AT=import/person_studyAt_organisation_0_0.csv --relationships=WORKS_AT=import/person_workAt_organisation_0_0.csv --relationships=HAS_CREATOR=import/post_hasCreator_person_0_0.csv --relationships=HAS_TAG=import/post_hasTag_tag_0_0.csv --relationships=IS_LOCATED_IN=import/post_isLocatedIn_place_0_0.csv --relationships=IS_LOCATED_IN=import/organisation_isLocatedIn_place_0_0.csv --relationships=IS_PART_OF=import/place_isPartOf_place_0_0.csv --relationships=HAS_TYPE=import/tag_hasType_tagclass_0_0.csv --relationships=IS_SUBCLASS_OF=import/tagclass_isSubclassOf_tagclass_0_0.csv
```

For fib25 : 
```
./bin/neo4j-admin import --database=fib25.db --nodes=import/Neuprint_Meta_fib25.csv --nodes=import/Neuprint_Neurons_fib25.csv --relationships=ConnectsTo=import/Neuprint_Neuron_Connections_fib25.csv --nodes=import/Neuprint_SynapseSet_fib25.csv --relationships=ConnectsTo=import/Neuprint_SynapseSet_to_SynapseSet_fib25.csv --relationships=Contains=import/Neuprint_Neuron_to_SynapseSet_fib25.csv --nodes=import/Neuprint_Synapses_fib25.csv --relationships=SynapsesTo=import/Neuprint_Synapse_Connections_fib25.csv --relationships=Contains=import/Neuprint_SynapseSet_to_Synapses_fib25.csv
```

## The Covid-19 graph codebase is accessible here: [Cord-19](https://github.com/covidgraph/data_cord19).

## Running the project

```console
$python manage.py makemigrations polls

$python manage.py migrate

$python manage.py collectstatic

$python manage.py runserver
```
Then, in your browser, go to [http://localhost:8000](http://localhost:8000).

## Project structure

* Graphical part: `templates/`

* Graph rendering: `static/`

* IO part of the wepApp: `wepApp/`

* Algorithmic part of the program: `webApp/scripts/src/`

  * `main.py` : entry point for the GMM-S, static schema discovery algorithm
  * `node.py` : main data structures 
  * `lecture_graph.py` : reading the graph for GMM-S
  * `sampling.py` : sampling the read graph
  * `clustering_algo.py` : running the GMM-S algorithm
  * `storing.py` : storing the graph inferred by the GMM-S algorithm
  * `incremental_scheme.py` : running the GMM-D and the I-GMM-D dynamic schema discovery algorithms
  * `eval_quality.py` : evaluating the quality of the computed clustering
  * `../settings.py` : storing global variables

The raw output is in `webApp/scripts/db.py` and `webApp/graph/`

