from src.indexing.faiss_index import load_index, load_metadata
from src.retrieval.retriever import retrieve

# 🔥 load saved index + chunks
index = load_index("clinical_rag/index.faiss")
chunks = load_metadata("clinical_rag/chunks.pkl")

# 🔥 test query
query = "causes of preeclampsia"

results = retrieve(query, index, chunks)

print("\n✅ Final Results:\n")
for i, r in enumerate(results):
    print(f"{i+1}. {r['text'][:200]}")