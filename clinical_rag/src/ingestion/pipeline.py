from src.ingestion.loader import load_pdfs
from src.ingestion.cleaner import clean_text
from src.ingestion.chunker import chunk_text


def ingestion_pipeline(data_path):
    docs = load_pdfs(data_path)

    all_chunks = []

    for doc in docs:
        clean = clean_text(doc["content"])

        chunks = chunk_text(clean)

        for i, chunk in enumerate(chunks):
            if len(chunk.split()) < 20:
                continue  # remove useless tiny chunks

            all_chunks.append({
                "text": chunk,
                "source": doc["file_name"],
                "chunk_id": f"{doc['file_name']}_{i}"
            })

    print(f"✅ Total chunks created: {len(all_chunks)}")

    return all_chunks