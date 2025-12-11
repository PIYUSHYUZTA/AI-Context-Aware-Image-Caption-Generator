"""Quick test to verify all components are ready."""
import sys

print("=" * 50)
print("🔍 Testing AI Caption Generator Setup")
print("=" * 50)
print()

# Test 1: Python dependencies
print("1️⃣ Checking Python dependencies...")
try:
    import fastapi
    import uvicorn
    import tensorflow
    from PIL import Image
    import numpy as np
    print("   ✅ FastAPI, Uvicorn, TensorFlow, PIL, NumPy - OK")
except ImportError as e:
    print(f"   ❌ Missing dependency: {e}")
    sys.exit(1)

# Test 2: Model files
print("\n2️⃣ Checking model files...")
import os
if os.path.exists('model.h5'):
    print("   ✅ model.h5 found")
else:
    print("   ❌ model.h5 NOT FOUND")
    
if os.path.exists('tokenizer.pkl'):
    print("   ✅ tokenizer.pkl found")
else:
    print("   ❌ tokenizer.pkl NOT FOUND")

# Test 3: Frontend files
print("\n3️⃣ Checking frontend files...")
if os.path.exists('frontend/src/App.js'):
    print("   ✅ React App.js found")
else:
    print("   ❌ React App.js NOT FOUND")

if os.path.exists('frontend/package.json'):
    print("   ✅ package.json found")
else:
    print("   ❌ package.json NOT FOUND")

# Test 4: API file
print("\n4️⃣ Checking API file...")
if os.path.exists('api.py'):
    print("   ✅ api.py found")
else:
    print("   ❌ api.py NOT FOUND")

print("\n" + "=" * 50)
print("✅ Setup verification complete!")
print("=" * 50)
print("\n📋 Next steps:")
print("1. Run: python api.py (in one terminal)")
print("2. Run: cd frontend && npm start (in another terminal)")
print("3. Open: http://localhost:3000")
