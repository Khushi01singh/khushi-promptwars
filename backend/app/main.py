from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import upload, jobs

app = FastAPI(
    title="Personalized AI Recruitment Agent API",
    description="Backend API for the recruitment agent",
    version="1.0.0",
)

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
