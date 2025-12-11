"""Simulate exactly what the React frontend does when generating a caption."""
import requests
import json
from pathlib import Path

print("=" * 70)
print("🎬 SIMULATING REACT FRONTEND REQUEST")
print("=" * 70)
print()

# This simulates exactly what happens when you click "Generate Caption"
# in the React app

print("📤 Step 1: User uploads image")
print("   → Image file selected: samples/dog.jpg")
print()

print("📤 Step 2: User clicks 'Generate Caption' button")
print("   → React creates FormData")
print("   → Appends file with key 'file'")
print("   → Sends POST request to http://localhost:8000/api/v1/caption")
print()

print("🔄 Step 3: Sending request...")
print()

try:
    # Open the file
    with open('samples/dog.jpg', 'rb') as f:
        # Create form data exactly like React does
        files = {'file': ('dog.jpg', f, 'image/jpeg')}
        
        # Send POST request exactly like axios does
        response = requests.post(
            'http://localhost:8000/api/v1/caption',
            files=files,
            headers={
                'Accept': 'application/json'
            }
        )
        
        print(f"📥 Step 4: Response received")
        print(f"   Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Caption generated:")
            print("=" * 70)
            print(f"📝 Caption: \"{data['caption']}\"")
            print(f"📊 Confidence: {data['confidence']}")
            print(f"⏱️  Processing Time: {data['processing_time']}s")
            print(f"🔑 Image Hash: {data['image_hash']}")
            print(f"📅 Timestamp: {data['timestamp']}")
            print("=" * 70)
            print()
            print("🎉 This is exactly what should appear in the React app!")
            print()
            print("If you're not seeing this in the browser:")
            print("1. Check browser console (F12) for errors")
            print("2. Check Network tab for failed requests")
            print("3. Try clearing browser cache (Ctrl+Shift+Delete)")
            
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            
except FileNotFoundError:
    print("❌ Error: samples/dog.jpg not found")
    print("   Please make sure the sample image exists")
    
except requests.exceptions.ConnectionError:
    print("❌ Error: Cannot connect to backend")
    print("   Make sure backend is running: python api.py")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print()
print("=" * 70)
print("🌐 FRONTEND URL: http://localhost:3000")
print("🔧 BACKEND URL: http://localhost:8000")
print("=" * 70)
