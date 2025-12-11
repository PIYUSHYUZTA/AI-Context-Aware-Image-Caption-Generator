"""Simple test for Gemini API."""
try:
    from google import genai
    
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client()
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", 
        contents="Explain how AI works in a few words"
    )
    print(response.text)
    
except ImportError as e:
    print(f"Import Error: {e}")
    print("\nTrying alternative import...")
    
    try:
        import google.generativeai as genai
        import os
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("\n❌ No API key found!")
            print("\nSet it with:")
            print('$env:GEMINI_API_KEY="your-key-here"')
            print("\nOr get a key from: https://makersuite.google.com/app/apikey")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Explain how AI works in a few words")
            print(response.text)
            print("\n✅ Gemini is working!")
            
    except Exception as e:
        print(f"Error: {e}")
        
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure:")
    print("1. You have set GEMINI_API_KEY environment variable")
    print("2. Run: $env:GEMINI_API_KEY=\"your-key-here\"")
    print("3. Get key from: https://makersuite.google.com/app/apikey")
