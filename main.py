from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Sample API", version="1.0.0")


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    message: str


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint returning health status"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        message="Welcome to the Sample API!"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for container orchestration"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        message="Service is running"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)