from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# PostgreSQL Connection
DB_HOST = os.getenv("DB_HOST", "postgres-age-container")
conn = psycopg2.connect(
    dbname="postgresDB",
    user="postgres",
    password="yourpassword",
    host=DB_HOST,
    port="5432"
)

class CypherQuery(BaseModel):
    query: str

import json

@app.post("/cypher")
def execute_cypher(request: CypherQuery):
    try:
        cursor = conn.cursor()

        # Load AGE and set search_path
        cursor.execute("LOAD 'age';")
        cursor.execute("SET search_path TO ag_catalog, \"$user\", public;")

        cypher_query = request.query
        translated_query = f"SELECT * FROM ag_catalog.cypher('my_graph', $$ {cypher_query} $$) AS (result agtype);"

        cursor.execute(translated_query)
        raw_results = cursor.fetchall()
        conn.commit()
        cursor.close()

        # Clean up the results (remove "::vertex" and parse JSON)
        formatted_results = []
        for row in raw_results:
            for item in row:
                clean_item = item.replace("::vertex", "")  # Remove "::vertex"
                parsed_json = json.loads(clean_item)  # Convert string to dictionary
                formatted_results.append(parsed_json)

        return {"results": formatted_results}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


