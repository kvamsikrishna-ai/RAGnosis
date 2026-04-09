import faiss
import pickle


def build_faiss_index(embeddings, save_path="clinical_rag/index.faiss"):
    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)  # cosine (after normalization)
    index.add(embeddings)

    faiss.write_index(index, save_path)
    return index


def save_metadata(chunks, path="clinical_rag/chunks.pkl"):
    with open(path, "wb") as f:
        pickle.dump(chunks, f)


def load_index(path="clinical_rag/index.faiss"):
    return faiss.read_index(path)


def load_metadata(path="clinical_rag/chunks.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)