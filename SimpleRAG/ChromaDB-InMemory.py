import ollama
import chromadb

# Create In Memory ChromaDB client
client = chromadb.Client()
# Create collection (like a table in DB)
collection = client.create_collection(name="user_inputs")

# User input
text = "AI Agents can use MCP tools"

# Generate embedding using Ollama
response = ollama.embed(
    model="nomic-embed-text:latest",
    input=text
)

embedding = response["embeddings"]

# Store into ChromaDB
collection.add(
    ids=["1"],
    embeddings=embedding,
    documents=[text]
)

print("Stored successfully")
