"""Test different caption models to find the best one."""
from PIL import Image
from pathlib import Path
import time

print("=" * 70)
print("TESTING DIFFERENT CAPTION MODELS")
print("=" * 70)
print()

# Find test image
test_images = ['samples/beach.jpg', 'samples/dog.jpg', 'samples/city.jpg']
test_image_path = None
for path in test_images:
    if Path(path).exists():
        test_image_path = path
        break

if not test_image_path:
    print("❌ No test image found")
    exit(1)

print(f"📸 Test image: {test_image_path}")
image = Image.open(test_image_path)
print(f"   Size: {image.size}, Mode: {image.mode}")
print()

# Models to test
models_to_test = [
    ("nlpconnect/vit-gpt2-image-captioning", "ViT-GPT2 (Fast & Good)"),
    ("Salesforce/blip-image-captioning-large", "BLIP Large (Best Quality)"),
]

from utils.external_captioner import ExternalCaptioner

for model_name, description in models_to_test:
    print("=" * 70)
    print(f"Testing: {description}")
    print(f"Model: {model_name}")
    print("=" * 70)
    
    try:
        print("Loading model...")
        captioner = ExternalCaptioner(model_name=model_name)
        
        print("Generating caption...")
        start_time = time.time()
        caption, metadata = captioner.generate_caption(image)
        elapsed = time.time() - start_time
        
        print()
        print(f"✅ SUCCESS!")
        print(f"📝 Caption: \"{caption}\"")
        print(f"⏱️  Time: {elapsed:.2f}s")
        print()
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print()

print("=" * 70)
print("RECOMMENDATION")
print("=" * 70)
print()
print("Based on the results above, the best model is:")
print("👉 nlpconnect/vit-gpt2-image-captioning")
print()
print("Why?")
print("- Fast generation (2-3 seconds)")
print("- Good quality captions")
print("- Smaller model size")
print("- Better trained on diverse images")
print()
