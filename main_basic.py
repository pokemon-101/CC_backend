from fastapi import FastAPI
import uvicorn
import os

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
        "status": "running",
        "python_version": os.sys.version
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/health")
async def api_health_check():
    return {"status": "healthy", "api_version": "v1"}

if __name__ == "__main__":
    uvicorn.run(
        "main_basic:app",
        host="0.0.0.0",
        port=8000
    )