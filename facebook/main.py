from fastapi import FastAPI
from api.routes.facebook import router as facebook_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Facebook API Service",
    description="API service for managing Facebook posts",
    version="1.0.0"
)

# Include routers
app.include_router(facebook_router)

@app.get("/")
async def root():
    return {"message": "Facebook API Service đang hoạt động"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )