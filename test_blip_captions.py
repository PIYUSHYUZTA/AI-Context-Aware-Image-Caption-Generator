"""Test the new BLIP model for better captions."""
import requests
import time

print("=" * 70)
print("🧪 TESTING HUGGING FACE BLIP MODEL")
print("=" * 70)
print()

test_images = [
    ('samples/dog.jpg', 'Dog Image'),
    ('samples/beach.jpg', 'Beach Image'),
    ('samples/city.jpg', 'City Image')
]

for img_path, description in test_images:
    try:
        print(f"\n📸 Testing: {description} ({img_path})")
        print("-" * 70)
        
        with open(img_path, 'rb') as f:
            files = {'file': f}
            start_time = time.time()
            
            # Test with external BLIP model (use_external=true)
            response = requests.post(
                'http://localhost:8000/api/v1/caption',
                files=files,
                params={'use_external': True, 'beam_width': 5}
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS!")
                print(f"📝 Caption: \"{data['caption']}\"")
                print(f"📊 Confidence: {data['confidence']}")
                print(f"⏱️  Time: {elapsed:.2f}s")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Response: {response.text}")
                
    except FileNotFoundError:
        print(f"⚠️  File not found: {img_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

print()
print("=" * 70)
print("✅ TESTING COMPLETE")
print("=" * 70)
print()
print("The captions should now be much more accurate!")
print("Try uploading images in the browser at: http://localhost:3000")
