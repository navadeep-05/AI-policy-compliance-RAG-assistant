from src.document_loader import load_documents  # Load text from policy PDFs
from src.text_splitter import create_chunks  # Split text into chunks
from src.embeddings import create_embeddings  # Convert chunks into vectors
from src.vector_store import store_chunks  # Store vectors in ChromaDB


def ingest_policies():
    # Step 1: Load policy pages from PDFs
    documents = load_documents()
    print(f"Loaded pages: {len(documents)}")

    # Step 2: Split pages into smaller searchable chunks
    chunks = create_chunks(documents)
    print(f"Created chunks: {len(chunks)}")

    # Step 3: Convert chunks into embeddings
    print("\nCreating embeddings...")
    embeddings = create_embeddings(chunks)

    # Step 4: Store chunks, embeddings, and metadata in ChromaDB
    print("\nStoring in ChromaDB...")
    store_chunks(chunks, embeddings)

    print("\n✓ Policy ingestion completed successfully!")


if __name__ == "__main__":
    # Run the complete ingestion pipeline
    ingest_policies()