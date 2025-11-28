"""
Pydantic models for request and response validation
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    points: List[List[float]] = Field(..., description="List of 4 points [x, y]")


class OCRTextResult(BaseModel):
    """Single OCR text detection result"""
    text: str = Field(..., description="Detected text")
    confidence: float = Field(..., description="Confidence score (0-1)")
    bounding_box: Optional[BoundingBox] = Field(None, description="Bounding box coordinates")