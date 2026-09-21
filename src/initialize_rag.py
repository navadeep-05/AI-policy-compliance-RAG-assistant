import chromadb

from src.document_loader import load_documents
from src.text_splitter import create_chunks
from src.embeddings import create_embeddings

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "policy_documents"


def initialize_vector_store():
    """Create the ChromaDB collection if it does not exist."""

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Check whether the collection already exists
    existing = [
        collection.name
        for collection in client.list_collections()
    ]

    if COLLECTION_NAME in existing:
        collection = client.get_collection(
            name=COLLECTION_NAME
        )

        print(
            f"ChromaDB ready: "
            f"{collection.count()} vectors"
        )

        return collection

    print("Creating ChromaDB policy vector database...")

    # Load policy PDF pages
    documents = load_documents()

    # Split policies into smaller retrieval chunks
    chunks = create_chunks(documents)

    # Generate embeddings for each chunk
    embeddings = create_embeddings(chunks)

    # Create the collection
    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    # Store documents and embeddings
    collection.upsert(
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings.tolist(),
        metadatas=[chunk["metadata"] for chunk in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(
        f"Vector database created: "
        f"{collection.count()} vectors"
    )

    return collection
