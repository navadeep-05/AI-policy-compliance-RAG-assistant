from functools import lru_cache  # tool for reducing model load time
from sentence_transformers import CrossEncoder  # Import reranking model

# Cross-encoder compares the query with each policy chunk
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Load the reranker only once and reuse it
@lru_cache(maxsize=1)
def get_reranker():
    return CrossEncoder(MODEL_NAME)


def rerank_documents(query, documents, metadatas, top_k=3):
    reranker = get_reranker()

    # Create query-document pairs for relevance scoring
    pairs = [[query, document] for document in documents]

    # Calculate a relevance score for each pair
    scores = reranker.predict(pairs)

    # Keep text, score, and metadata together
    ranked = []

    for document, score, metadata in zip(documents, scores, metadatas):
        ranked.append({
            "text": document,
            "score": float(score),
            "source": metadata["source"],
            "page": metadata["page"]
        })

    # Sort from most relevant to least relevant
    ranked.sort(key=lambda x: x["score"], reverse=True)

    # Return only the best results
    return ranked[:top_k]