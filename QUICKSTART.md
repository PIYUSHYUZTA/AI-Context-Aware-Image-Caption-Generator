# 🚀 Quick Start Guide

Get up and running with the AI Image Caption Generator in minutes!

## Prerequisites

- Python 3.8 or higher
- 4GB RAM minimum
- 10GB disk space
- (Optional) Docker for containerized deployment

---

## Option 1: Docker (Recommended) ⚡

**Fastest way to get started!**

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd image-caption-generator

# 2. Start all services
docker-compose up -d

# 3. Access the applications
# Streamlit UI: http://localhost:8501
# API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs

# 4. Stop services
docker-compose down
```

That's it! 🎉

---

## Option 2: Local Installation 💻

### Step 1: Setup Environment

```bash
# Clone repository
git clone <your-repo-url>
cd image-caption-generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Dataset (Optional for Training)

```bash
# Run the download helper
python scripts/download_dataset.py

# Follow the instructions to download Flickr8k dataset
# Or use your own pre-trained model
```

### Step 3: Prepare Data (If Training)

```bash
# Preprocess captions
python preprocess_captions.py

# Extract image features
python preprocess_images.py

# Create train/val/test splits
python scripts/create_splits.py
```

### Step 4: Train Model (Optional)

```bash
# Train the model
python train_improved.py

# Or use a pre-trained model by placing:
# - model.h5
# - tokenizer.pkl
# - features.pkl
# in the project root
```

### Step 5: Run Applications

**Option A: Streamlit Web App**

```bash
# Run the professional app
streamlit run app_professional.py

# Or run the enhanced app
streamlit run app_enhanced.py

# Access at: http://localhost:8501
```

**Option B: REST API**

```bash
# Start the API server
python api.py

# Access at: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

---

## 🎯 Quick Test

### Test the Web Interface

1. Open http://localhost:8501
2. Upload an image (JPG, PNG)
3. Click "Generate Caption"
4. View the results!

### Test the API

```bash
# Using curl
curl -X POST "http://localhost:8000/api/v1/caption" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"

# Using Python
import requests

with open('your_image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/caption',
        files={'file': f}
    )
    print(response.json())
```

---

## 📁 Project Structure

```
image-caption-generator/
├── api.py                      # FastAPI REST API
├── app_enhanced.py             # Enhanced Streamlit app
├── app_professional.py         # Professional Streamlit app
├── model.py                    # Model architecture
├── train_improved.py           # Training script
├── config.yaml                 # Configuration
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Multi-container setup
├── utils/                      # Utility modules
│   ├── config.py
│   ├── logger.py
│   ├── image_utils.py
│   ├── model_utils.py
│   ├── data_utils.py
│   ├── visualization.py
│   └── advanced_metrics.py
├── tests/                      # Test suite
├── scripts/                    # Helper scripts
└── docs/                       # Documentation
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
model:
  max_length: 34              # Maximum caption length
  beam_width: 3               # Beam search width

inference:
  use_beam_search: true       # Enable beam search
  temperature: 1.0            # Sampling temperature

app:
  max_upload_size: 10         # Max file size (MB)
  supported_formats:          # Allowed formats
    - jpg
    - jpeg
    - png
```

---

## 🔧 Common Commands

### Development

```bash
# Run tests
pytest tests/ -v

# Check code quality
flake8 .
black --check .

# Format code
black .

# Run with hot reload
streamlit run app_professional.py --server.runOnSave true
```

### Docker

```bash
# Build images
docker-compose build

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Remove everything
docker-compose down -v
```

---

## 🐛 Troubleshooting

### Issue: Models not found

**Solution**: Ensure you have `model.h5` and `tokenizer.pkl` in the project root.

```bash
# Check if files exist
ls -la *.h5 *.pkl

# If missing, train the model or download pre-trained weights
```

### Issue: Out of memory

**Solution**: Reduce batch size or use smaller images.

```yaml
# In config.yaml
training:
  batch_size: 16  # Reduce from 32
```

### Issue: Port already in use

**Solution**: Change ports in docker-compose.yml or stop conflicting services.

```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8501

# macOS/Linux:
lsof -i :8501

# Kill the process or change port
```

### Issue: CUDA/GPU errors

**Solution**: Install TensorFlow GPU version or use CPU.

```bash
# For GPU support
pip install tensorflow-gpu==2.16.1

# Or force CPU
export CUDA_VISIBLE_DEVICES=""
```

---

## 📚 Next Steps

1. **Explore the API**: Visit http://localhost:8000/api/docs
2. **Read Documentation**: Check out README_PROFESSIONAL.md
3. **Try Examples**: Test with different images
4. **Customize**: Modify config.yaml for your needs
5. **Deploy**: Follow DEPLOYMENT.md for production

---

## 🆘 Getting Help

- **Documentation**: See README_PROFESSIONAL.md
- **Issues**: Open a GitHub issue
- **Deployment**: Check DEPLOYMENT.md
- **Contributing**: Read CONTRIBUTING.md

---

## 🎉 Success!

You're now ready to generate image captions! 

Try uploading different types of images:
- 🏖️ Outdoor scenes
- 🐕 Animals
- 🌆 Urban landscapes
- 👥 People
- 🍕 Food

Enjoy! 🚀
