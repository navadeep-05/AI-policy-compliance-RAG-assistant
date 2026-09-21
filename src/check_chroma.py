import chromadb  # Import ChromaDB


# Connect to the exact database used by our project
client = chromadb.PersistentClient(path="chroma_db")

# Show all collections stored in this database
collections = client.list_collections()

print("\nCollections found:")

if not collections:
    print("No collections found.")

else:
    for collection in collections:
        print(
            f"- {collection.name} | "
            f"Documents: {collection.count()}"
        )