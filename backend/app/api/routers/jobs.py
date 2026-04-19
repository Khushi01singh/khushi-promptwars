from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.rag import vector_store

router = APIRouter()

@router.get("/")
async def list_jobs() -> List[Dict[str, Any]]:
    """Returns all jobs currently in the mock vector store."""
    return vector_store.jobs_db

@router.get("/search")
async def search_jobs(query: str) -> List[Dict[str, Any]]:
    """Simulates a RAG vector search across job descriptions."""
    return vector_store.search_similar_jobs(query)
