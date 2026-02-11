# ChromaDB - PDF Ingestion Script
# This script reads PDF files from a specified folder, extracts text, generates embeddings using Ollama, and stores the data in a persistent ChromaDB collection.
# Make sure to have the "pdfs" folder with PDF files in the same directory as this script.
# Flow is PDF -> Text Extraction -> Text Chunking -> Embedding Generation -> Store in ChromaDB
import os
import ollama
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------------------------
# Persistent ChromaDB
# -------------------------
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("pdf_docs")

# -------------------------
# Text Splitter
# -------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Folder containing PDFs
PDF_FOLDER = "./pdfs"

doc_id = 1

for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):
        filepath = os.path.join(PDF_FOLDER, file)

        print(f"Processing: {file}")

        reader = PdfReader(filepath)
        full_text = ""

        for page in reader.pages:
            if page.extract_text():
                full_text += page.extract_text()

        # Split into chunks
        chunks = splitter.split_text(full_text)

        for chunk in chunks:

            # Create embedding using Ollama
            response = ollama.embed(
                model="nomic-embed-text:latest",
                input=chunk
            )

            embedding = response["embeddings"][0]

            # Store into ChromaDB
            collection.add(
                ids=[str(doc_id)],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": file}]
            )

            doc_id += 1

print("All PDFs stored successfully.")
