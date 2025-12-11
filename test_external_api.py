"""Test external API caption generation."""
from PIL import Image
from pathlib import Path
import time

print("=" * 60)
print("TESTING EXTERNAL API CAPTION GENERATION")
print("=" * 60)
print()

# Check if packages are installed
print("📦 Checking required packages...")
try:
    import transformers
    print("✅ transformers installed")
except ImportError:
    print("❌ transformers not installed")
    print("   Run: pip install transformers")
    exit(1)

try:
    import torch
    print("✅ torch installed")
except ImportError:
    print("❌ torch not installed")
    print("   Run: pip install torch")
    exit(1)

print()

# Import external captioner
print("📥 Loading external captioner...")
try:
    from utils.external_captioner import ExternalCaptioner
    captioner = ExternalCaptioner()
    print("✅ External captioner initialized")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print()

# Find test image
test_images = [
    'samples/beach.jpg',
    'samples/dog.jpg',
    'samples/city.jpg',
    'test_image.jpg'
]

test_image_path = None
for path in test_images:
    if Path(path).exists():
        test_image_path = path
        break

if not test_image_path:
    print("📸 No test image found. Creating one...")
    test_img = Image.new('RGB', (224, 224), color='blue')
    test_img.save('test_image.jpg')
    test_image_path = 'test_image.jpg'
    print("✅ Test image created")

print(f"🖼️  Using image: {test_image_path}")
print()

# Load image
image = Image.open(test_image_path)
print(f"Image loaded: {image.size}, mode: {image.mode}")
print()

# Generate caption
print("🚀 Generating caption...")
print("⏳ This may take a moment on first run (downloading model)...")
print()

start_time = time.time()
try:
    caption, metadata = captioner.generate_caption(image)
    elapsed_time = time.time() - start_time
    
    print("=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print()
    print(f"📝 Caption: \"{caption}\"")
    print()
    print(f"⏱️  Time: {elapsed_time:.2f} seconds")
    print(f"🤖 Model: {metadata['model']}")
    print(f"🔧 Method: {metadata['method']}")
    print(f"📏 Max Length: {metadata['max_length']}")
    print(f"🔍 Beam Width: {metadata['num_beams']}")
    print()
    print("=" * 60)
    print("🎉 External API is working perfectly!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: streamlit run app_enhanced.py")
    print("2. Select 'External API (BLIP)' in sidebar")
    print("3. Upload an image and generate captions")
    print()
    
except Exception as e:
    print("=" * 60)
    print("❌ ERROR")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    import traceback
    traceback.print_exc()
