"""
FastAPI OCR Application
Main application file with CORS middleware and route registration
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import config
from routes import ocr, table


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print("🚀 Starting PaddleOCR API Server...")
    print(f"📍 GPU Mode: {config.USE_GPU}")
    print(f"🌐 Language: {config.MODEL_LANG}")
    print(f"📁 Max Upload Size: {config.MAX_UPLOAD_SIZE / 1024 / 1024}MB")
    print("✅ Server ready!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down PaddleOCR API Server...")


# Create FastAPI application
app = FastAPI(
    title="PaddleOCR API",
    description="FastAPI application for OCR (text and table) using PaddleOCR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ocr.router)
app.include_router(table.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PaddleOCR API Server",
        "version": "1.0.0",
        "endpoints": {
            "text_ocr": "/ocr",
            "table_ocr": "/table",
            "documentation": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Global health check endpoint"""
    return {
        "status": "healthy",
        "service": "paddleocr_api",
        "gpu_enabled": config.USE_GPU
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
