"""Test if the app components work correctly"""
import sys
from pathlib import Path

print("=" * 60)
print("TESTING APP COMPONENTS")
print("=" * 60)

# Test 1: Check required files
print("\n1. Checking required files...")
required_files = ['model.h5', 'tokenizer.pkl', 'features.pkl', 'config.yaml']
for file in required_files:
    exists = Path(file).exists()
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"   {file}: {status}")

# Test 2: Check imports
print("\n2. Checking imports...")
try:
    import streamlit as st
    print("   ✅ streamlit")
except ImportError as e:
    print(f"   ❌ streamlit: {e}")

try:
    from PIL import Image
    print("   ✅ PIL")
except ImportError as e:
    print(f"   ❌ PIL: {e}")

try:
    import tensorflow as tf
    print(f"   ✅ tensorflow {tf.__version__}")
except ImportError as e:
    print(f"   ❌ tensorflow: {e}")

# Test 3: Check utils modules
print("\n3. Checking utils modules...")
try:
    from utils.config import config
    print("   ✅ utils.config")
except ImportError as e:
    print(f"   ❌ utils.config: {e}")

try:
    from utils.logger import logger
    print("   ✅ utils.logger")
except ImportError as e:
    print(f"   ❌ utils.logger: {e}")

try:
    from utils.image_utils import FeatureExtractor
    print("   ✅ utils.image_utils")
except ImportError as e:
    print(f"   ❌ utils.image_utils: {e}")

try:
    from utils.model_utils import CaptionGenerator
    print("   ✅ utils.model_utils")
except ImportError as e:
    print(f"   ❌ utils.model_utils: {e}")

# Test 4: Load model and tokenizer
print("\n4. Testing model loading...")
try:
    from pickle import load
    from tensorflow.keras.models import load_model
    
    tokenizer = load(open('tokenizer.pkl', 'rb'))
    print(f"   ✅ Tokenizer loaded (vocab size: {len(tokenizer.word_index)})")
    
    model = load_model('model.h5')
    print(f"   ✅ Model loaded")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Test caption generation
print("\n5. Testing caption generation...")
try:
    from utils.image_utils import FeatureExtractor
    from utils.model_utils import CaptionGenerator
    from PIL import Image
    import numpy as np
    
    # Check if sample image exists
    sample_paths = ['samples/beach.jpg', 'samples/dog.jpg', 'samples/city.jpg']
    test_image = None
    for path in sample_paths:
        if Path(path).exists():
            test_image = path
            break
    
    if test_image:
        print(f"   Using test image: {test_image}")
        
        # Load image
        image = Image.open(test_image)
        print(f"   ✅ Image loaded: {image.size}")
        
        # Extract features
        feature_extractor = FeatureExtractor()
        features = feature_extractor.extract_from_pil(image)
        print(f"   ✅ Features extracted: {features.shape}")
        
        # Generate caption
        caption_generator = CaptionGenerator(
            model=model,
            tokenizer=tokenizer,
            max_length=20,
            beam_width=3,
            use_beam_search=True
        )
        caption = caption_generator.generate(features)
        print(f"   ✅ Caption generated: '{caption}'")
        
    else:
        print("   ⚠️  No sample images found in samples/ folder")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nIf all tests passed, run: streamlit run app_enhanced.py")
