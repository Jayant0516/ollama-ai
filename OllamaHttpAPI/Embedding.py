import requests

url = "http://localhost:11434/api/embeddings"

payload = {
    "model": "nomic-embed-text",
    "prompt": "My Name is Jayant"
}

response = requests.post(url, json=payload)

embedding = response.json()["embedding"]

print("Vector length:", len(embedding))
print("First 5 values:", embedding[:5])
