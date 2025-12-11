"""Test the API endpoint to see what error occurs."""
import requests

# Test the API
url = "http://localhost:8000/api/v1/caption"
files = {'file': open('samples/dog.jpg', 'rb')}

print("Testing API endpoint...")
print(f"URL: {url}")
print(f"File: samples/dog.jpg")
print()

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Caption: {data.get('caption')}")
        print(f"Confidence: {data.get('confidence')}")
        print(f"Processing Time: {data.get('processing_time')}s")
    else:
        print(f"\n❌ ERROR!")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
