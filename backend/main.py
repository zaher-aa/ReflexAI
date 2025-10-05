from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from app.api import analysis_router, ollama_router
from app.core.config import settings

app = FastAPI(title="Text Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

app.include_router(analysis_router.router, prefix="/api")
app.include_router(ollama_router.router, prefix="/api/ollama", tags=["ollama"])

@app.get("/")
async def root():
    return {"message": "Text Analysis API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)