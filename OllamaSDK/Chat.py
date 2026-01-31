import ollama

response = ollama.chat(
    model="gemma3:1b",
    messages=[
        {"role": "system", "content": "You are a physics teacher"},
        {"role": "user", "content": "What is force?"},
        {"role": "user", "content": "Give one real-world example"}
    ]
)

print(response["message"]["content"])
