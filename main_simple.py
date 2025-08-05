from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="ChordCircle API",
    description="Backend API for ChordCircle music platform integration",
    version="1.0.0"
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
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )