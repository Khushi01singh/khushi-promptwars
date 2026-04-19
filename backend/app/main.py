from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import upload, jobs

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personalized AI Recruitment Agent API",
    description="Backend API for the recruitment agent",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    # --- DEBUGGING SNIPPET FOR CLOUD RUN STARTUP ---
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("STARTUP ERROR: GOOGLE_API_KEY is explicitly None or empty at application boot time!")
    else:
        masked_key = api_key[:4] + "***" + api_key[-4:] if len(api_key) > 8 else "***"
        logger.info(f"STARTUP SUCCESS: GOOGLE_API_KEY is correctly loaded into the container! Masked: {masked_key}")
    # -----------------------------------------------


# CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload & Process"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs & Match"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Personalized AI Recruitment Agent API"}
