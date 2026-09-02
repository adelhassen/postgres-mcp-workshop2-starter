from typing import Any

import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="PostgreSQL Query API")


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
}


class QueryRequest(BaseModel):
    sql: str


@app.post("/query")
def execute_query(request: QueryRequest) -> dict[str, Any]:
    """Execute a SQL query against PostgreSQL and return the results."""

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(request.sql)

            # Get column names
            columns = [desc[0] for desc in cur.description]

            # Convert rows to dictionaries
            rows = [
                dict(zip(columns, row))
                for row in cur.fetchall()
            ]

    return {"data": rows}