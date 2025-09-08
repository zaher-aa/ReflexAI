from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.api import analysis_router, ollama_router
from app.core.config import settings

app = FastAPI(title="Text Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router.router, prefix="/api")
app.include_router(ollama_router.router, prefix="/api/ollama", tags=["ollama"])

@app.get("/")
async def root():
    return {"message": "Text Analysis API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)