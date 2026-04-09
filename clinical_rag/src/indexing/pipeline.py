from src.ingestion.pipeline import ingestion_pipeline
from src.indexing.embedder import generate_embeddings
from src.indexing.normalizer import normalize_vectors
from src.indexing.faiss_index import build_faiss_index, save_metadata


def indexing_pipeline(data_path):
    print("📥 Loading & chunking data...")
    chunks = ingestion_pipeline(data_path)

    print("🧠 Generating embeddings...")
    embeddings = generate_embeddings(chunks)

    print("📏 Normalizing embeddings...")
    embeddings = normalize_vectors(embeddings)

    print("⚡ Building FAISS index...")
    index = build_faiss_index(embeddings)

    print("💾 Saving metadata...")
    save_metadata(chunks)

    print("✅ Indexing complete!")

    return index, chunks