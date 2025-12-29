from app.vector_store import get_vector_components
import gc

def semantic_search(query: str, top_k: int = 2):  # Reduced from 3 to 2
    """Lightweight semantic search with minimal memory usage"""
    try:
        model, collection = get_vector_components()

        # Truncate long queries to save processing
        if len(query) > 200:
            query = query[:200]

        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        hits = []
        for doc, meta in zip(documents, metadatas):
            hits.append({
                "text": doc,
                "metadata": meta
            })

        # Minimal debug output
        if not hits:
            print("⚠️ No results")
        else:
            print(f"✓ Retrieved {len(hits)} docs")

        # Clean up
        gc.collect()
        
        return hits
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []
