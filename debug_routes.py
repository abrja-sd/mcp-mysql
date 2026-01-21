from fastmcp import FastMCP
mcp = FastMCP("demo")
app = mcp.http_app()
print(f"Routes before: {getattr(app, 'routes', 'No routes')}")
try:
    # fastmcp might need settings or manual setup call
    # Try calling _setup_handlers if it exists
    if hasattr(mcp, "_setup_handlers"):
        mcp._setup_handlers()

    # Or maybe we need to enable SSE in settings?
    if hasattr(mcp, "settings"):
        print(f"Settings: {mcp.settings}")
        # mcp.settings.transport = 'sse'?

    print("Called setup handlers.")
except Exception as e:
    print(f"Error calling setup: {e}")

# Routes might be separate from app if handlers attach to it?
print(f"Routes after: {getattr(app, 'routes', 'No routes')}")
if hasattr(app, 'routes'):
    for r in app.routes:
        print(f"Route: {r.path} {r.name}")
