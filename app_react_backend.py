"""Flask backend API for React frontend."""
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
import io
import os

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables for models
caption_generator = None
feature_extractor = None


def load_models():
    """Load model, tokenizer, and feature extractor."""
    global caption_generator, feature_extractor
    
    try:
        logger.info("Loading models...")
        tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
        model = load_model(config.get('paths.model_file'))
        feature_extractor = FeatureExtractor()
        
        max_length = config.get('model.max_length', 34)
        beam_width = config.get('inference.beam_width', 3)
        use_beam_search = config.get('inference.use_beam_search', True)
        
        caption_generator = CaptionGenerator(
            model=model,
            tokenizer=tokenizer,
            max_length=max_length,
            beam_width=beam_width,
            use_beam_search=use_beam_search
        )
        
        logger.info("Models loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'models_loaded': caption_generator is not None
    })


@app.route('/generate', methods=['POST'])
def generate_caption():
    """Generate caption for uploaded image."""
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read and validate image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract features
        features = feature_extractor.extract_from_pil(image)
        
        # Generate caption
        caption = caption_generator.generate(features)
        
        logger.info(f"Generated caption: {caption}")
        
        return jsonify({
            'caption': caption,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        'message': 'AI Caption Generator API',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'Health check',
            '/generate': 'Generate caption (POST with image)'
        }
    })


if __name__ == '__main__':
    # Load models on startup
    if load_models():
        print("=" * 50)
        print("🚀 Flask Backend Server Starting...")
        print("=" * 50)
        print("📡 API will be available at: http://localhost:5000")
        print("🔗 React frontend should connect to this URL")
        print("=" * 50)
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to load models. Please check your model files.")
