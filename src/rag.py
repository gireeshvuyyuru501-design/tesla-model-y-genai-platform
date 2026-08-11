import json
import os
from pathlib import Path

import faiss
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "drawbacks.json"

with open(DATA_FILE, "r", encoding="utf-8-sig") as file:
    DRAWBACKS = json.load(file)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

DOCUMENT_TEXTS = []

for item in DRAWBACKS:
    DOCUMENT_TEXTS.append(
        f"""
Title: {item['title']}
Category: {item['category']}
Severity: {item['severity']}
Evidence: {item['evidence']}
Description: {item['text']}
"""
    )


document_embeddings = embedding_model.encode(
    DOCUMENT_TEXTS,
    convert_to_numpy=True
).astype("float32")

faiss.normalize_L2(document_embeddings)

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(document_embeddings)


def retrieve_documents(question: str, top_k: int = 4):

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indexes = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indexes[0]):

        if idx == -1:
            continue

        item = DRAWBACKS[idx].copy()

        item["similarity_score"] = float(score)

        results.append(item)

    return results


def build_context(results):

    blocks = []

    for number, item in enumerate(results, start=1):

        blocks.append(
            f"""
SOURCE {number}

Title: {item['title']}
Category: {item['category']}
Severity: {item['severity']}
Evidence: {item['evidence']}

Information:
{item['text']}
"""
        )

    return "\n".join(blocks)


def generate_answer(question: str):

    retrieved = retrieve_documents(question)

    context = build_context(retrieved)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "YOUR_REAL_OPENAI_API_KEY":

        return {
            "question": question,
            "answer": "Semantic retrieval is working, but OpenAI API key is not configured.",
            "sources": retrieved,
            "mode": "retrieval-only"
        }

    client = OpenAI(api_key=api_key)

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-4.1-mini"
    )

    system_prompt = """
You are a grounded automotive research assistant.

Use only the retrieved context.

Rules:
- Do not invent facts.
- Distinguish official information from reviews.
- Treat owner reports as anecdotal.
- State when evidence is insufficient.
- Keep the answer concise and factual.
"""

    user_prompt = f"""
QUESTION:

{question}

RETRIEVED CONTEXT:

{context}

Answer using only the retrieved context.
"""

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_prompt
    )

    return {
        "question": question,
        "answer": response.output_text,
        "sources": retrieved,
        "mode": "rag"
    }