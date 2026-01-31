import requests

url = "http://localhost:11434/api/embeddings"

payload = {
    "model": "nomic-embed-text",
    "prompt": "Artificial intelligence is the future"
}

response = requests.post(url, json=payload)

embedding = response.json()["embedding"]

print("Vector length:", len(embedding))
print("First 5 values:", embedding[:5])
