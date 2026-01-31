import ollama

response = ollama.generate(
    model="gemma3:1b",
    prompt="Explain Newton's first law of motion"
)

print(response["response"])
