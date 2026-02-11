from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Math + Time Tools")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(x: int, y: int) -> int:
    return x * y

@mcp.tool()
def get_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    mcp.run()
