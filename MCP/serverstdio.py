from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Create MCP server
mcp = FastMCP("Sample Utility Tools")


# ------------------ TOOL 1: ADDITION ------------------
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b


# ------------------ TOOL 2: MULTIPLICATION ------------------
@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b


# ------------------ TOOL 3: TEXT SUMMARY ------------------
@mcp.tool()
def summarize_text(text: str) -> str:
    """Return a short summary of the given text."""
    if len(text) < 50:
        return text
    return text[:50] + "..."


# ------------------ TOOL 4: WORD COUNT ------------------
@mcp.tool()
def count_words(text: str) -> int:
    """Count the number of words in the given text."""
    return len(text.split())


# ------------------ TOOL 5: CURRENT TIME ------------------
@mcp.tool()
def get_current_time() -> str:
    """Get the current system time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ------------------ TOOL 6: REVERSE STRING ------------------
@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]


# Run the MCP server
if __name__ == "__main__":
    mcp.run()