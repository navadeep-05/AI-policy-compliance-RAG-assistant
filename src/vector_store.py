import chromadb              # ChromaDB for vector storage

from src.document_loader import load_documents   # Load policy documents
from src.text_splitter import create_chunks   # Create text chunks
from src.embeddings import create_embeddings   # Create embeddings
CHROMA_PATH = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="policy_documents"
)

def store_chunks(chunks, embeddings):
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.upsert(
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

if __name__ == "__main__":

    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Documents/pages: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    print("\nCreating embeddings...")
    embeddings = create_embeddings(chunks)

    print("Storing in ChromaDB...")
    store_chunks(chunks, embeddings)

    print("\n✓ Data stored successfully!")
    print("Collection:", collection.name)
    print("Total vectors:", collection.count())