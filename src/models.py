from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    question: str

class Drawback(BaseModel):
    id: int
    category: str
    title: str
    text: str
    severity: str
    evidence: str

class RetrievedDocument(BaseModel):
    title: str
    category: str
    text: str
    severity: str
    evidence: str
    similarity_score: float

class AIResponse(BaseModel):
    question: str
    answer: str
    sources: List[RetrievedDocument]
