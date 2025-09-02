import os
import uuid
import aiofiles
from typing import Optional, Dict
from fastapi import UploadFile, HTTPException
import asyncio
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        self.temp_dir = "/tmp/text_analysis"
        self.upload_progress: Dict[str, float] = {}
        os.makedirs(self.temp_dir, exist_ok=True)
    
    async def save_temp_file(self, file: UploadFile, session_id: str) -> str:
        """Save uploaded file temporarily with progress tracking"""
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.temp_dir, f"{file_id}.txt")
        
        try:
            # Initialize progress
            self.upload_progress[session_id] = 0.0
            
            # Get file size
            file_size = 0
            contents = await file.read()
            file_size = len(contents)
            
            # Reset file pointer
            await file.seek(0)
            
            # Save file with progress tracking
            async with aiofiles.open(file_path, 'wb') as f:
                chunk_size = 8192
                bytes_written = 0
                
                while True:
                    chunk = await file.read(chunk_size)
                    if not chunk:
                        break
                    
                    await f.write(chunk)
                    bytes_written += len(chunk)
                    
                    # Update progress
                    if file_size > 0:
                        self.upload_progress[session_id] = (bytes_written / file_size) * 100
            
            # Set complete
            self.upload_progress[session_id] = 100.0
            
            logger.info(f"File saved temporarily: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise HTTPException(status_code=500, detail="Error saving file")
    
    async def read_temp_file(self, file_path: str) -> str:
        """Read content from temporary file"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return content
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise HTTPException(status_code=500, detail="Error reading file")
    
    def delete_temp_file(self, file_path: str) -> bool:
        """Delete temporary file after processing"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted temporary file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def get_upload_progress(self, session_id: str) -> float:
        """Get upload progress for session"""
        return self.upload_progress.get(session_id, 0.0)
    
    def cleanup_old_files(self, max_age_seconds: int = 3600):
        """Clean up old temporary files"""
        import time
        current_time = time.time()
        
        for filename in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age_seconds:
                    self.delete_temp_file(file_path)