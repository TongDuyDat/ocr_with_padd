"""
OCR Service layer with model caching and async processing
"""
import asyncio
from typing import Optional, Dict, Any, List
from paddleocr import PaddleOCR, PPStructureV3
import config
from models import OCRTextResult, BoundingBox


class OCRModelManager:
    """
    Singleton class to manage PaddleOCR models with caching
    """
    _instance = None
    _text_ocr_model: Optional[PaddleOCR] = None
    _table_ocr_model: Optional[PPStructureV3] = None
    _text_lock = asyncio.Lock()  # Separate lock for text model
    _table_lock = asyncio.Lock()  # Separate lock for table model
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def get_text_ocr_model(self) -> PaddleOCR:
        """
        Get or initialize text OCR model (lazy loading with caching)
        
        Returns:
            PaddleOCR instance
        """
        if self._text_ocr_model is None:
            async with self._text_lock:  # Use text-specific lock
                # Double-check locking pattern
                if self._text_ocr_model is None:
                    # Run model initialization in thread pool to avoid blocking
                    loop = asyncio.get_event_loop()
                    self._text_ocr_model = await loop.run_in_executor(
                        None,
                        lambda: PaddleOCR(**config.TEXT_OCR_CONFIG)
                    )
                    print("✅ Text OCR model loaded and cached")
        
        return self._text_ocr_model
    
    async def get_table_ocr_model(self) -> PPStructureV3:
        """
        Get or initialize table OCR model (lazy loading with caching)
        
        Returns:
            PPStructureV3 instance
        """
        if self._table_ocr_model is None:
            async with self._table_lock:  # Use table-specific lock
                # Double-check locking pattern
                if self._table_ocr_model is None:
                    # Run model initialization in thread pool to avoid blocking
                    loop = asyncio.get_event_loop()
                    self._table_ocr_model = await loop.run_in_executor(
                        None,
                        lambda: PPStructureV3(**config.TABLE_OCR_CONFIG)
                    )
                    print("✅ Table OCR model loaded and cached")
        
        return self._table_ocr_model


# Global instance
model_manager = OCRModelManager()


async def process_text_ocr(image_path: str) -> List[OCRTextResult]:
    """
    Process text OCR on an image
    
    Args:
        image_path: Path to image file
        
    Returns:
        List of OCR text results
    """
    # Get cached model
    ocr_model = await model_manager.get_text_ocr_model()
    
    # Run OCR in thread pool to avoid blocking event loop
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: ocr_model.ocr(image_path)
    )
    # Parse results
    ocr_results = []
    
    # New PaddleOCR format with custom config returns a list of dicts
    if result and len(result) > 0:
        first_result = result[0]
        
        # Check if it's the new format (dict with rec_texts, rec_scores, rec_polys)
        if isinstance(first_result, dict):
            rec_texts = first_result.get('rec_texts', [])
            rec_scores = first_result.get('rec_scores', [])
            rec_polys = first_result.get('rec_polys', [])
            
            # Combine results
            for i in range(len(rec_texts)):
                text = rec_texts[i] if i < len(rec_texts) else ""
                confidence = float(rec_scores[i]) if i < len(rec_scores) else 0.0
                
                # Convert polygon to points format [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                bbox_points = []
                if i < len(rec_polys):
                    poly = rec_polys[i]
                    # poly is array([[x1,y1], [x2,y2], [x3,y3], [x4,y4]])
                    bbox_points = poly.tolist() if hasattr(poly, 'tolist') else list(poly)
                
                ocr_results.append(OCRTextResult(
                    text=text,
                    confidence=confidence,
                    bounding_box=BoundingBox(points=bbox_points) if bbox_points else None
                ))
        
        # Old format (list of [bbox, (text, confidence)])
        else:
            for line in first_result:
                if line and len(line) >= 2:
                    bbox_points = line[0]  # Bounding box coordinates
                    text_info = line[1]    # (text, confidence)
                    
                    if text_info and len(text_info) >= 2:
                        text = text_info[0]
                        confidence = float(text_info[1])
                        
                        ocr_results.append(OCRTextResult(
                            text=text,
                            confidence=confidence,
                            bounding_box=BoundingBox(points=bbox_points)
                        ))
    
    return ocr_results


async def process_table_ocr(image_path: str, output_format: str = "markdown") -> Dict[str, Any]:
    """
    Process table OCR on an image
    
    Args:
        image_path: Path to image file
        output_format: Output format ("markdown" or "text")
        
    Returns:
        Dictionary with table content and metadata
    """
    # Get cached model
    table_model = await model_manager.get_table_ocr_model()
    
    # Run table OCR in thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: table_model.predict(image_path)
    )
    
    # Process results
    content = ""
    raw_result = None
    
    if result:
        # PPStructureV3 returns a list of results
        for res in result:
            raw_result = {
                "layout": getattr(res, 'layout', None),
                "ocr": getattr(res, 'ocr', None),
            }
            
            # Extract content based on format
            if output_format == "markdown":
                # Try to get markdown representation
                try:
                    # Save to markdown and read it
                    import tempfile
                    import os
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        res.save_to_markdown(save_path=tmp_dir)
                        # Find the generated markdown file
                        md_files = [f for f in os.listdir(tmp_dir) if f.endswith('.md')]
                        if md_files:
                            with open(os.path.join(tmp_dir, md_files[0]), 'r', encoding='utf-8') as f:
                                content = f.read()
                except Exception as e:
                    # Fallback to text if markdown fails
                    content = str(res)
            else:
                # Plain text format
                content = str(res)
    
    return {
        "format": output_format,
        "content": content,
        "raw_result": raw_result
    }
