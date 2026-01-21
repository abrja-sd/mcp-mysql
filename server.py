
import os
import sys
import mysql.connector
from mysql.connector import Error
from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn

# Configuration
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DATABASE", "")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Initialize FastMCP
mcp = FastMCP("mysql")

def get_connection():
    """Creates and returns a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        # For a production app, we might want to log this
        print(f"Error connecting to MySQL: {e}")
        return None
    return None

@mcp.tool()
def list_tables() -> str:
    """Lists all tables in the database."""
    conn = get_connection()
    if not conn:
        return "Failed to connect to database."
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        return "\n".join(tables) if tables else "No tables found."
    except Error as e:
        return f"Error: {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@mcp.tool()
def get_table_schema(table_name: str) -> str:
    """Returns the CREATE TABLE statement for a given table."""
    conn = get_connection()
    if not conn:
        return "Failed to connect."
    try:
        cursor = conn.cursor()
        # Verify table exists
        cursor.execute("SHOW TABLES")
        valid_tables = {row[0] for row in cursor.fetchall()}

        if table_name not in valid_tables:
            return f"Table '{table_name}' does not exist."

        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
        result = cursor.fetchone()
        if result:
            return result[1]
        return "Could not fetch schema."
    except Error as e:
        return f"Error: {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@mcp.tool()
def run_query(query: str) -> str:
    """Executes a SQL query. Only SELECT statements are permitted."""
    if not query.strip().upper().startswith("SELECT"):
         return "Error: Only SELECT queries are allowed."

    conn = get_connection()
    if not conn:
        return "Failed to connect."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return "No results."
        return str(rows[:100])
    except Error as e:
        return f"Error executing query: {e}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # We protect SSE/message endpoints
        # Note: endpoint might be /mcp, /sse, or /messages depending on config
        path = request.url.path
        if path.startswith("/sse") or path.startswith("/messages") or path.startswith("/mcp"):
             token = os.getenv("AUTH_TOKEN")
             if token:
                 auth = request.headers.get("Authorization")
                 if not auth or auth != f"Bearer {token}":
                     return JSONResponse({"error": "Unauthorized"}, status_code=401)
        response = await call_next(request)
        return response

if __name__ == "__main__":
    if not AUTH_TOKEN:
        print("WARNING: AUTH_TOKEN not set. Server is unprotected.")

    # Manually run with uvicorn to ensure middleware is applied to the serving app
    try:
        # Access the underlying ASGI app call method
        app = mcp.http_app()

        # Initialize handlers to populate routes (crucial step for fastmcp)
        if hasattr(mcp, "_setup_handlers"):
            print("Initializing FastMCP handlers...")
            mcp._setup_handlers()

        # Add middleware to THIS app instance
        app.add_middleware(TokenAuthMiddleware)

        print(f"Starting server via uvicorn with Auth Token protection on port 8000...")
        uvicorn.run(app, host="0.0.0.0", port=8000)

    except Exception as e:
        print(f"Error starting uvicorn: {e}")
        # Fallback
        mcp.run(transport='sse')
