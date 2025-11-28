"""
Text OCR endpoint
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from models import OCRResponse, OCRTextResult
from service import process_text_ocr
from utils import validate_image, save_upload_file_tmp, cleanup_temp_file

router = APIRouter(prefix="/ocr", tags=["Text OCR"])


@router.post("", response_model=OCRResponse)
async def ocr_text(file: UploadFile = File(..., description="Image file to perform OCR on")):
    """
    Perform text OCR on uploaded image
    
    - **file**: Image file (jpg, png, bmp, tiff, webp)
    
    Returns detected text with bounding boxes and confidence scores
    """
    temp_file_path = None
    
    try:
        # Validate image
        await validate_image(file)
        
        # Save to temporary file
        temp_file_path = await save_upload_file_tmp(file)
        
        # Process OCR
        results = await process_text_ocr(temp_file_path)
        
        # Combine all text into full context
        full_text = "\n".join([r.text for r in results])
        
        return OCRResponse(
            success=True,
            message="OCR completed successfully",
            context=full_text,
            results=results,
            total_detections=len(results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )
    finally:
        # Cleanup temporary file
        if temp_file_path:
            cleanup_temp_file(temp_file_path)
