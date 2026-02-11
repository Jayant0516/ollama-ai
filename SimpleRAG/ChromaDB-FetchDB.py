# ChromaDB - Fetching data from persistent storage
# Collection means a table in DB where we store related data. Here we are fetching all the records from "pdf_docs" collection.
import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("pdf_docs")

data = collection.get()
print(data)
