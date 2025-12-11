"""Test the complete flow from frontend to backend."""
import requests
import time

print("=" * 70)
print("🔍 TESTING COMPLETE CAPTION GENERATION FLOW")
print("=" * 70)
print()

# Test 1: Backend Health
print("1️⃣ Testing Backend Health...")
try:
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Backend is {data['status']}")
        print(f"   ✅ Models loaded: {data['model_loaded']}")
    else:
        print(f"   ❌ Backend health check failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Cannot connect to backend: {e}")
    exit(1)

print()

# Test 2: Frontend Accessibility
print("2️⃣ Testing Frontend Accessibility...")
try:
    response = requests.get("http://localhost:3000", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Frontend is accessible")
    else:
        print(f"   ⚠️  Frontend returned: {response.status_code}")
except Exception as e:
    print(f"   ❌ Cannot connect to frontend: {e}")

print()

# Test 3: Caption Generation with Sample Images
print("3️⃣ Testing Caption Generation...")
test_images = [
    'samples/dog.jpg',
    'samples/beach.jpg',
    'samples/city.jpg'
]

for img_path in test_images:
    try:
        print(f"\n   Testing: {img_path}")
        with open(img_path, 'rb') as f:
            files = {'file': f}
            start_time = time.time()
            response = requests.post(
                'http://localhost:8000/api/v1/caption',
                files=files
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Caption: \"{data['caption']}\"")
                print(f"   ⏱️  Time: {elapsed:.2f}s")
                print(f"   📊 Confidence: {data['confidence']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   Response: {response.text}")
    except FileNotFoundError:
        print(f"   ⚠️  File not found: {img_path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print()
print("=" * 70)
print("✅ TESTING COMPLETE")
print("=" * 70)
print()
print("📋 NEXT STEPS:")
print("1. Open browser: http://localhost:3000")
print("2. Upload an image")
print("3. Click 'Generate Caption'")
print("4. Check browser console (F12) for any errors")
print()
