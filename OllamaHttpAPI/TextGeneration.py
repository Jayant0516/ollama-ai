import requests
import json

url = "http://localhost:11434/api/generate"

payload = {
    "model": "gemma3:1b",
    "prompt": "Explain AI in simple words",
    "stream": True
}

with requests.post(url, json=payload, stream=True) as response:
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            print(data.get("response", ""), end="", flush=True)
