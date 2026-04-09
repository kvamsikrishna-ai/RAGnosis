def build_context(chunks, max_chars=2000):
    """
    Builds structured, prioritized context for generator
    """

    if not chunks:
        return ""

    context_parts = []
    total_length = 0

    # 🔥 sort by rerank score (safety)
    chunks = sorted(
        chunks,
        key=lambda x: x.get("rerank_score", x.get("score", 0)),
        reverse=True
    )

    for i, chunk in enumerate(chunks):
        text = chunk["text"].strip()

        # 🔥 compress long chunks
        if len(text) > 300:
            text = text[:300] + "..."

        # 🔥 include score for signal (optional but powerful)
        score = chunk.get("rerank_score", chunk.get("score", 0))

        formatted_chunk = (
            f"[Source {i+1} | Score: {score:.2f}]\n"
            f"{text}\n"
        )

        # 🔥 strict length control
        if total_length + len(formatted_chunk) > max_chars:
            break

        context_parts.append(formatted_chunk)
        total_length += len(formatted_chunk)

    return "\n".join(context_parts)