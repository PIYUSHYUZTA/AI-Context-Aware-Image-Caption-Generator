# Installing External API Support

## 🚀 Quick Install

Run this command to install required packages:

```bash
pip install transformers torch pillow
```

Or use the requirements file:

```bash
pip install -r requirements_api.txt
```

## 📦 What Gets Installed

- **transformers** - Hugging Face library for BLIP model
- **torch** - PyTorch for model inference
- **pillow** - Image processing (already installed)

## ⏱️ Installation Time

- Download size: ~2-3 GB
- Installation time: 5-10 minutes
- First run: Additional 1-2 GB for BLIP model download

## ✅ Verify Installation

Run this test script:

```bash
python test_external_api.py
```

## 🎯 Usage

1. Install packages (above)
2. Run the app: `streamlit run app_enhanced.py`
3. Select "External API (BLIP)" in sidebar
4. Upload image and generate caption

## 💡 Benefits

- **Better Quality**: Professional-grade captions
- **Larger Vocabulary**: 30,000+ words
- **Context Aware**: Understands complex scenes
- **No Training**: Works immediately

## 🔄 Fallback

If external API fails, app automatically falls back to local model.
