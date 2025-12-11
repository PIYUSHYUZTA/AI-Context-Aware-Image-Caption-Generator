"""External API caption generation using Hugging Face models."""
from PIL import Image
import numpy as np
from typing import Optional, Tuple
from utils.logger import logger
import os

# Set Hugging Face cache to D drive
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'


class ExternalCaptioner:
    """Caption generator using Hugging Face transformers."""
    
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        """Initialize external captioner.
        
        Args:
            model_name: Hugging Face model name
            Options:
            - Salesforce/blip-image-captioning-base (balanced, recommended)
            - Salesforce/blip-image-captioning-large (best quality, slower)
            - microsoft/git-base-coco (good alternative)
        """
        self.model_name = model_name
        self.processor = None
        self.model = None
        self._initialized = False
    
    def _lazy_load(self):
        """Lazy load the model to avoid loading if not needed."""
        if self._initialized:
            return
        
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            
            logger.info(f"Loading {self.model_name}...")
            self.processor = BlipProcessor.from_pretrained(self.model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(self.model_name)
            self._initialized = True
            logger.info("External captioner loaded successfully")
            
        except ImportError:
            logger.error("transformers library not installed. Run: pip install transformers torch")
            raise ImportError(
                "Please install required packages:\n"
                "pip install transformers torch pillow"
            )
        except Exception as e:
            logger.error(f"Error loading external captioner: {e}")
            raise
    
    def generate_caption(
        self,
        image: Image.Image,
        max_length: int = 50,
        num_beams: int = 8,
        min_length: int = 10,
        temperature: float = 1.0
    ) -> Tuple[str, dict]:
        """Generate caption for image using external model.
        
        Args:
            image: PIL Image
            max_length: Maximum caption length (increased for more detail)
            num_beams: Number of beams for beam search (increased for better quality)
            min_length: Minimum caption length (increased for more descriptive captions)
            temperature: Sampling temperature
            
        Returns:
            Tuple of (caption, metadata)
        """
        self._lazy_load()
        
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image for optimal processing (larger size for better quality)
            target_size = 512  # Increased from 384 for better detail recognition
            if max(image.size) > target_size:
                ratio = target_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            elif max(image.size) < 256:
                # Upscale very small images
                ratio = 256 / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Process image
            inputs = self.processor(image, return_tensors="pt")
            
            # Generate caption with optimized parameters for better descriptions
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                num_beams=num_beams,
                length_penalty=1.0,  # Balanced length penalty
                no_repeat_ngram_size=3,
                early_stopping=True,
                temperature=temperature,
                do_sample=False,
                repetition_penalty=1.5  # Increased to avoid repetitive words
            )
            
            # Decode caption
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up caption
            caption = caption.strip()
            
            # Remove common artifacts and improve caption quality
            artifacts_to_remove = [
                "arafed", "araffe",  # Common BLIP artifacts
            ]
            
            for artifact in artifacts_to_remove:
                caption = caption.replace(artifact, "").strip()
            
            # Check if caption is generic or low quality
            generic_phrases = [
                "an image of", "a picture of", "a photo of",
                "there is", "there are", "this is"
            ]
            
            caption_lower = caption.lower()
            is_generic = any(phrase in caption_lower for phrase in generic_phrases)
            
            # If generic caption, try to improve it
            if is_generic:
                # Remove generic phrases
                for phrase in generic_phrases:
                    if caption_lower.startswith(phrase):
                        caption = caption[len(phrase):].strip()
                        caption = caption[0].upper() + caption[1:] if caption else caption
                        break
            
            # Check for very poor quality captions (pixelated, blurry mentions)
            quality_issues = ["pixeled", "pixel pixel", "blurry", "blurred"]
            has_quality_issue = any(issue in caption_lower for issue in quality_issues)
            
            # If quality issue detected, try with sampling for more creative description
            if has_quality_issue and num_beams > 1:
                logger.warning(f"Quality issue detected in caption: {caption}, trying alternative...")
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=5,
                    length_penalty=1.2,
                    no_repeat_ngram_size=2,
                    early_stopping=True,
                    do_sample=True,
                    top_k=50,
                    top_p=0.92,
                    temperature=0.8,
                    repetition_penalty=1.3
                )
                alt_caption = self.processor.decode(outputs[0], skip_special_tokens=True).strip()
                
                # Use alternative if it doesn't have quality issues
                alt_lower = alt_caption.lower()
                if not any(issue in alt_lower for issue in quality_issues):
                    caption = alt_caption
                    logger.info(f"Using alternative caption: {caption}")
            
            # Capitalize first letter
            if caption:
                caption = caption[0].upper() + caption[1:]
            
            metadata = {
                "model": self.model_name,
                "method": "external_api",
                "max_length": max_length,
                "num_beams": num_beams
            }
            
            logger.info(f"Generated caption: {caption}")
            return caption, metadata
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if external captioner is available."""
        try:
            import transformers
            import torch
            return True
        except ImportError:
            return False


class HybridCaptioner:
    """Hybrid captioner that uses both local and external models."""
    
    def __init__(
        self,
        local_generator=None,
        local_feature_extractor=None,
        use_external_by_default: bool = True
    ):
        """Initialize hybrid captioner.
        
        Args:
            local_generator: Local CaptionGenerator instance
            local_feature_extractor: Local FeatureExtractor instance
            use_external_by_default: Whether to use external API by default
        """
        self.local_generator = local_generator
        self.local_feature_extractor = local_feature_extractor
        self.use_external_by_default = use_external_by_default
        self.external_captioner = None
        
        # Try to initialize external captioner
        if use_external_by_default:
            try:
                self.external_captioner = ExternalCaptioner()
            except Exception as e:
                logger.warning(f"External captioner not available: {e}")
    
    def generate(
        self,
        image: Image.Image,
        use_external: Optional[bool] = None,
        **kwargs
    ) -> Tuple[str, str, dict]:
        """Generate caption using best available method.
        
        Args:
            image: PIL Image
            use_external: Force use of external API (None = auto)
            **kwargs: Additional arguments
            
        Returns:
            Tuple of (caption, method, metadata)
        """
        # Determine which method to use
        if use_external is None:
            use_external = self.use_external_by_default
        
        # Try external API first if requested
        if use_external and self.external_captioner:
            try:
                caption, metadata = self.external_captioner.generate_caption(image, **kwargs)
                return caption, "external_api", metadata
            except Exception as e:
                logger.warning(f"External API failed, falling back to local: {e}")
        
        # Fall back to local model
        if self.local_generator and self.local_feature_extractor:
            try:
                features = self.local_feature_extractor.extract_from_pil(image)
                caption = self.local_generator.generate(features)
                metadata = {
                    "model": "local",
                    "method": "local_model",
                    "vocab_size": len(self.local_generator.tokenizer.word_index)
                }
                return caption, "local_model", metadata
            except Exception as e:
                logger.error(f"Local model failed: {e}")
                raise
        
        raise RuntimeError("No caption generation method available")
    
    def is_external_available(self) -> bool:
        """Check if external API is available."""
        return self.external_captioner is not None and self.external_captioner.is_available()
