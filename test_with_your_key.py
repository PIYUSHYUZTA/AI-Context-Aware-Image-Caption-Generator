"""Test with your Gemini API key."""
from PIL import Image
from utils.ai_caption_apis import get_captioner

# PUT YOUR API KEY HERE
GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE"  # Replace this!

# Test with sample image
image_path = "samples/dog.jpg"

print("Testing Google Gemini with your API key...")
print("=" * 60)

try:
    # Create captioner
    captioner = get_captioner("gemini", GEMINI_API_KEY)
    
    # Load image
    image = Image.open(image_path)
    
    # Generate 5 caption options
    print("\nGenerating 5 caption options...\n")
    captions = captioner.generate_multiple_options(image, num_options=5)
    
    # Display results
    for i, caption in enumerate(captions, 1):
        print(f"Option {i}: {caption}")
        print()
    
    print("=" * 60)
    print("✅ SUCCESS! Gemini is working!")
    print("\nNow open the app and use it:")
    print("1. Go to http://localhost:8501")
    print("2. Select 'Google Gemini'")
    print("3. Enter your API key")
    print("4. Upload image and generate!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("1. You replaced 'PASTE_YOUR_KEY_HERE' with your actual key")
    print("2. Your key is correct (starts with AIza...)")
    print("3. You have internet connection")
