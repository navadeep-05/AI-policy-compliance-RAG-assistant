import chromadb   # ChromaDB for vector search
from functools import lru_cache
from sentence_transformers import SentenceTransformer  # Create query embeddings
from src.reranker import rerank_documents  # Rerank retrieved policy chunks

CHROMA_PATH = "chroma_db"  # Location of our newly created vector database (chromadb)
MODEL_NAME = "all-MiniLM-L6-v2"  # Same model used during indexing


# Reuse the embedding model instead of loading it repeatedly
@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)


# Connect to our existing persistent vector database
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create/load the vector database automatically
collection = initialize_vector_store()


def retrieve_documents(query, top_k=5):
    """Retrieve the most semantically similar policy chunks."""

    model = get_embedding_model()
    # Convert the user's question into a vector
    query_embedding = model.encode([query])

    # Search ChromaDB using the user's question embedding
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )
    return results

def retrieve_and_rerank(query, retrieve_k=5, rerank_k=3):
    # First retrieve candidate policy chunks
    results = retrieve_documents(query, top_k=retrieve_k)

    # Get retrieved text and metadata
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Rerank the retrieved chunks by exact relevance
    ranked_documents = rerank_documents(
        query,
        documents,
        metadatas,
        top_k=rerank_k
    )
    return ranked_documents

if __name__ == "__main__":

    # Example employee question
    query = "Can I work remotely for 20 days?"

    # Retrieve 5 candidates and keep the best 3
    results = retrieve_and_rerank(
        query,
        retrieve_k=5,
        rerank_k=3
    )

    print("\nQuery:", query)
    print("\nFinal Ranked Policy Evidence:\n")

    # Display final results with evidence information
    for rank, result in enumerate(results, start=1):

        print("=" * 60)
        print(f"RANK {rank}")
        print("=" * 60)

        print("Score:", result["score"])
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("\nText:")
        print(result["text"])
