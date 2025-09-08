import os
import uuid
import aiofiles
from typing import Optional, Dict, AsyncGenerator
from fastapi import UploadFile, HTTPException
import asyncio
import logging
import time
import mmap
from pathlib import Path

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        self.temp_dir = "/tmp/text_analysis"
        self.upload_progress: Dict[str, float] = {}
        self.max_file_size = 50 * 1024 * 1024  # 50MB limit
        self.chunk_size = 64 * 1024  # 64KB chunks for better performance
        os.makedirs(self.temp_dir, exist_ok=True)
    
    async def save_temp_file(self, file: UploadFile, session_id: str) -> str:
        """Save uploaded file temporarily with optimized performance for large files"""
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.temp_dir, f"{file_id}.txt")
        
        try:
            # Initialize progress
            self.upload_progress[session_id] = 0.0
            
            # Check file size if available
            file_size = getattr(file, 'size', None)
            if file_size and file_size > self.max_file_size:
                raise HTTPException(
                    status_code=413, 
                    detail=f"File too large. Maximum size is {self.max_file_size // (1024*1024)}MB"
                )
            
            # Save file with optimized streaming
            async with aiofiles.open(file_path, 'wb') as f:
                bytes_written = 0
                start_time = time.time()
                
                while True:
                    chunk = await file.read(self.chunk_size)
                    if not chunk:
                        break
                    
                    await f.write(chunk)
                    bytes_written += len(chunk)
                    
                    # Update progress and check size limit
                    if bytes_written > self.max_file_size:
                        os.remove(file_path)
                        raise HTTPException(
                            status_code=413,
                            detail="File too large during upload"
                        )
                    
                    # Update progress if we know the file size
                    if file_size and file_size > 0:
                        self.upload_progress[session_id] = (bytes_written / file_size) * 100
                    else:
                        # Estimate progress based on chunks (less accurate but gives feedback)
                        self.upload_progress[session_id] = min(95.0, bytes_written / (1024 * 1024) * 10)
            
            # Finalize
            self.upload_progress[session_id] = 100.0
            end_time = time.time()
            
            logger.info(f"File saved temporarily: {file_path} ({bytes_written} bytes in {end_time - start_time:.2f}s)")
            return file_path
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    async def read_temp_file(self, file_path: str) -> str:
        """Read content from temporary file with optimized performance"""
        try:
            file_size = os.path.getsize(file_path)
            
            # For small files, read normally
            if file_size < 1024 * 1024:  # < 1MB
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                return content
            
            # For large files, use memory mapping for better performance
            logger.info(f"Reading large file ({file_size} bytes) using memory mapping")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                    content = mmapped_file.read().decode('utf-8')
                    
            return content
            
        except UnicodeDecodeError as e:
            logger.error(f"File encoding error: {e}")
            raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text")
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
    async def read_file_streaming(self, file_path: str) -> AsyncGenerator[str, None]:
        """Stream file content for processing very large files"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                while True:
                    chunk = await f.read(self.chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            logger.error(f"Error streaming file: {e}")
            raise HTTPException(status_code=500, detail=f"Error streaming file: {str(e)}")
    
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
        """Clean up old temporary files (automatic cleanup)"""
        current_time = time.time()
        deleted_count = 0
        total_size_deleted = 0
        
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        file_size = os.path.getsize(file_path)
                        if self.delete_temp_file(file_path):
                            deleted_count += 1
                            total_size_deleted += file_size
            
            if deleted_count > 0:
                logger.info(f"Cleanup: Deleted {deleted_count} old files, freed {total_size_deleted / (1024*1024):.2f}MB")
                
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_temp_directory_stats(self) -> Dict[str, any]:
        """Get statistics about temporary directory"""
        try:
            files = []
            total_size = 0
            current_time = time.time()
            
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    file_size = stat.st_size
                    file_age = current_time - stat.st_mtime
                    
                    files.append({
                        "name": filename,
                        "size": file_size,
                        "age_seconds": file_age,
                        "created": time.ctime(stat.st_ctime)
                    })
                    total_size += file_size
            
            return {
                "directory": self.temp_dir,
                "file_count": len(files),
                "total_size_bytes": total_size,
                "total_size_mb": total_size / (1024 * 1024),
                "files": files
            }
            
        except Exception as e:
            logger.error(f"Error getting directory stats: {e}")
            return {"error": str(e)}