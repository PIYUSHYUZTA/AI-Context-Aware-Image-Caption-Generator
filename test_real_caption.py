"""Test caption generation with real image."""
from PIL import Image
from utils.ai_caption_apis import get_captioner
import os

# Test with sample image
image_path = "samples/dog.jpg"

print("Testing caption generation...")
print("=" * 60)

# Test with ViT-GPT2 (offline)
print("\n1. Testing ViT-GPT2 (Offline Model):")
print("-" * 60)
try:
    from utils.pretrained_caption import PretrainedCaptioner
    captioner = PretrainedCaptioner()
    image = Image.open(image_path)
    caption = captioner.generate_caption(image)
    print(f"Result: {caption}")
except Exception as e:
    print(f"Error: {e}")

# Test with OpenAI (if API key available)
print("\n2. Testing OpenAI GPT-4 Vision:")
print("-" * 60)
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    try:
        captioner = get_captioner("openai", openai_key)
        image = Image.open(image_path)
        captions = captioner.generate_multiple_options(image, num_options=5)
        for i, cap in enumerate(captions, 1):
            print(f"Option {i}: {cap}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found. Set OPENAI_API_KEY environment variable to test.")

# Test with Gemini (if API key available)
print("\n3. Testing Google Gemini:")
print("-" * 60)
gemini_key = os.getenv('GOOGLE_API_KEY')
if gemini_key:
    try:
        captioner = get_captioner("gemini", gemini_key)
        image = Image.open(image_path)
        captions = captioner.generate_multiple_options(image, num_options=5)
        for i, cap in enumerate(captions, 1):
            print(f"Option {i}: {cap}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found. Set GOOGLE_API_KEY environment variable to test.")

print("\n" + "=" * 60)
print("Test complete!")
print("\nTo test with your own image:")
print("1. Replace 'samples/dog.jpg' with your image path")
print("2. Run: python test_real_caption.py")
