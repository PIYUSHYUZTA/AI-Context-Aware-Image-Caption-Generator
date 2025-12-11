# 🎓 AI Image Caption Generator - Mentor Submission

## 📌 Project Overview

A professional AI-powered image caption generator with a modern React frontend and FastAPI backend. The system uses deep learning (VGG16 + LSTM) to automatically generate descriptive captions for uploaded images.

## ✨ Key Features

### 🎨 Professional UI Design
- **Animated gradient background** with floating orbs
- **Smooth animations** using Framer Motion
- **Responsive design** that works on all devices
- **Modern glassmorphism** effects

### 🤖 AI Capabilities
- **Deep learning model** (VGG16 + LSTM architecture)
- **Beam search** for high-quality captions
- **Fast processing** with caching
- **Batch processing** support

### 🔧 Technical Stack
- **Frontend**: React 18, Framer Motion, Lucide Icons, Axios
- **Backend**: FastAPI, TensorFlow/Keras, PIL
- **AI Model**: VGG16 (feature extraction) + LSTM (caption generation)

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Node.js 14+
- All dependencies installed (see requirements.txt)

### Running the Application

**Option 1: Using Batch Files (Easiest)**

1. **Start Backend** - Double-click `start_backend.bat`
   - Backend runs on http://localhost:8000
   
2. **Start Frontend** - Double-click `start_frontend.bat`
   - Frontend opens at http://localhost:3000

**Option 2: Manual Start**

Terminal 1 (Backend):
```bash
python api.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```


## 📸 How to Use

1. **Open the application** at http://localhost:3000
2. **Upload an image** by clicking or dragging & dropping
3. **Click "Generate Caption"** button
4. **View the AI-generated caption** with confidence score
5. **Copy the caption** to clipboard if needed

## 🎯 All 7 Icons Implemented

✅ **Sparkles** - Logo animation  
✅ **Upload** - File upload indicator  
✅ **X** - Clear/remove image  
✅ **Loader2** - Loading spinner  
✅ **Zap** - Generate button & fast feature  
✅ **ImageIcon** - Caption display & accuracy feature  
✅ **Download** - Copy caption button  

## 🎨 Professional Design Elements

### Animated Background
- 3 floating gradient orbs
- Smooth color transitions
- Purple, pink, and blue theme

### UI Components
- Glassmorphism cards
- Smooth hover effects
- Professional color scheme
- Responsive layout

### Animations
- Header entrance animation
- Button hover effects
- Image preview transitions
- Caption reveal animation

## 📊 API Endpoints

### Generate Caption
```
POST /api/v1/caption
- Upload image file
- Returns: caption, confidence, processing time
```

### Health Check
```
GET /health
- Check if backend is running
```

### API Documentation
```
GET /api/docs
- Interactive Swagger UI
```

## 🔧 Technical Details

### Model Architecture
- **Feature Extractor**: VGG16 (pre-trained on ImageNet)
- **Sequence Generator**: LSTM with attention
- **Vocabulary Size**: ~8,000 words
- **Max Caption Length**: 34 words

### Performance
- **Average processing time**: 0.5-2 seconds
- **Caching**: Enabled for faster repeated requests
- **Batch processing**: Up to 10 images

## 📁 Project Structure

```
├── frontend/              # React application
│   ├── src/
│   │   ├── App.js        # Main component
│   │   ├── App.css       # Styling
│   │   └── index.js      # Entry point
│   └── public/
├── api.py                # FastAPI backend
├── model.h5              # Trained AI model
├── tokenizer.pkl         # Word tokenizer
├── utils/                # Utility modules
├── start_backend.bat     # Backend launcher
└── start_frontend.bat    # Frontend launcher
```

## 🎓 Mentor Demonstration Script

1. **Show the professional UI**
   - Point out animated background
   - Highlight modern design

2. **Upload a test image**
   - Demonstrate drag & drop
   - Show image preview

3. **Generate caption**
   - Click generate button
   - Show loading animation
   - Display generated caption

4. **Highlight features**
   - Show all 7 working icons
   - Demonstrate copy functionality
   - Show confidence score

5. **Technical overview**
   - Open API docs at /api/docs
   - Explain model architecture
   - Show processing metrics

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify Python dependencies: `pip install -r requirements.txt`
- Check if model files exist (model.h5, tokenizer.pkl)

### Frontend won't start
- Check if port 3000 is available
- Verify Node dependencies: `cd frontend && npm install`

### Caption generation fails
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify image format (JPG, PNG supported)

## 📝 Future Enhancements

- [ ] Multiple language support
- [ ] Social media integration
- [ ] Caption style customization
- [ ] Mobile app version
- [ ] Real-time video captioning

## 👨‍💻 Development Notes

This project demonstrates:
- Full-stack development skills
- Modern React patterns and hooks
- RESTful API design
- Deep learning integration
- Professional UI/UX design
- Production-ready code structure

---

**Built with ❤️ for AI/ML Internship Submission**
