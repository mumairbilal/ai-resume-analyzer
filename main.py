import sys
import os
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from modules.construction.ingest import process_pdf
# 👇 chat_with_document import kiya
from modules.construction.analyzer import analyze_document, chat_with_document 

app = FastAPI(title=settings.PROJECT_NAME)

# 👇 SIMPLE MEMORY (RAM) - Asli apps mein ye Database hota hai
contract_memory = {} 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def home():
    return {"status": "Active", "message": "Construction Engine is Running!"}

@app.post("/api/analyze")
async def analyze_rfp(file: UploadFile = File(...)):
    # 1. Text Extract
    ingest_result = await process_pdf(file)
    extracted_text = ingest_result["extracted_text"]
    filename = ingest_result["filename"]
    
    # 👇 2. Memory mein Store karo (Taake baad mein Chat kar sakein)
    contract_memory["current_doc"] = extracted_text
    
    # 3. Analyze
    ai_report = await analyze_document(extracted_text)
    
    return {
        "status": "Success",
        "filename": filename,
        "ai_report": ai_report
    }

# 👇 NAYA CHAT ENDPOINT
@app.post("/api/chat")
async def chat_rfp(question: str = Body(..., embed=True)):
    # Memory se text nikalo
    text = contract_memory.get("current_doc")
    
    if not text:
        return {"answer": "Error: Please upload a document first."}
    
    # AI se poocho
    answer = await chat_with_document(text, question)
    return {"answer": answer}