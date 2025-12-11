"""Image processing utilities."""
import numpy as np
from PIL import Image
from typing import Optional, Tuple
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import Model
from utils.logger import logger


class FeatureExtractor:
    """Singleton class for efficient feature extraction."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize feature extractor with VGG16."""
        if self._model is None:
            logger.info("Loading VGG16 model for feature extraction...")
            base_model = VGG16()
            self._model = Model(
                inputs=base_model.inputs,
                outputs=base_model.layers[-2].output
            )
            logger.info("VGG16 model loaded successfully")
    
    def extract_from_path(
        self,
        image_path: str,
        target_size: Tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """Extract features from image file path.
        
        Args:
            image_path: Path to image file
            target_size: Target image size
            
        Returns:
            Feature vector
        """
        try:
            image = load_img(image_path, target_size=target_size)
            image = img_to_array(image)
            image = image.reshape((1, *image.shape))
            image = preprocess_input(image)
            features = self._model.predict(image, verbose=0)
            return features
        except Exception as e:
            logger.error(f"Error extracting features from {image_path}: {e}")
            raise
    
    def extract_from_pil(
        self,
        image: Image.Image,
        target_size: Tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """Extract features from PIL Image.
        
        Args:
            image: PIL Image object
            target_size: Target image size
            
        Returns:
            Feature vector
        """
        try:
            image = image.resize(target_size)
            image = img_to_array(image)
            image = image.reshape((1, *image.shape))
            image = preprocess_input(image)
            features = self._model.predict(image, verbose=0)
            return features
        except Exception as e:
            logger.error(f"Error extracting features from PIL image: {e}")
            raise
    
    def extract_from_array(
        self,
        image_array: np.ndarray,
        target_size: Tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """Extract features from numpy array.
        
        Args:
            image_array: Image as numpy array
            target_size: Target image size
            
        Returns:
            Feature vector
        """
        try:
            # Convert to PIL and back to ensure correct format
            image = Image.fromarray(image_array.astype('uint8'))
            return self.extract_from_pil(image, target_size)
        except Exception as e:
            logger.error(f"Error extracting features from array: {e}")
            raise


def validate_image(
    image_path: str,
    max_size_mb: float = 10.0,
    allowed_formats: Optional[list] = None
) -> Tuple[bool, str]:
    """Validate image file.
    
    Args:
        image_path: Path to image file
        max_size_mb: Maximum file size in MB
        allowed_formats: List of allowed formats
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if allowed_formats is None:
        allowed_formats = ['JPEG', 'PNG', 'BMP']
    
    try:
        # Check file exists
        from pathlib import Path
        path = Path(image_path)
        if not path.exists():
            return False, "File does not exist"
        
        # Check file size
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"File size ({size_mb:.2f}MB) exceeds limit ({max_size_mb}MB)"
        
        # Check format
        with Image.open(image_path) as img:
            if img.format not in allowed_formats:
                return False, f"Format {img.format} not supported. Allowed: {allowed_formats}"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating image: {str(e)}"
