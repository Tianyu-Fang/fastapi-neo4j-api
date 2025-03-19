"""
This is a minimally-functional package designed to mimic the neo4j python driver. 
It connects to a psotgres database with the apache age extensions. 
"""

from pydantic import BaseModel
import psycopg2
import os
import json
from dataclasses import dataclass


class GraphDatabase:
    def driver(url, auth):
        return GraphDatabaseDriver(url, auth)


@dataclass
class QueryExecutionSummary:
    query = None
    counters = {
        "_contains_updates": False,
        "labels_added": 0,
        "relationships_created": 0,
        "nodes_created": 0,
        "properties_set": 0,
    }
    result_available_after = None
    plan = None
    summary_notifications = []


@dataclass
class QueryExecutionResult:
    # for record in records: print(record.data())  # obtain record as dict
    records = None
    summary = QueryExecutionSummary()
    keys = None


class GraphDatabaseDriver:
    def __init__(self, url, auth):

        # Filter neo4j protocol specification 
        url_parts = url.split("://")
        if url_parts[0] in ["neo4j", "bolt"]:
            url = "".join(url_parts[1:])
        
        # Extract port and host
        url_parts = url.split(":")
        if url_parts[::-1][0].isdigit():
            # Port specified in url
            self.port = url_parts[::-1][0]
            self.host = "".join(url_parts[0:len(url_parts)-1])
        else:
            # Port unspecified, use defualt 
            self.port = "5432"
            self.host = host
        print(f"Host {self.host} port {self.port}")

        self.user = auth[0]
        self.password = auth[1]
        self.dbname = "db" # Should be variable? 

        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        print(f"Connecting to {self.host}:{self.port} database {self.dbname} as {self.user} with password {self.password}")
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        print("Connection success!")
        self.cursor = self.conn.cursor()
        print("Cursor success!")
        # Load AGE and set search_path
        self.cursor.execute("LOAD 'age';")
        self.cursor.execute("SET search_path TO ag_catalog, \"$user\", public;")
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.cursor.close()
        self.cursor = None
        self.conn = None
    
    def verify_connectivity(self):
        print("Todo: Verify connectivity")
        # execute an example query, see if it returns 
        pass

    def execute_query(self, query, **kwargs):
        # Fill params
        print("Todo: Parameter filling")
        query = query

        new_query = ""
        in_param = True
        for part in re.split(" ", query):
            in_param = not in_param
            
            if in_param:
                part = 
            
            new_query += part
        query = new_query

        
        database = kwargs["database_"]
        translated_query = f"SELECT * FROM ag_catalog.cypher('{database}', $$ {query} $$) AS (result agtype);"

        try:
            self.cursor.execute(translated_query)
            raw_results = self.cursor.fetchall()
            self.conn.commit()

            # Clean up the results (remove "::vertex" and parse JSON)
            formatted_results = []
            for row in raw_results:
                for item in row:
                    clean_item = item.replace("::vertex", "")  # Remove "::vertex"
                    parsed_json = json.loads(clean_item)  # Convert string to dictionary
                    formatted_results.append(parsed_json)

            summary = QueryExecutionSummary(query=query)
            result = QueryExecutionResult(summary)

            print({"results": formatted_results})
            return result

        except Exception as e:
            self.conn.rollback()
            return {"error": str(e)}
