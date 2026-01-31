from mcp.server.fastmcp import FastMCP
import ollama

# Initialize FastMCP server
mcp = FastMCP("ollama-server")

@mcp.tool()
def query_ollama(model: str, prompt: str) -> str:
    """
    Query a local Ollama model with a prompt.

    Args:
        model: The name of the model to use (e.g., "llama3").
        prompt: The prompt to send to the model.
    """
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error querying Ollama: {str(e)}"

if __name__ == "__main__":
    mcp.run()
