import numpy as np
from typing import List, Dict
from src.indexing.embedder import encode_query
from src.indexing.normalizer import normalize_vectors


# -------------------------
# 🔹 Query Cleaning
# -------------------------
def clean_query(query: str) -> str:
    return query.strip().lower()


# -------------------------
# 🔹 Query Expansion
# -------------------------
def expand_query(query: str) -> List[str]:
    return list(set([
        query,
        f"{query} explanation",
        f"{query} meaning",
    ]))


# -------------------------
# 🔹 Encode Queries (FIXED)
# -------------------------
def encode_queries(queries: List[str]) -> np.ndarray:
    vectors = []

    for q in queries:
        vec = encode_query(q)          # ✅ CORRECT
        vec = normalize_vectors(vec)   # ✅ normalize
        vectors.append(vec[0])         # flatten

    return np.array(vectors)


# -------------------------
# 🔹 Dense Retrieval
# -------------------------
def dense_search(query_vectors, index, k=10):
    scores, indices = index.search(query_vectors, k)
    return scores, indices


# -------------------------
# 🔹 Merge Results
# -------------------------
def merge_results(scores, indices, chunks):
    score_map = {}

    for q_idx in range(len(indices)):
        for score, idx in zip(scores[q_idx], indices[q_idx]):
            if idx == -1:
                continue

            if idx not in score_map:
                score_map[idx] = float(score)
            else:
                score_map[idx] = max(score_map[idx], float(score))

    merged = [
        {"text": chunks[i]["text"], "score": score_map[i]}
        for i in score_map
    ]

    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged


# -------------------------
# 🔹 Dynamic Filtering
# -------------------------
def dynamic_filter(results: List[Dict], top_k=5):
    if not results:
        return []

    max_score = results[0]["score"]
    threshold = max(0.5 * max_score, 0.2)

    filtered = [r for r in results if r["score"] >= threshold]
    return filtered[:top_k]


# -------------------------
# 🔹 Main Retriever
# -------------------------
def retrieve(query: str, index, chunks, k=10) -> List[Dict]:
    print(f"\n🔍 Query: {query}")

    query = clean_query(query)
    queries = expand_query(query)

    query_vectors = encode_queries(queries)

    scores, indices = dense_search(query_vectors, index, k)

    merged_results = merge_results(scores, indices, chunks)

    final_results = dynamic_filter(merged_results)

    print("\n📊 Retrieval Debug:\n")
    for i, r in enumerate(final_results):
        print(f"[{i+1}] Score: {r['score']:.4f}")
        print(f"{r['text'][:200]}\n---")

    return final_results