from sentence_transformers import SentenceTransformer

# 🔥 Single source of truth
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

PREFIX = "Represent this sentence for retrieval: "


def generate_embeddings(chunks):
    texts = [PREFIX + chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=False
    )

    return embeddings


def encode_query(query: str):
    query = PREFIX + query

    embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=False
    )

    return embedding