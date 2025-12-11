"""FastAPI REST API for Image Caption Generator - Production Ready."""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uvicorn
from PIL import Image
import io
import time
import hashlib
from datetime import datetime
from pickle import load
from tensorflow.keras.models import load_model
import numpy as np

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor, validate_image
from utils.model_utils import CaptionGenerator
from utils.external_captioner import HybridCaptioner, ExternalCaptioner

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Caption Generator API",
    description="Production-ready REST API for generating image captions using deep learning",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global models (loaded once)
caption_generator = None
feature_extractor = None
hybrid_captioner = None
request_cache = {}

# Response models
class CaptionResponse(BaseModel):
    """Response model for caption generation."""
    caption: str = Field(..., description="Generated caption")
    confidence: float = Field(..., description="Model confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    image_hash: str = Field(..., description="Unique image identifier")
    timestamp: str = Field(..., description="Generation timestamp")
    model_version: str = Field(default="2.0.0", description="Model version")
    
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    timestamp: str
    version: str

class BatchCaptionRequest(BaseModel):
    """Request model for batch processing."""
    use_beam_search: bool = True
    beam_width: int = 3
    temperature: float = 1.0

class MetricsResponse(BaseModel):
    """API metrics response."""
    total_requests: int
    cache_hits: int
    cache_misses: int
    average_processing_time: float


# Metrics tracking
metrics = {
    "total_requests": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "processing_times": []
}


@app.on_event("startup")
async def load_models():
    """Load models on startup."""
    global caption_generator, feature_extractor, hybrid_captioner
    
    try:
        logger.info("Loading models...")
        
        # Try to load local models (optional fallback)
        local_generator = None
        local_extractor = None
        try:
            tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
            model = load_model(config.get('paths.model_file'))
            local_extractor = FeatureExtractor()
            
            local_generator = CaptionGenerator(
                model=model,
                tokenizer=tokenizer,
                max_length=config.get('model.max_length', 34),
                beam_width=config.get('inference.beam_width', 3),
                use_beam_search=config.get('inference.use_beam_search', True)
            )
            logger.info("Local models loaded successfully")
        except Exception as e:
            logger.warning(f"Local models not available: {e}")
        
        # Initialize hybrid captioner with external (Hugging Face BLIP) as default
        hybrid_captioner = HybridCaptioner(
            local_generator=local_generator,
            local_feature_extractor=local_extractor,
            use_external_by_default=True  # Use BLIP by default for better captions
        )
        
        # Keep references for backward compatibility
        caption_generator = local_generator
        feature_extractor = local_extractor
        
        logger.info("Caption system initialized (using Hugging Face BLIP for best quality)")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise


def calculate_image_hash(image_bytes: bytes) -> str:
    """Calculate hash for image caching."""
    return hashlib.md5(image_bytes).hexdigest()


def calculate_confidence(features: np.ndarray) -> float:
    """Calculate pseudo-confidence score based on feature variance."""
    variance = np.var(features)
    confidence = min(0.95, max(0.60, 1.0 - (variance / 1000)))
    return round(confidence, 3)


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint."""
    return {
        "message": "AI Image Caption Generator API",
        "version": "2.0.0",
        "docs": "/api/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if hybrid_captioner else "unhealthy",
        model_loaded=hybrid_captioner is not None,
        timestamp=datetime.now().isoformat(),
        version="2.0.0"
    )


@app.post("/api/v1/caption", response_model=CaptionResponse)
async def generate_caption(
    file: UploadFile = File(...),
    use_beam_search: bool = True,
    beam_width: int = 5,
    use_cache: bool = True,
    use_external: bool = True
):
    """
    Generate caption for uploaded image.
    
    Args:
        file: Image file (JPEG, PNG, BMP)
        use_beam_search: Use beam search for better quality
        beam_width: Beam width (1-10)
        use_cache: Use caching for faster responses
        use_external: Use external Hugging Face BLIP model (recommended for best quality)
        
    Returns:
        CaptionResponse with generated caption and metadata
    """
    if not hybrid_captioner:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # Update metrics
    metrics["total_requests"] += 1
    
    try:
        # Read image
        image_bytes = await file.read()
        image_hash = calculate_image_hash(image_bytes)
        
        # Check cache
        cache_key = f"{image_hash}_{use_external}_{beam_width}"
        if use_cache and cache_key in request_cache:
            metrics["cache_hits"] += 1
            logger.info(f"Cache hit for image {image_hash}")
            return request_cache[cache_key]
        
        metrics["cache_misses"] += 1
        
        # Validate and process image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Generate caption using hybrid captioner
        start_time = time.time()
        
        # Use Hugging Face BLIP for better captions
        caption, method, metadata = hybrid_captioner.generate(
            image,
            use_external=use_external,
            num_beams=beam_width,
            max_length=30
        )
        
        processing_time = time.time() - start_time
        metrics["processing_times"].append(processing_time)
        
        # Calculate confidence (higher for external model)
        confidence = 0.95 if method == "external_api" else 0.85
        
        # Create response
        response = CaptionResponse(
            caption=caption,
            confidence=confidence,
            processing_time=round(processing_time, 3),
            image_hash=image_hash,
            timestamp=datetime.now().isoformat()
        )
        
        # Cache response
        if use_cache:
            request_cache[cache_key] = response
        
        logger.info(f"Generated caption: '{caption}' using {method} (time: {processing_time:.3f}s)")
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/batch-caption")
async def batch_generate_captions(
    files: List[UploadFile] = File(...),
    use_beam_search: bool = True,
    beam_width: int = 3
):
    """
    Generate captions for multiple images.
    
    Args:
        files: List of image files
        use_beam_search: Use beam search
        beam_width: Beam width
        
    Returns:
        List of caption responses
    """
    if not caption_generator or not feature_extractor:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
    
    results = []
    
    for file in files:
        try:
            response = await generate_caption(file, use_beam_search, beam_width, use_cache=True)
            results.append({
                "filename": file.filename,
                "success": True,
                "data": response
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results, "total": len(files), "successful": sum(1 for r in results if r["success"])}


@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get API usage metrics."""
    avg_time = (
        sum(metrics["processing_times"]) / len(metrics["processing_times"])
        if metrics["processing_times"] else 0
    )
    
    return MetricsResponse(
        total_requests=metrics["total_requests"],
        cache_hits=metrics["cache_hits"],
        cache_misses=metrics["cache_misses"],
        average_processing_time=round(avg_time, 3)
    )


@app.delete("/api/v1/cache")
async def clear_cache():
    """Clear request cache."""
    request_cache.clear()
    return {"message": "Cache cleared", "timestamp": datetime.now().isoformat()}


@app.get("/api/v1/model-info")
async def get_model_info():
    """Get model information."""
    if not caption_generator:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_version": "2.0.0",
        "architecture": "CNN-LSTM with VGG16",
        "vocab_size": len(caption_generator.tokenizer.word_index) + 1,
        "max_length": caption_generator.max_length,
        "beam_width": caption_generator.beam_width,
        "use_beam_search": caption_generator.use_beam_search
    }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
