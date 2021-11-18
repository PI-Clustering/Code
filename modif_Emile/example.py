### Imports
import csv
import time

### Neo4j imports
from neo4j import GraphDatabase

uri = input("Neo4j bolt address: ")
user = input("Neo4j username: ")
passwd = input('Neo4j password: ')

driver = GraphDatabase.driver(uri, auth=(user, passwd), encrypted=False)

def execute_query(query,driver):
	with driver.session() as session:
		t1 = time.perf_counter()
		session.run(query)
		tf1 = time.perf_counter()
		print("Executing time: ", tf1-t1)

query="MATCH (n) RETURN labels(n)"
query2="MATCH (n)-[r]-(m) RETURN n,r,m LIMIT 1000"
l = (query,query2)
m = (driver,driver)

t1 = time.perf_counter()
for elt in l:
	execute_query(elt,driver)
tf1 = time.perf_counter()
print("Total executing time: ", tf1-t1)