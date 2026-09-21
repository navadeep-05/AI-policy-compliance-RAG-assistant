from pathlib import Path
import pymupdf

POLICY_DIR = Path("data/acme_policy_documents/policies")

def load_documents():
    documents = []

    for pdf_path in POLICY_DIR.glob("*.pdf"):

        doc = pymupdf.open(pdf_path)

        for page_number, page in enumerate(doc, start=1):

            text = page.get_text().strip()

            if text:
                documents.append({
                    "text": text,
                    "metadata": {
                        "source": pdf_path.name,
                        "page": page_number
                    }
                })

        doc.close()

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(f"Loaded {len(documents)} pages\n")

    for document in documents[:3]:

        print("=" * 60)
        print("SOURCE:", document["metadata"]["source"])
        print("PAGE:", document["metadata"]["page"])
        print("=" * 60)
        print(document["text"][:500])
        print()