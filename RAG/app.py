import os
import uuid
import ollama
import chromadb
from flask import Flask, request, render_template, jsonify
from pypdf import PdfReader

# ------------------ CONFIG ------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Chroma DB setup (persistent)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="documents")

# ------------------ HELPERS ------------------

def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]


def ask_llm(question, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "Not found in document."

Context:
{context}

Question: {question}
Answer:
"""

    response = ollama.generate(
        model="gemma3:1b",
        prompt=prompt
    )

    return response["response"]

# ------------------ ROUTES ------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    text = extract_pdf_text(filepath)
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = get_embedding(chunk)
        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": file.filename}]
        )

    return jsonify({
        "status": "Document processed",
        "chunks_added": len(chunks)
    })


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context_chunks = results["documents"][0]

    answer = ask_llm(question, context_chunks)

    return jsonify({
        "answer": answer,
        "sources": results["metadatas"][0]
    })


# ------------------ MAIN ------------------

if __name__ == "__main__":
    app.run(debug=True)
