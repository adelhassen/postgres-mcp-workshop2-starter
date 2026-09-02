from typing import List, Dict
import os
import psycopg2
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initializes your MCP server instance. It's used to register your tools.
mcp = FastMCP("postgres-server")

# Database connection configuration from environment variables
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "practice_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password123"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

@mcp.tool()
async def execute_sql(query: str) -> List[Dict]:
    """
    Execute a SQL query and return the results as a list of dictionaries.
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, r)) for r in cur.fetchall()]
    return rows

@mcp.tool()
async def get_schema(table: str) -> List[Dict]:
    """Return column names and types for a given table."""
    sql = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (table,))
            rows = [{"column": r[0], "type": r[1]} for r in cur.fetchall()]
    return rows

def main():
    # Run MCP server using stdio transport for AI assistant integration
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
