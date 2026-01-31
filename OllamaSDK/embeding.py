import ollama

embedding = ollama.embeddings(
    model='nomic-embed-text:latest',
    prompt='Ollama runs LLMs locally.'
)

vector = embedding['embedding']
print(len(vector))  # vector size
