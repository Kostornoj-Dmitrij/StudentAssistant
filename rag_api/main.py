from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from services.vector_store import VectorStore
from services.llm_client import LLMClient
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG API", version="1.0.0")

vector_store = VectorStore()
llm_client = LLMClient()


class QuestionRequest(BaseModel):
    question: str
    user_id: int


class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    logger.info("Initializing RAG API...")
    await vector_store.initialize()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        relevant_docs = await vector_store.search(request.question, top_k=3)

        answer = await llm_client.generate_answer(
            question=request.question,
            context=relevant_docs
        )

        sources = [doc.get('source', 'unknown') for doc in relevant_docs]

        return QuestionResponse(answer=answer, sources=sources)

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)