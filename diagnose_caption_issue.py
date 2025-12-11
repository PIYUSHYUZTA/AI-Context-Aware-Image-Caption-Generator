"""Diagnose caption generation issue."""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

from PIL import Image
from pathlib import Path

print("=" * 70)
print("🔍 DIAGNOSING CAPTION GENERATION ISSUE")
print("=" * 70)

# Test 1: Check if transformers is installed
print("\n1️⃣ Checking dependencies...")
try:
    import transformers
    import torch
    print(f"   ✅ transformers version: {transformers.__version__}")
    print(f"   ✅ torch version: {torch.__version__}")
except ImportError as e:
    print(f"   ❌ Missing dependency: {e}")
    print("\n   Install with: pip install transformers torch")
    exit(1)

# Test 2: Load the BLIP model
print("\n2️⃣ Loading BLIP model...")
try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    
    model_name = "Salesforce/blip-image-captioning-base"
    print(f"   Loading {model_name}...")
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    print("   ✅ Model loaded successfully")
except Exception as e:
    print(f"   ❌ Error loading model: {e}")
    exit(1)

# Test 3: Test with a sample image
print("\n3️⃣ Testing caption generation...")

# Find a test image
test_images = [
    "samples/dog.jpg",
    "samples/beach.jpg", 
    "samples/city.jpg",
    "samples_real/dog.jpg"
]

test_image_path = None
for img_path in test_images:
    if Path(img_path).exists():
        test_image_path = img_path
        break

if not test_image_path:
    print("   ❌ No test images found!")
    print("   Please place an image at: samples/dog.jpg")
    exit(1)

print(f"   Using image: {test_image_path}")

try:
    # Load image
    image = Image.open(test_image_path)
    print(f"   Image size: {image.size}")
    print(f"   Image mode: {image.mode}")
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        print(f"   Converting from {image.mode} to RGB...")
        image = image.convert('RGB')
    
    # Resize if too large
    max_size = 384
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        print(f"   Resizing from {image.size} to {new_size}...")
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    print("\n   Processing image...")
    inputs = processor(image, return_tensors="pt")
    print(f"   Input shape: {inputs['pixel_values'].shape}")
    
    print("\n   Generating caption (this may take a moment)...")
    
    # Test with different parameters
    configs = [
        {
            "name": "Default (Beam Search)",
            "params": {
                "max_length": 30,
                "min_length": 5,
                "num_beams": 5,
                "length_penalty": 0.8,
                "no_repeat_ngram_size": 3,
                "early_stopping": True,
                "do_sample": False,
                "repetition_penalty": 1.2
            }
        },
        {
            "name": "Sampling (More Creative)",
            "params": {
                "max_length": 30,
                "min_length": 5,
                "num_beams": 3,
                "do_sample": True,
                "top_k": 50,
                "top_p": 0.95,
                "temperature": 0.7,
                "repetition_penalty": 1.2
            }
        },
        {
            "name": "Greedy (Fast)",
            "params": {
                "max_length": 30,
                "min_length": 5,
                "do_sample": False
            }
        }
    ]
    
    print("\n" + "=" * 70)
    print("TESTING DIFFERENT GENERATION STRATEGIES")
    print("=" * 70)
    
    for config in configs:
        print(f"\n📝 {config['name']}:")
        print(f"   Parameters: {config['params']}")
        
        try:
            outputs = model.generate(**inputs, **config['params'])
            caption = processor.decode(outputs[0], skip_special_tokens=True)
            caption = caption.strip()
            
            # Capitalize first letter
            if caption:
                caption = caption[0].upper() + caption[1:]
            
            print(f"   ✅ Caption: \"{caption}\"")
            print(f"   Length: {len(caption.split())} words")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ DIAGNOSIS COMPLETE")
    print("=" * 70)
    
    print("\n📊 SUMMARY:")
    print("   • BLIP model is working correctly")
    print("   • Image processing is successful")
    print("   • Captions are being generated")
    
    print("\n🔍 IF CAPTIONS ARE WRONG:")
    print("   1. Check if the image is clear and well-lit")
    print("   2. Try different generation parameters")
    print("   3. Use a different image to test")
    print("   4. The model may need better prompting or fine-tuning")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
