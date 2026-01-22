# MCP MySQL Server

A Model Context Protocol (MCP) server that provides secure access to MySQL databases. This server exposes MySQL database operations as MCP tools, allowing AI assistants and other MCP clients to interact with your database safely.

## Features

- **Secure Query Execution**: Only SELECT queries are permitted for read-only database access
- **Database Schema Inspection**: List tables and view table schemas
- **Token Authentication**: Built-in token-based authentication middleware
- **Docker Support**: Includes Docker Compose setup for easy MySQL deployment
- **FastMCP Framework**: Built on FastMCP for efficient MCP server implementation

## Available Tools

The server exposes three MCP tools:

1. **list_tables()**: Lists all tables in the configured database
2. **get_table_schema(table_name)**: Returns the CREATE TABLE statement for a specific table
3. **run_query(query)**: Executes SELECT queries against the database (limited to 100 results)

## Prerequisites

- Python 3.8+
- MySQL 8.0+ (or use the included Docker Compose setup)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-mysql
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The server is configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_HOST` | MySQL server hostname | `localhost` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | (empty) |
| `MYSQL_DATABASE` | Database name | (empty) |
| `AUTH_TOKEN` | Authentication token for API access | (none) |

## Quick Start with Docker

1. Start the MySQL database:
```bash
docker-compose up -d
```

This will:
- Start a MySQL 8.0 container
- Create a test database (`test_db`)
- Initialize with sample tables (users, products, orders)
- Expose MySQL on port 3306

2. Run the MCP server:
```bash
./run_server.sh
```

Or manually:
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=password
export MYSQL_DATABASE=test_db
export AUTH_TOKEN=secret-token
python server.py
```

The server will start on port 8000.

## Usage

### As an MCP Server

The server runs as an HTTP MCP server using Server-Sent Events (SSE) transport. Configure your MCP client to connect to:

```
http://localhost:8000/sse
```

Include the authentication token in the Authorization header:
```
Authorization: Bearer <your-auth-token>
```

### Example Database Operations

The included sample database has three tables:

- **users**: User information (id, username, email, created_at)
- **products**: Product catalog (id, name, price, stock)
- **orders**: Order records (id, user_id, total_amount, order_date)

Sample queries you can run:
```sql
SELECT * FROM users;
SELECT name, price FROM products WHERE stock > 20;
SELECT u.username, o.total_amount FROM orders o JOIN users u ON o.user_id = u.id;
```

## Security

- **Query Restrictions**: Only SELECT statements are allowed to prevent data modification
- **Token Authentication**: All MCP endpoints require Bearer token authentication
- **Connection Handling**: Database connections are properly managed and closed after each operation
- **Error Handling**: Detailed error messages without exposing sensitive information

## Development

### Project Structure

```
mcp-mysql/
├── server.py              # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── run_server.sh         # Server startup script
├── docker-compose.yml    # Docker configuration for MySQL
└── docker-init/
    └── init.sql          # Database initialization script
```

## Dependencies

- **fastmcp**: FastMCP framework for building MCP servers
- **mysql-connector-python**: Official MySQL driver for Python
- **uvicorn**: ASGI server for running the application
- **python-dotenv**: Environment variable management

## Troubleshooting

### Connection Issues

If you can't connect to MySQL:
- Verify Docker container is running: `docker-compose ps`
- Check MySQL logs: `docker-compose logs db`
- Ensure port 3306 is not already in use

### Authentication Errors

If you receive 401 Unauthorized:
- Verify AUTH_TOKEN is set correctly
- Include the token in the Authorization header: `Bearer <token>`
- Check that the token matches on both client and server

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]