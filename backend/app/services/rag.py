from typing import List, Dict, Any

class MockVectorStore:
    """
    A mock vector store to simulate RAG retrieval.
    Structured to allow swapping with Pinecone or another Vector DB later.
    """
    def __init__(self):
        # Mock database of job descriptions
        self.jobs_db = [
            {
                "id": "job_1",
                "title": "Senior React Developer",
                "description": "Looking for an experienced React developer with 5+ years of experience. Must know Redux, Vite, and Tailwind CSS. Bonus for Next.js.",
                "skills": ["React", "JavaScript", "Redux", "Vite", "Tailwind CSS"]
            },
            {
                "id": "job_2",
                "title": "Python Backend Engineer",
                "description": "Seeking a backend engineer skilled in FastAPI and PostgreSQL. Experience with Docker and AWS is required. Knowledge of LangChain is a plus.",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "LangChain"]
            }
        ]

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Mock method for adding documents to the index."""
        # Pinecone implementation would go here: 
        # pinecone.Index('jobs').upsert(vectors=...)
        self.jobs_db.extend(documents)
    
    def search_similar_jobs(self, query_text: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Mock semantic search. 
        In reality, this would convert query_text to embeddings and search Pinecone.
        """
        # Pinecone implementation would go here: 
        # embedding = get_embedding(query_text)
        # results = pinecone.Index('jobs').query(vector=embedding, top_k=top_k, include_metadata=True)
        # return results.matches
        
        # Mock logic: return a job that has matching keywords, or just the first one
        query_lower = query_text.lower()
        for job in self.jobs_db:
            if any(skill.lower() in query_lower for skill in job['skills']):
                return [job]
        
        return [self.jobs_db[0]] if self.jobs_db else []

# Global instance for mock use
vector_store = MockVectorStore()
