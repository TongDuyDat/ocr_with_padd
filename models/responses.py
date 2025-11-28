"""
Pydantic models for request and response validation
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from .results import OCRTextResult
class OCRResponse(BaseModel):
    """Response for text OCR endpoint"""
    success: bool = Field(..., description="Whether OCR was successful")
    message: str = Field(..., description="Status message")
    context: str = Field("", description="Complete text content from all detections")
    results: List[OCRTextResult] = Field(default_factory=list, description="List of detected texts")
    total_detections: int = Field(0, description="Total number of text detections")


class TableCell(BaseModel):
    """Table cell data"""
    text: str
    row: Optional[int] = None
    col: Optional[int] = None


class TableOCRResponse(BaseModel):
    """Response for table OCR endpoint"""
    success: bool = Field(..., description="Whether table OCR was successful")
    message: str = Field(..., description="Status message")
    format: Literal["markdown", "text"] = Field(..., description="Output format")
    content: str = Field(..., description="Table content in requested format")
    raw_result: Optional[dict] = Field(None, description="Raw OCR result from PPStructureV3")
