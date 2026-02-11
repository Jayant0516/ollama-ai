import ollama
import chromadb

# Create persistent ChromaDB (data saved in folder)
client = chromadb.PersistentClient(path="chroma_db")

collection = client.create_collection(name="user_inputs")

# User input
text = "What is AI Agents can use MCP tools"

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

print("Stored successfully on disk")
