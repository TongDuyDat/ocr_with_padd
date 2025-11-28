"""
Table OCR endpoint
"""
from typing import Literal
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from models import TableOCRResponse
from service import process_table_ocr
from utils import validate_image, save_upload_file_tmp, cleanup_temp_file

router = APIRouter(prefix="/table", tags=["Table OCR"])


@router.post("", response_model=TableOCRResponse)
async def ocr_table(
    file: UploadFile = File(..., description="Image file containing table to perform OCR on"),
    format: Literal["markdown", "text"] = Query("markdown", description="Output format (markdown or text)")
):
    """
    Perform table OCR on uploaded image
    
    - **file**: Image file containing a table (jpg, png, bmp, tiff, webp)
    - **format**: Output format - "markdown" for markdown table or "text" for plain text
    
    Returns table content in requested format
    """
    temp_file_path = None
    
    try:
        # Validate image
        await validate_image(file)
        
        # Save to temporary file
        temp_file_path = await save_upload_file_tmp(file)
        
        # Process table OCR
        result = await process_table_ocr(temp_file_path, output_format=format)
        
        return TableOCRResponse(
            success=True,
            message="Table OCR completed successfully",
            format=result["format"],
            content=result["content"],
            raw_result=result["raw_result"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Table OCR processing failed: {str(e)}"
        )
    finally:
        # Cleanup temporary file
        if temp_file_path:
            cleanup_temp_file(temp_file_path)