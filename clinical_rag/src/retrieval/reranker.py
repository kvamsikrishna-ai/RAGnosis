from sentence_transformers import CrossEncoder

# 🔥 Load once
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, chunks, top_k=3):
    if not chunks:
        return []

    # 🔹 Remove duplicates (IMPORTANT)
    seen = set()
    unique_chunks = []
    for c in chunks:
        text = c["text"]
        if text not in seen:
            seen.add(text)
            unique_chunks.append(c)

    # 🔹 Prepare pairs
    pairs = [(query, c["text"]) for c in unique_chunks]

    # 🔹 Predict scores
    scores = reranker_model.predict(pairs)

    # 🔹 Attach scores
    for i, c in enumerate(unique_chunks):
        c["rerank_score"] = float(scores[i])

    # 🔹 Sort (NO thresholding)
    ranked = sorted(
        unique_chunks,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # 🔹 Safe fallback (IMPORTANT)
    if not ranked:
        return chunks[:top_k]

    # 🔍 Debug
    print("\n🔁 Reranked Results:\n")
    for i, c in enumerate(ranked[:top_k]):
        print(f"[{i+1}] Rerank: {c['rerank_score']:.4f} | Retrieve: {c.get('score', 0):.4f}")
        print(c["text"][:200], "\n---")

    return ranked[:top_k]