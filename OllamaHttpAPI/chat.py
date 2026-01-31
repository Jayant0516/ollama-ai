import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "gemma3:1b",          # MUST be chat-capable
    "messages": [
        {"role": "system", "content": "You are a helpful teacher"},
        {"role": "user", "content": "What is a lever?"}
    ],
    "stream": False             # 🔑 IMPORTANT
}

r = requests.post(url, json=payload)
#print(r.status_code)
#print(r.json())
print(r.json()["message"]["content"])
