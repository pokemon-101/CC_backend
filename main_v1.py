from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

from app.core.config_v1 import settings

app = FastAPI(
    title="ChordCircle API",
    description="Backend API for ChordCircle music platform integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "ChordCircle API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-08-05T09:57:00Z"}

@app.get("/api/v1/health")
async def api_health_check():
    return {"status": "healthy", "api_version": "v1", "timestamp": "2025-08-05T09:57:00Z"}

if __name__ == "__main__":
    uvicorn.run(
        "main_v1:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )