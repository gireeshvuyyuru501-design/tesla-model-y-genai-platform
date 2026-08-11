from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.agents import run_agent

from src.models import QuestionRequest
from src.rag import (
    DRAWBACKS,
    retrieve_documents,
    generate_answer,
)


app = FastAPI(
    title="Tesla Model Y 2026 Premium GenAI Platform",
    description="""
GenAI + RAG application for analyzing
2026 Tesla Model Y Premium drawbacks.

Features:
- Tesla drawback dataset
- Embeddings
- Semantic search
- Retrieval-Augmented Generation
- Evidence classification
- OpenAI integration
- FastAPI REST API
""",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Tesla Model Y 2026 Premium GenAI API",
        "swagger": "/docs",
        "health": "/health",
        "drawbacks": "/drawbacks",
        "search": "/search",
        "ask": "/ask",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "Tesla Model Y GenAI Platform",
        "documents": len(DRAWBACKS),
    }


@app.get("/drawbacks")
def drawbacks():
    return DRAWBACKS


@app.post("/search")
def semantic_search(request: QuestionRequest):

    documents = retrieve_documents(
        request.question
    )

    return {
        "question": request.question,
        "retrieved_documents": documents,
    }


@app.post("/ask")
def ask_tesla_assistant(request: QuestionRequest):

    return generate_answer(
        request.question
    )
@app.post("/agent")
def agent_analysis(request: QuestionRequest):

    return run_agent(
        request.question
    )