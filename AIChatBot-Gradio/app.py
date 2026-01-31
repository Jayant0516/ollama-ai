import gradio as gr
import ollama

MODEL_NAME = "gemma3:1b"   # Change to mistral, gemma, phi3, etc.

def chat_with_ai(message, history):
    # Convert Gradio history into Ollama message format
    messages = []

    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})

    messages.append({"role": "user", "content": message})

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response["message"]["content"]

demo = gr.ChatInterface(
    fn=chat_with_ai,
    title="🦙 Local AI Chatbot (Ollama Python SDK)",
    description="Runs completely on your machine using Ollama"
)

demo.launch()
