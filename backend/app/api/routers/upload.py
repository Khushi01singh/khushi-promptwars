from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.pii_stripper import ResumeProcessor
from app.services.rag import vector_store
from app.services.matcher import matcher_service

router = APIRouter()

@router.post("/process-resume")
async def process_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...) 
):
    """
    Endpoint to upload a candidate resume and a job description.
    1. Extracts text and strips PII.
    2. Runs the LLM Agent (LangGraph) to score the match.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        # Read file bytes
        contents = await file.read()
        
        # Step 1: Extract text and sanitize PII
        sanitized_text = ResumeProcessor.process_pdf(contents)
        
        # Step 2: Evaluate candidate using the core matching logic (LangGraph)
        match_result = matcher_service.evaluate(
            sanitized_resume_text=sanitized_text,
            job_description=job_description
        )
        
        return {
            "status": "success",
            "candidate_data": {
                "sanitized_text_preview": sanitized_text[:200] + "...",
            },
            "job_matched": {"description": "Custom Job Description Provided"},
            "evaluation": match_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
