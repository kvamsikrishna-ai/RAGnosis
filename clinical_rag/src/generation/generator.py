import os
from google import genai
from transformers import pipeline

# ✅ Gemini client (NEW SDK)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ⚠️ Fallback model (weak but safe)
fallback_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    tokenizer="google/flan-t5-large"
)


# 🔥 CLEAN PROMPT (no overengineering)
def build_prompt(query, context):
    return f"""
You are a medical expert.

Answer using ONLY the context.

Rules:
- You may infer logical conclusions from the context
- Combine multiple statements to form the answer
- Do NOT require exact sentence match
- If completely unrelated, say: Not found in context

Context:
{context}

Question:
{query}

Answer:
"""


# ⚡ Fallback (only if Gemini fails)
def fallback_answer(prompt):
    print("⚡ Using fallback model...\n")

    result = fallback_model(
        prompt,
        max_length=256,
        do_sample=False,
        truncation=True
    )

    return result[0]["generated_text"].strip()


# 🚀 MAIN GENERATION FUNCTION
def generate_answer(query, context):
    prompt = build_prompt(query, context)

    # 🔍 DEBUG (MANDATORY)
    print("\n====== CONTEXT ======\n")
    print(context[:800])
    print("\n====================\n")

    print("🚀 Using Gemini model: gemini-2.5-flash\n")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # ✅ FIXED MODEL
            contents=prompt
        )

        # ✅ Safe extraction
        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

        print("⚠️ Empty response from Gemini")

    except Exception as e:
        print("⚠️ Gemini failed:", e)
        print("⏳ Switching to fallback...\n")

    return fallback_answer(prompt)