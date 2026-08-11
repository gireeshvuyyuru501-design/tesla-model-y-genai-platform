# Tesla Model Y 2026 Premium — GenAI Course Project
Portfolio project: build a grounded RAG + agentic AI assistant that analyzes drawbacks and owner/reviewer feedback.

## Run (Windows)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload

Open http://127.0.0.1:8000/docs

## Curriculum
See COURSE.md. Start with keyword retrieval, then embeddings, RAG, vector DB, LLMs, Pydantic, FastAPI, evaluation, guardrails, LangGraph agents and deployment.
