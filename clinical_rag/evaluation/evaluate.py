import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline import rag_pipeline
from src.retrieval.retriever import retrieve
from src.indexing.faiss_index import load_index, load_metadata


# 🔥 Load once
index = load_index("clinical_rag/index.faiss")
chunks = load_metadata("clinical_rag/chunks.pkl")


# ✅ MINIMAL HIGH-SIGNAL TESTS
test_cases = [
    {
        "query": "Why does systemic vascular resistance decrease?",
        "expected_keywords": ["vasodilation", "resistance"]
    },
    {
        "query": "Types of hypertensive disorders in pregnancy",
        "expected_keywords": ["preeclampsia", "gestational", "chronic"]
    }
]


# ✅ Answer scoring
def keyword_match(answer, expected_keywords):
    answer = answer.lower()
    matches = sum(1 for kw in expected_keywords if kw in answer)
    return matches / len(expected_keywords)


# ✅ Retrieval recall (STRICT)
def retrieval_recall(query, expected_keywords):
    results = retrieve(query, index, chunks, k=5)  # 🔥 FIXED

    combined_text = " ".join([r["text"].lower() for r in results])

    matches = sum(1 for kw in expected_keywords if kw in combined_text)
    return matches / len(expected_keywords)


def evaluate():
    total_answer = 0
    total_retrieval = 0
    total_latency = 0

    print("\n🚀 Running Evaluation...\n")

    for case in test_cases:
        query = case["query"]
        expected = case["expected_keywords"]

        start = time.time()

        answer = rag_pipeline(query)

        latency = time.time() - start

        ans_score = keyword_match(answer, expected)
        ret_score = retrieval_recall(query, expected)

        total_answer += ans_score
        total_retrieval += ret_score
        total_latency += latency

        print("\n-----------------------------")
        print("Q:", query)
        print("Answer:", answer[:200], "...")
        print(f"Answer Score: {ans_score:.2f}")
        print(f"Retrieval Score: {ret_score:.2f}")
        print(f"Latency: {latency:.2f}s")

        time.sleep(2)

    n = len(test_cases)

    print("\n📊 FINAL METRICS")
    print(f"Answer Accuracy: {(total_answer/n)*100:.2f}%")
    print(f"Retrieval Recall: {(total_retrieval/n)*100:.2f}%")
    print(f"Avg Latency: {(total_latency/n):.2f}s")


if __name__ == "__main__":
    evaluate()