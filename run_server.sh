#!/bin/bash
source venv/bin/activate
export MYSQL_HOST=${MYSQL_HOST:-localhost}
export MYSQL_USER=${MYSQL_USER:-root}
export MYSQL_PASSWORD=${MYSQL_PASSWORD:-password}
export MYSQL_DATABASE=${MYSQL_DATABASE:-test_db}
export AUTH_TOKEN=${AUTH_TOKEN:-secret-token}

# fastmcp run usually defaults to stdio
# To run HTTP, we might need to specify it.
# fastmcp CLI: fastmcp run server.py --transport sse --port 8000
# venv/bin/fastmcp run server.py --transport sse --port 8000
# Try running directly to ensure middleware is respected
venv/bin/python server.py --transport sse --port 8000
