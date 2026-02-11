from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Remote Weather Tool")

@mcp.tool()
def get_weather(city: str) -> str:
    """Returns the weather for a given city."""
    return f"The weather in {city} is sunny, 22°C."

if __name__ == "__main__":
    # Switch to SSE transport and specify a port
    mcp.run(transport="http")
    