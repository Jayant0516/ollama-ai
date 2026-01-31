import requests
import json

url = "http://localhost:11434/api/generate"

payload = {
    "model": "gemma3:1b",
    "prompt": "Explain AI in simple words",
    "stream": False
}

response = requests.post(url, json=payload)

print(response.json()["response"])
