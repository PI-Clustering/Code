from neo4j import GraphDatabase
from neo4j import Query
import os
import time
from random import randint


def get_benchmark(algo, dataset):
    time = randint(20, 50)
    size = randint(500, 1000)
    url = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    username = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "1234")
    neo4jVersion = os.getenv("NEO4J_VERSION", "4")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    port = os.getenv("PORT", 8080)
    # driver=GraphDatabase.driver(url,username,password)
    results = driver.get_result("hello, world")
    bm = {
        'time': time,
        'size': size,
        'algo': algo,
        'name': results[0]
    }
    print(f"result is {bm}")
    return bm


class QueryBuilder:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_result(self, message):
        with self.driver.session() as session:
            t1 = time.perf_counter()
            return session.read_transaction(self._do_query, message)
            # evaluate

    @staticmethod
    def _do_query(tx, person_name):
        query1 = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        query2 = (
            "MATCH (n:Person)-[r]-(m) "
            "RETURN n,r,m LIMIT 5"
        )
        # result = tx.run(query1, person_name=person_name)
        result = tx.run(query2, person_name=person_name)
        return [record["n"]["firstName"] for record in result]


if __name__ == "__main__":
    url = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    username = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "1234")
    neo4jVersion = os.getenv("NEO4J_VERSION", "4")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    port = os.getenv("PORT", 8080)

    driver = QueryBuilder(url, username, password)
    get_benchmark(driver, "kmeans", "LDBC")
    driver.close()
