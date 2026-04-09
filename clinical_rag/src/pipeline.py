import os
import time

from src.indexing.pipeline import indexing_pipeline
from src.indexing.faiss_index import load_index, load_metadata
from src.retrieval.retriever import retrieve
from src.retrieval.reranker import rerank
from src.retrieval.context_builder import build_context
from src.generation.generator import generate_answer


# -------------------------
# 🔹 PATH SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(BASE_DIR, "chunks.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "raw")


# -------------------------
# 🔹 GLOBAL CACHE
# -------------------------
index = None
chunks = None


# -------------------------
# 🔹 DOMAIN DETECTION
# -------------------------
def detect_domain(query):
    q = query.lower()

    if any(x in q for x in ["heart", "cardiac", "echo", "echocardiography"]):
        return "cardiac"

    if any(x in q for x in ["pregnancy", "preeclampsia", "hypertension"]):
        return "obg"

    return "general"


# -------------------------
# 🔹 QUERY REWRITE
# -------------------------
def rewrite_query(query):
    domain = detect_domain(query)

    if domain == "cardiac":
        return query + " related to heart disease in pregnancy"

    if domain == "obg":
        return query + " in obstetrics pregnancy context"

    return query


# -------------------------
# 🔹 MULTI-QUERY GENERATION
# -------------------------
def generate_queries(query):
    return list(set([
        query,
        rewrite_query(query),
        f"{query} causes",
        f"{query} explanation"
    ]))


# -------------------------
# 🔹 MERGE RESULTS
# -------------------------
def merge_results(results):
    seen = {}

    for r in results:
        text = r["text"]

        if text not in seen or r["score"] > seen[text]:
            seen[text] = r["score"]

    merged = [{"text": k, "score": v} for k, v in seen.items()]
    merged.sort(key=lambda x: x["score"], reverse=True)

    return merged


# -------------------------
# 🔹 INITIALIZE INDEX
# -------------------------
def initialize_index(data_path=DATA_PATH):
    global index, chunks

    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        print("⚡ Loading existing index...")
        index = load_index(INDEX_PATH)
        chunks = load_metadata(CHUNKS_PATH)
    else:
        print("⚠️ Index not found. Building new index...")
        index, chunks = indexing_pipeline(data_path)


# -------------------------
# 🔹 MAIN RAG PIPELINE
# -------------------------
def rag_pipeline(query):
    global index, chunks

    start_time = time.time()

    # 🔥 Ensure index loaded
    if index is None or chunks is None:
        initialize_index()

    # -------------------------
    # MULTI-QUERY RETRIEVAL
    # -------------------------
    queries = generate_queries(query)

    all_results = []

    for q in queries:
        results = retrieve(q, index, chunks, k=6)
        all_results.extend(results)

    # -------------------------
    # MERGE + TOP-K
    # -------------------------
    retrieved = merge_results(all_results)[:12]

    # -------------------------
    # RERANK
    # -------------------------
    reranked = rerank(query, retrieved, top_k=8)

    # 🔥 FILTER (balanced threshold)
    reranked = [c for c in reranked if c.get("rerank_score", 0) > 0.3]

    # 🔥 FALLBACK (important)
    if not reranked:
        print("⚠️ Reranker removed all → fallback to retriever")
        reranked = retrieved[:3]

    # -------------------------
    # CONTEXT BUILD
    # -------------------------
    context = build_context(reranked)

    # -------------------------
    # GENERATE ANSWER
    # -------------------------
    answer = generate_answer(query, context)

    end_time = time.time()
    print(f"\n⏱️ Total RAG Time: {end_time - start_time:.2f}s")

    return answer