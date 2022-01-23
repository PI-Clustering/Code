from neo4j import GraphDatabase
import os
import time
from random import randint
from ..models import Benchmark


def get_benchmark(algo, dataset):
    time = randint(20, 50)
    size = randint(500, 1000)
    bm = {
        'time': time,
        'size': size,
        'algo': algo
    }
    return bm


class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_result(self, message):
        with self.driver.session() as session:
            t1 = time.perf_counter()
            greeting = session.write_transaction(
                self._do_query, message)
            print(greeting)

    @staticmethod
    def _do_query(tx, message):
        print(message)
        result = tx.run(
            "MATCH (n)-[r]-(m) RETURN n,r,m LIMIT 1000", message=message)
        return result.single()[0]


if __name__ == "__main__":
    url = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    username = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "1234")
    neo4jVersion = os.getenv("NEO4J_VERSION", "4")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    port = os.getenv("PORT", 8080)

    greeter = HelloWorldExample(url, username, password)
    greeter.print_result("hello, world")
    greeter.close()
