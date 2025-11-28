"""
Configuration settings for FastAPI OCR Application
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Model settings
MODEL_LANG = "vi"  # Vietnamese language support
USE_GPU = True  # Set to False for CPU-only mode
DEVICE = "gpu" if USE_GPU else "cpu"

# File upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB in bytes
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# OCR Model settings
TEXT_OCR_CONFIG = {
    "use_doc_orientation_classify": True,  # Phát hiện hướng văn bản
    "use_doc_unwarping": False,            # Làm phẳng tài liệu
    "use_textline_orientation": True,      # Phát hiện hướng dòng text
    "text_recognition_model_dir": "/mnt/d/ThucTap/OCR_Labs/models/tdd_ocr",
    # doc_parser=True,                    # Bật chế độ phân tích tài liệu
    # use_angle_cls=True,                 # Phát hiện góc xoay
    # lang='vi'
}

# Table OCR settings (PPStructureV3)
TABLE_OCR_CONFIG = {
    "lang": "vi", 
    "device": "gpu"
}

# Output directory
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
