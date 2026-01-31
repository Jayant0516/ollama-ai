# AI Chatbot using Flask and Ollama API
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma3:1b"  # MUST be chat-capable

# Store conversation history
chat_history = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]


@app.route("/")
def home():
    return render_template("index.htm")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Add user message to history
    chat_history.append({"role": "user", "content": user_message})

    payload = {
        "model": MODEL_NAME,
        "messages": chat_history,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()

    bot_reply = result["message"]["content"]

    # Add assistant reply to history
    chat_history.append({"role": "assistant", "content": bot_reply})

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
