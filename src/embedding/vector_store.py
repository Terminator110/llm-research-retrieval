from pathlib import Path

from embedder import main
import chromadb

CURRENT_DIR = Path(__file__).resolve().parent

client = chromadb.PersistentClient(path=CURRENT_DIR.parent.parent / "storage/chroma")

table = client.get_or_create_collection("ai_research_papers")
    

chunks = main()
print(f"Loaded {len(chunks)} chunks")

table.upsert(
    ids=[chunk["id"] for chunk in chunks],
    documents=[chunk["text"] for chunk in chunks],
    embeddings=[chunk["embedding"] for chunk in chunks],
    metadatas=[chunk["metadata"] for chunk in chunks],
)


print(f"Stored {len(chunks)} chunks in ChromaDB")
print(table.get(limit=5))