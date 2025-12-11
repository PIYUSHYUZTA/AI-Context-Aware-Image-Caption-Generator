"""Test with a real image."""
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
from PIL import Image
import traceback
from pathlib import Path

# Import utilities
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator

print("=== Testing Real Image Caption Generation ===\n")

# Load models
print("Loading models...")
tokenizer = load(open('tokenizer.pkl', 'rb'))
model = load_model('model.h5')
print("Models loaded successfully\n")

# Initialize feature extractor and caption generator
print("Initializing feature extractor...")
feature_extractor = FeatureExtractor()
print("Feature extractor ready\n")

caption_generator = CaptionGenerator(
    model=model,
    tokenizer=tokenizer,
    max_length=20,
    beam_width=3,
    use_beam_search=True
)
print("Caption generator ready\n")

# Check for sample images
sample_paths = [
    'samples/beach.jpg',
    'samples/dog.jpg', 
    'samples/city.jpg'
]

# Find any existing image
test_image = None
for path in sample_paths:
    if Path(path).exists():
        test_image = path
        break

if test_image:
    print(f"Testing with: {test_image}\n")
    try:
        # Load image
        image = Image.open(test_image)
        print(f"Image loaded: {image.size}, mode: {image.mode}")
        
        # Extract features
        print("Extracting features...")
        features = feature_extractor.extract_from_pil(image)
        print(f"Features extracted: shape={features.shape}")
        print(f"Features stats: min={features.min():.4f}, max={features.max():.4f}, mean={features.mean():.4f}\n")
        
        # Generate caption
        print("Generating caption...")
        caption = caption_generator.generate(features)
        
        print(f"\n=== RESULT ===")
        print(f"Caption: '{caption}'")
        
    except Exception as e:
        print(f"\n!!! ERROR !!!")
        print(f"Error: {e}")
        traceback.print_exc()
else:
    print("No sample images found. Creating a test image...")
    # Create a simple test image
    test_img = Image.new('RGB', (224, 224), color='blue')
    test_img.save('test_image.jpg')
    print("Test image created: test_image.jpg\n")
    
    try:
        # Extract features
        print("Extracting features...")
        features = feature_extractor.extract_from_pil(test_img)
        print(f"Features extracted: shape={features.shape}\n")
        
        # Generate caption
        print("Generating caption...")
        caption = caption_generator.generate(features)
        
        print(f"\n=== RESULT ===")
        print(f"Caption: '{caption}'")
        
    except Exception as e:
        print(f"\n!!! ERROR !!!")
        print(f"Error: {e}")
        traceback.print_exc()
