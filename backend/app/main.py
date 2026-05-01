"""
AI SDLC Orchestrator - Backend Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import requirements, stories, estimates

app = FastAPI(
    title="AI SDLC Orchestrator API",
    description="AI-powered Software Development Lifecycle platform",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(requirements.router, prefix="/api/v1/requirements", tags=["requirements"])
app.include_router(stories.router, prefix="/api/v1/stories", tags=["stories"])
app.include_router(estimates.router, prefix="/api/v1/estimates", tags=["estimates"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI SDLC Orchestrator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-sdlc-orchestrator"}