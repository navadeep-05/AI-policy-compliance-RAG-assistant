from sentence_transformers import SentenceTransformer  # Embedding model
from src.text_splitter import create_chunks  # Create text chunks
from src.document_loader import load_documents  # Load policy documents

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def create_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings

if __name__ == "__main__":

    documents = load_documents()
    chunks = create_chunks(documents)
    embeddings = create_embeddings(chunks)

    print("\nDocuments:", len(documents))
    print("Chunks:", len(chunks))
    print("Embeddings shape:", embeddings.shape)

    print("\nFirst embedding:")
    print(embeddings[0])