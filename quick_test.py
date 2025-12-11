"""Quick test - Just paste your API key here and run!"""

# ============================================
# PASTE YOUR API KEY HERE:
# ============================================
GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE"
# ============================================

print("Testing Gemini API...")
print("=" * 60)

if GEMINI_API_KEY == "PASTE_YOUR_KEY_HERE":
    print("❌ ERROR: You need to paste your API key!")
    print("\n📋 Steps:")
    print("1. Get FREE key: https://makersuite.google.com/app/apikey")
    print("2. Open this file: quick_test.py")
    print("3. Replace 'PASTE_YOUR_KEY_HERE' with your key")
    print("4. Run: python quick_test.py")
    exit()

try:
    import google.generativeai as genai
    from PIL import Image
    
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Test 1: Simple text
    print("\n✅ Test 1: Simple text generation")
    response = model.generate_content("Say hello in 5 words")
    print(f"Response: {response.text}")
    
    # Test 2: Image caption
    print("\n✅ Test 2: Image caption generation")
    image = Image.open("samples/dog.jpg")
    
    prompt = """Analyze this image and provide 5 different caption options.

Make them varied:
- Option 1: Descriptive and detailed
- Option 2: Short and catchy
- Option 3: Creative/storytelling
- Option 4: Professional/formal
- Option 5: Casual/friendly

Format EXACTLY as:
1. [caption 1]
2. [caption 2]
3. [caption 3]
4. [caption 4]
5. [caption 5]"""
    
    response = model.generate_content([prompt, image])
    print(response.text)
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Your API key works!")
    print("\n📱 Now use it in the app:")
    print("1. Open: http://localhost:8501")
    print("2. Select 'Google Gemini'")
    print("3. Enter your API key")
    print("4. Upload image and generate!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n🔍 Troubleshooting:")
    print("1. Make sure your API key is correct")
    print("2. Check internet connection")
    print("3. Get new key: https://makersuite.google.com/app/apikey")
