from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.document_loader import load_documents  # Load policy documents

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

def create_chunks(documents):
    chunks = []

    for document in documents:

        text_chunks = splitter.split_text(document["text"])

        for chunk in text_chunks:
            chunks.append({
                "text": chunk,
                "metadata": document["metadata"]
            })

    return chunks

if __name__ == "__main__":

    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Documents/pages loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    print("\n" + "=" * 60)
    print("SAMPLE CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(chunks[:5], start=1):

        print(f"\n--- CHUNK {i} ---")
        print("SOURCE:", chunk["metadata"]["source"])
        print("PAGE:", chunk["metadata"]["page"])
        print("TEXT:")
        print(chunk["text"])