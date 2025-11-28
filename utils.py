"""
Utility functions for image processing and validation
"""
import os
import tempfile
from pathlib import Path
from typing import BinaryIO
from fastapi import UploadFile, HTTPException
from PIL import Image
import config


async def validate_image(file: UploadFile) -> None:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file from FastAPI
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > config.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {config.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Validate it's a real image
    try:
        image = Image.open(file.file)
        image.verify()
        file.file.seek(0)  # Reset after verify
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image file: {str(e)}"
        )


async def save_upload_file_tmp(upload_file: UploadFile) -> str:
    """
    Save uploaded file to temporary location
    
    Args:
        upload_file: FastAPI UploadFile object
        
    Returns:
        Path to saved temporary file
    """
    try:
        suffix = Path(upload_file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            content = await upload_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        await upload_file.seek(0)  # Reset file pointer
        return tmp_path
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file: {str(e)}"
        )


def cleanup_temp_file(file_path: str) -> None:
    """
    Remove temporary file
    
    Args:
        file_path: Path to file to remove
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Ignore cleanup errors
