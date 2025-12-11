"""Test caption generation with real images."""
from PIL import Image
from utils.external_captioner import ExternalCaptioner
import time

print("=" * 70)
print("TESTING CAPTIONS WITH REAL IMAGES")
print("=" * 70)
print()

captioner = ExternalCaptioner()

test_images = [
    ('samples_real/beach.jpg', 'Beach Scene'),
    ('samples_real/dog.jpg', 'Dog Scene'),
    ('samples_real/city.jpg', 'City Scene'),
]

for img_path, description in test_images:
    print(f"📸 {description}")
    print(f"   File: {img_path}")
    
    try:
        image = Image.open(img_path)
        print(f"   Size: {image.size}")
        
        print("   Generating caption...")
        start = time.time()
        caption, metadata = captioner.generate_caption(image)
        elapsed = time.time() - start
        
        print(f"   ✅ Caption: \"{caption}\"")
        print(f"   ⏱️  Time: {elapsed:.2f}s")
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()

print("=" * 70)
print("✅ CAPTION GENERATION TEST COMPLETE")
print("=" * 70)
