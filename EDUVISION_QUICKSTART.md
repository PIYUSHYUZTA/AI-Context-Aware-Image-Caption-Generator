# 🚀 EduVision AI - Quick Start Guide

Get up and running with EduVision AI in 5 minutes!

## ✅ Prerequisites

Before you start, make sure you have:

1. ✅ Python 3.8 or higher installed
2. ✅ Model files ready:
   - `model.h5` (trained model)
   - `tokenizer.pkl` (tokenizer)
   - `descriptions.txt` (dataset)
3. ✅ Sample images (optional, in `samples/` folder)

## 📦 Step 1: Install Dependencies

```bash
pip install streamlit tensorflow pillow numpy pandas plotly pyyaml
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## 🔧 Step 2: Verify Model Files

Make sure these files exist in your project directory:

```
your-project/
├── app_eduvision.py
├── model.h5              ← Trained model
├── tokenizer.pkl         ← Tokenizer
├── descriptions.txt      ← Dataset
├── config.yaml           ← Configuration
└── pages/                ← Application modules
```

## ⚠️ Important: Fix Tokenizer First!

If you haven't already, rebuild the tokenizer:

```bash
python rebuild_tokenizer.py
```

This ensures the tokenizer has proper word-level tokenization with `startseq` and `endseq` tokens.

## 🎯 Step 3: Retrain Model (If Needed)

If your model was trained with the old tokenizer, retrain it:

```bash
python train_improved.py
```

This will create a new `model.h5` compatible with the fixed tokenizer.

## 🚀 Step 4: Launch EduVision AI

```bash
streamlit run app_eduvision.py
```

The application will open automatically in your browser at:
```
http://localhost:8501
```

## 🎨 Step 5: Explore the Platform

### 1. Start with Image Captioning 🎨
- Click "🎨 Image Captioning" in the sidebar
- Upload an image or use a sample
- Click "Generate Caption"
- See the AI-generated description!

### 2. Learn How It Works 🎓
- Go to "🎓 Learning Module"
- Explore interactive tutorials
- Understand the technology
- Learn about AI concepts

### 3. Analyze Performance 📊
- Visit "📊 Analytics Dashboard"
- View model metrics
- Explore dataset statistics
- Analyze vocabulary

### 4. Compare Models 🔬
- Open "🔬 Model Comparison Lab"
- Upload an image
- Compare Greedy vs Beam Search
- See performance differences

### 5. Explore Dataset 📈
- Check "📈 Dataset Explorer"
- Browse captions
- Analyze word frequency
- View visualizations

### 6. Evaluate Quality 🎯
- Go to "🎯 Evaluation Center"
- Upload image with reference captions
- Calculate BLEU scores
- Assess caption quality

## 🎯 Quick Demo Flow

**5-Minute Demo:**

1. **Launch** the app
2. **Navigate** to Image Captioning
3. **Upload** a sample image (or use provided samples)
4. **Generate** a caption
5. **Explore** the Learning Module to understand how it works
6. **Check** Analytics Dashboard for insights

## 🐛 Troubleshooting

### Issue: "Model file not found"
**Solution**: Make sure `model.h5` is in the project root directory

### Issue: "Tokenizer error" or "startseq not found"
**Solution**: Run `python rebuild_tokenizer.py` to fix the tokenizer

### Issue: "Model output mismatch"
**Solution**: Retrain the model with `python train_improved.py`

### Issue: "Import error"
**Solution**: Install missing dependencies:
```bash
pip install streamlit tensorflow pillow numpy pandas plotly pyyaml
```

### Issue: "Port already in use"
**Solution**: Use a different port:
```bash
streamlit run app_eduvision.py --server.port 8502
```

## 📊 Expected Results

After setup, you should see:

✅ Application loads without errors  
✅ All 6 modules accessible from sidebar  
✅ Image captioning generates descriptions  
✅ Analytics show dataset statistics  
✅ Learning module displays educational content  
✅ Model comparison works correctly  

## 🎓 For Educators

### Classroom Setup (15 minutes)

1. **Prepare Environment**
   ```bash
   # Clone or download project
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Verify Models**
   ```bash
   python check_model.py
   ```

3. **Launch Application**
   ```bash
   streamlit run app_eduvision.py
   ```

4. **Demo Flow**
   - Show image captioning (5 min)
   - Explain architecture in Learning Module (5 min)
   - Demonstrate model comparison (5 min)

### Student Assignment Ideas

1. **Beginner**: Generate captions for 5 different images, compare results
2. **Intermediate**: Analyze dataset statistics, create report
3. **Advanced**: Compare Greedy vs Beam Search, evaluate with metrics
4. **Research**: Explore vocabulary analysis, find patterns

## 🔧 Configuration Tips

### Adjust Generation Speed

In `config.yaml`:
```yaml
inference:
  beam_width: 3        # Lower = faster, Higher = better quality
  use_beam_search: true  # false for fastest generation
```

### Customize Model Settings

```yaml
model:
  max_length: 20       # Maximum caption length
  embedding_dim: 256   # Word embedding size
  lstm_units: 256      # LSTM memory units
```

## 📚 Next Steps

After getting started:

1. **Explore All Modules**: Try each feature
2. **Read Documentation**: Check EDUVISION_README.md
3. **Experiment**: Upload your own images
4. **Learn**: Go through the Learning Module
5. **Analyze**: Use Analytics Dashboard
6. **Compare**: Test different strategies
7. **Evaluate**: Measure caption quality

## 🎯 Learning Path

### Week 1: Basics
- Understand image captioning
- Generate captions for sample images
- Explore the interface

### Week 2: Deep Dive
- Study the Learning Module
- Understand VGG16 and LSTM
- Analyze dataset statistics

### Week 3: Advanced
- Compare generation strategies
- Evaluate caption quality
- Explore vocabulary analysis

### Week 4: Research
- Conduct experiments
- Analyze performance
- Create reports

## 💡 Pro Tips

1. **Start Simple**: Begin with sample images
2. **Learn First**: Visit Learning Module before experimenting
3. **Compare**: Try both Greedy and Beam Search
4. **Analyze**: Use Analytics to understand the data
5. **Evaluate**: Measure quality with metrics
6. **Experiment**: Upload diverse images to test

## 🎉 You're Ready!

You now have a fully functional educational AI platform!

**Enjoy exploring EduVision AI!** 🎓✨

---

Need help? Check:
- 📖 EDUVISION_README.md for detailed documentation
- 🐛 CAPTION_GENERATION_ISSUE_REPORT.md for troubleshooting
- 💬 Create an issue for support
