import shutil
import os
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader

# Temp folder jahan file kuch dair ke liye save hogi
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_pdf(file: UploadFile):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    # 1. File Save karna
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")

    # 2. Text Extract karna (Using PyPDF)
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        full_text = ""
        for page in pages:
            full_text += page.page_content + "\n\n"
            
        return {
            "filename": file.filename,
            "total_pages": len(pages),
            "extracted_text": full_text  # Pura text yahan hoga
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF reading failed: {str(e)}")
        
    finally:
        # 3. Cleanup (File delete kar dena taake server bhare na)
        if os.path.exists(file_path):
            os.remove(file_path)