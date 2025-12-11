# 🔑 Setup Gemini API Key - Do This First!

## Step 1: Get Your FREE API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with Google
3. Click "Create API Key"
4. Click "Create API key in new project"
5. **COPY the key** (starts with AIza...)

---

## Step 2: Set the API Key in PowerShell

Open PowerShell and run this command:

```powershell
$env:GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

**Replace the XXX with your actual key!**

---

## Step 3: Test It Works

```powershell
python test_gemini_simple.py
```

You should see: "AI works by..." and "✅ Gemini is working!"

---

## Step 4: Run the App

```powershell
python -m streamlit run app_eduvision.py
```

Then:
1. Go to http://localhost:8501
2. Select "Google Gemini"
3. Enter your API key in the sidebar
4. Upload image
5. Generate captions!

---

## ⚠️ Important Notes

- The API key is **FREE**
- No credit card needed
- 60 requests per minute
- You must set it EVERY TIME you open a new PowerShell window

---

## 🔄 To Make It Permanent (Optional)

Add to your PowerShell profile:

```powershell
notepad $PROFILE
```

Add this line:
```powershell
$env:GEMINI_API_KEY="your-key-here"
```

Save and close.

---

## ✅ Quick Commands

```powershell
# 1. Set API key
$env:GEMINI_API_KEY="your-key-here"

# 2. Test it
python test_gemini_simple.py

# 3. Run app
python -m streamlit run app_eduvision.py
```

---

**Get your key now**: https://makersuite.google.com/app/apikey
