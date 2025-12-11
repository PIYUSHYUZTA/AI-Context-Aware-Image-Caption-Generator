# 🔑 API Setup Guide for AI Caption Generation

## Overview

EduVision AI now supports **3 AI providers** for image captioning:

1. **ViT-GPT2** (Free, Offline) - No API key needed
2. **OpenAI GPT-4 Vision** (Best Quality) - Requires API key
3. **Google Gemini** (Free Tier) - Requires API key

---

## 🚀 Quick Start

### Option 1: ViT-GPT2 (No Setup Required)
- **Cost**: Free
- **Setup**: None needed
- **Quality**: Good
- **Speed**: Fast (2-5 seconds)
- **Best for**: Quick testing, offline use

Just select "ViT-GPT2 (Free, Offline)" and start generating!

---

## 🔑 Option 2: OpenAI GPT-4 Vision Setup

### Step 1: Get API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### Step 2: Add Credits

1. Go to https://platform.openai.com/account/billing
2. Add payment method
3. Add credits ($5 minimum recommended)

### Step 3: Use in App

**Method A: Enter in App**
1. Select "OpenAI GPT-4 Vision" in sidebar
2. Paste API key in the text field
3. Generate captions!

**Method B: Set Environment Variable**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-key-here"

# Windows (CMD)
set OPENAI_API_KEY=sk-your-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-key-here
```

### Pricing
- **Cost**: ~$0.01 per image
- **Model**: gpt-4o-mini (cost-efficient)
- **Quality**: Best available

---

## 🔑 Option 3: Google Gemini Setup

### Step 1: Get API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### Step 2: Use in App

**Method A: Enter in App**
1. Select "Google Gemini" in sidebar
2. Paste API key in the text field
3. Generate captions!

**Method B: Set Environment Variable**
```bash
# Windows (PowerShell)
$env:GOOGLE_API_KEY="your-key-here"

# Windows (CMD)
set GOOGLE_API_KEY=your-key-here

# Linux/Mac
export GOOGLE_API_KEY=your-key-here
```

### Pricing
- **Cost**: FREE tier available
- **Limits**: 60 requests per minute
- **Model**: Gemini 1.5 Flash
- **Quality**: Excellent

---

## 📦 Install Required Packages

```bash
# For OpenAI
pip install openai

# For Google Gemini
pip install google-generativeai

# Install both
pip install openai google-generativeai
```

---

## 🎯 Comparison

| Feature | ViT-GPT2 | OpenAI GPT-4 | Google Gemini |
|---------|----------|--------------|---------------|
| **Cost** | Free | ~$0.01/image | Free tier |
| **Setup** | None | API key + billing | API key |
| **Quality** | Good | Best | Excellent |
| **Speed** | Fast (2-5s) | Medium (3-8s) | Fast (2-5s) |
| **Offline** | Yes | No | No |
| **Hashtags** | No | Yes | Yes |
| **Styles** | Limited | Multiple | Multiple |

---

## 🎨 Caption Styles (OpenAI & Gemini)

### 1. Descriptive
- Detailed, objective description
- Focus on what's visible
- Good for accessibility

**Example**: "A golden retriever playing with a red ball in a green park on a sunny day"

### 2. Creative
- Engaging, storytelling style
- Emotional and vivid
- Good for social media

**Example**: "Pure joy captured! This happy pup is living his best life chasing dreams (and balls) in the sunshine ☀️"

### 3. Technical
- Objective, analytical
- Composition and lighting details
- Good for photography

**Example**: "Well-composed outdoor shot featuring a golden retriever in mid-action, natural lighting, shallow depth of field, vibrant colors"

### 4. Social Media
- Catchy, engaging
- Includes hashtags
- Ready to post

**Example**: "Weekend vibes with my furry best friend! 🐕 #DogLife #PuppyLove #WeekendVibes #GoldenRetriever"

---

## 🔒 Security Best Practices

### DO:
✅ Use environment variables for API keys
✅ Keep API keys private
✅ Monitor usage and costs
✅ Set spending limits (OpenAI)
✅ Rotate keys periodically

### DON'T:
❌ Share API keys publicly
❌ Commit keys to Git
❌ Use keys in screenshots
❌ Share keys in chat/email

---

## 💡 Tips

### For Best Results:
1. **Use high-quality images** - Clear, well-lit photos work best
2. **Choose appropriate style** - Match style to your use case
3. **Try multiple providers** - Compare results
4. **Use hashtags feature** - Great for social media posts

### Cost Optimization:
1. **Start with free options** - Try ViT-GPT2 or Gemini first
2. **Use Gemini for volume** - Free tier is generous
3. **Use OpenAI for quality** - When you need the best
4. **Monitor usage** - Check API dashboards regularly

---

## 🐛 Troubleshooting

### "API key required" error
- Make sure you entered the API key correctly
- Check if environment variable is set
- Verify key hasn't expired

### "Rate limit exceeded"
- **Gemini**: Wait a minute (60 requests/min limit)
- **OpenAI**: Check your usage tier

### "Insufficient credits"
- **OpenAI**: Add credits to your account
- **Gemini**: Should be free, check API status

### Slow generation
- First time downloads model (ViT-GPT2)
- API calls take 3-8 seconds (normal)
- Check internet connection

---

## 📞 Support

### OpenAI
- Docs: https://platform.openai.com/docs
- Status: https://status.openai.com
- Support: https://help.openai.com

### Google Gemini
- Docs: https://ai.google.dev/docs
- Support: https://support.google.com

---

## 🎉 You're Ready!

1. Choose your AI provider
2. Get API key (if needed)
3. Start generating amazing captions!

**Enjoy your AI-powered caption generation!** 🚀
