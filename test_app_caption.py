"""Test the actual app caption generation flow."""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

from PIL import Image
from pathlib import Path
from utils.external_captioner import HybridCaptioner, ExternalCaptioner

print("=" * 70)
print("🔍 TESTING APP CAPTION GENERATION FLOW")
print("=" * 70)

# Test 1: Initialize HybridCaptioner (same as app)
print("\n1️⃣ Initializing HybridCaptioner...")
try:
    hybrid_captioner = HybridCaptioner(
        local_generator=None,
        local_feature_extractor=None,
        use_external_by_default=True
    )
    print("   ✅ HybridCaptioner initialized")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Check if external API is available
print("\n2️⃣ Checking external API availability...")
is_available = hybrid_captioner.is_external_available()
print(f"   External API available: {is_available}")

if not is_available:
    print("   ❌ External API not available!")
    print("   Install with: pip install transformers torch")
    exit(1)

# Test 3: Load test image
print("\n3️⃣ Loading test image...")
test_images = [
    "samples/dog.jpg",
    "samples/beach.jpg",
    "samples/city.jpg"
]

test_image_path = None
for img_path in test_images:
    if Path(img_path).exists():
        test_image_path = img_path
        break

if not test_image_path:
    print("   ❌ No test images found!")
    exit(1)

print(f"   Using: {test_image_path}")
image = Image.open(test_image_path)
print(f"   Image size: {image.size}, mode: {image.mode}")

# Test 4: Generate caption using the same method as app
print("\n4️⃣ Generating caption (same as app)...")
try:
    caption, method, metadata = hybrid_captioner.generate(
        image,
        use_external=True,
        num_beams=5
    )
    
    print(f"\n   ✅ SUCCESS!")
    print(f"   Caption: \"{caption}\"")
    print(f"   Method: {method}")
    print(f"   Metadata: {metadata}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Test with different images
print("\n" + "=" * 70)
print("5️⃣ TESTING WITH MULTIPLE IMAGES")
print("=" * 70)

for img_path in test_images:
    if Path(img_path).exists():
        print(f"\n📸 {img_path}:")
        try:
            image = Image.open(img_path)
            caption, method, metadata = hybrid_captioner.generate(
                image,
                use_external=True,
                num_beams=5
            )
            print(f"   Caption: \"{caption}\"")
        except Exception as e:
            print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)

print("\n📊 CONCLUSION:")
print("   If captions are showing correctly here but not in the app:")
print("   1. Check Streamlit session state")
print("   2. Check if model is being reloaded properly")
print("   3. Check for caching issues")
print("   4. Restart the Streamlit app")
