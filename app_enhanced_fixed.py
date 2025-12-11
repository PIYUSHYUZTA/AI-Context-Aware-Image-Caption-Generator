"""Enhanced Streamlit application with improved caption generation."""
import streamlit as st
from PIL import Image
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
import time
from pathlib import Path

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the same CSS from app_enhanced.py
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d1b4e 50%, #1a1a2e 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: titleGlow 3s ease-in-out infinite;
    }
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 20px rgba(167, 139, 250, 0.6)); }
        50% { filter: brightness(1.2) drop-shadow(0 0 40px rgba(236, 72, 153, 0.8)); }
    }
    .subtitle {
        text-align: center;
        color: #c4b5fd;
        font-size: 1.3rem;
        margin-bottom: 3rem;
    }
    .caption-box {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        color: white;
        font-size: 1.4rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.4);
        animation: slideInScale 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes slideInScale {
        from { opacity: 0; transform: scale(0.8) translateY(30px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6);
    }
    .info-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.3);
        color: #c4b5fd;
    }
    .warning-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid rgba(251, 191, 36, 0.3);
        color: #fbbf24;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load model, tokenizer, and feature extractor."""
    try:
        with st.spinner("Loading AI models..."):
            tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
            model = load_model(config.get('paths.model_file'))
            feature_extractor = FeatureExtractor()
            
            # Check vocabulary size
            vocab_size = len(tokenizer.word_index)
            
            max_length = config.get('model.max_length', 20)
            beam_width = config.get('inference.beam_width', 3)
            use_beam_search = config.get('inference.use_beam_search', True)
            
            caption_generator = CaptionGenerator(
                model=model,
                tokenizer=tokenizer,
                max_length=max_length,
                beam_width=beam_width,
                use_beam_search=use_beam_search
            )
            
            logger.info(f"Models loaded successfully (vocab: {vocab_size})")
            return caption_generator, feature_extractor, vocab_size
            
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        st.error(f"Error loading models: {e}")
        return None, None, 0


def generate_caption_with_fallback(image, caption_generator, feature_extractor):
    """Generate caption with fallback options."""
    try:
        # Extract features
        features = feature_extractor.extract_from_pil(image)
        
        # Generate caption
        caption = caption_generator.generate(features)
        
        return caption, "local_model"
        
    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        return f"Error: {str(e)}", "error"


def main():
    """Main application function."""
    
    # Header
    st.markdown('''
        <h1 class="main-header">✨ AI-Powered Image Caption Generator ✨</h1>
        <p class="subtitle">🎨 Transform Your Images into Beautiful Descriptions 🚀</p>
    ''', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model settings
        st.subheader("Model Configuration")
        use_beam_search = st.checkbox(
            "Use Beam Search",
            value=config.get('inference.use_beam_search', True),
            help="Beam search produces better captions but is slower"
        )
        
        if use_beam_search:
            beam_width = st.slider(
                "Beam Width",
                min_value=1,
                max_value=10,
                value=config.get('inference.beam_width', 3),
                help="Higher values may produce better results but are slower"
            )
        else:
            beam_width = 1
        
        st.divider()
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        <div class="info-box">
            <p>🧠 <strong>Deep Learning Powered</strong></p>
            <p>🎯 <strong>VGG16</strong> - Image features</p>
            <p>🔮 <strong>LSTM</strong> - Caption generation</p>
            <p>⚡ <strong>Beam Search</strong> - Optimal results</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Statistics
        st.subheader("📊 Model Info")
        try:
            tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
            vocab_size = len(tokenizer.word_index)
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("📚 Vocabulary", f"{vocab_size}")
            with col_b:
                st.metric("📏 Max Length", config.get('model.max_length', 20))
            
            # Warning for small vocabulary
            if vocab_size < 1000:
                st.markdown("""
                <div class="warning-box">
                    <p>⚠️ <strong>Limited Vocabulary</strong></p>
                    <p>Current model has only {0} words. For better results, consider retraining with more data.</p>
                </div>
                """.format(vocab_size), unsafe_allow_html=True)
        except:
            pass
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Your Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=config.get('app.supported_formats', ['jpg', 'jpeg', 'png']),
            help="Supported formats: JPG, JPEG, PNG"
        )
        
        # Sample images
        st.markdown("---")
        st.write("Or try a sample:")
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        
        with sample_col1:
            if st.button("🏖️ Beach"):
                if Path('samples/beach.jpg').exists():
                    st.session_state['sample_image'] = 'samples/beach.jpg'
                    st.rerun()
        with sample_col2:
            if st.button("🐕 Dog"):
                if Path('samples/dog.jpg').exists():
                    st.session_state['sample_image'] = 'samples/dog.jpg'
                    st.rerun()
        with sample_col3:
            if st.button("🌆 City"):
                if Path('samples/city.jpg').exists():
                    st.session_state['sample_image'] = 'samples/city.jpg'
                    st.rerun()
    
    with col2:
        st.markdown("### 🎯 AI Generated Caption")
        
        # Check for image
        image_source = None
        if 'sample_image' in st.session_state and st.session_state['sample_image']:
            image_source = st.session_state['sample_image']
            st.session_state['sample_image'] = None
        elif uploaded_file is not None:
            image_source = uploaded_file
        
        if image_source is not None:
            try:
                # Load image
                if isinstance(image_source, str):
                    image = Image.open(image_source)
                else:
                    image = Image.open(image_source)
                
                st.image(image, caption='Uploaded Image', use_container_width=True)
                
                # Generate button
                if st.button("🚀 Generate Caption with AI", type="primary"):
                    # Load models
                    caption_generator, feature_extractor, vocab_size = load_models()
                    
                    if caption_generator and feature_extractor:
                        # Update settings
                        caption_generator.use_beam_search = use_beam_search
                        caption_generator.beam_width = beam_width
                        
                        # Progress
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("🔍 Extracting features...")
                        progress_bar.progress(30)
                        start_time = time.time()
                        
                        status_text.text("✨ Generating caption...")
                        progress_bar.progress(60)
                        
                        caption, method = generate_caption_with_fallback(
                            image, caption_generator, feature_extractor
                        )
                        
                        elapsed_time = time.time() - start_time
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Complete!")
                        time.sleep(0.5)
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Display caption
                        st.markdown(
                            f'<div class="caption-box">"{caption}"</div>',
                            unsafe_allow_html=True
                        )
                        
                        # Metrics
                        st.markdown("---")
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric("⏱️ Time", f"{elapsed_time:.2f}s")
                        with metric_col2:
                            st.metric("📝 Words", len(caption.split()))
                        with metric_col3:
                            st.metric("🔧 Method", method.replace('_', ' ').title())
                        
                        # Technical details
                        with st.expander("🔍 Technical Details"):
                            st.write(f"**Search Method:** {'Beam Search' if use_beam_search else 'Greedy Search'}")
                            if use_beam_search:
                                st.write(f"**Beam Width:** {beam_width}")
                            st.write(f"**Vocabulary Size:** {vocab_size} words")
                            st.write(f"**Feature Extraction:** VGG16")
                            st.write(f"**Sequence Model:** LSTM")
                            
                            if vocab_size < 1000:
                                st.warning("⚠️ Small vocabulary may limit caption diversity. Consider retraining with more data.")
                        
                        logger.info(f"Generated caption: {caption} (time: {elapsed_time:.2f}s)")
                        
            except Exception as e:
                st.error(f"Error processing image: {e}")
                logger.error(f"Error in main app: {e}")
        else:
            st.markdown("""
                <div class="info-box" style="text-align: center; padding: 3rem;">
                    <h2 style="color: #c4b5fd;">👆 Upload an Image to Begin</h2>
                    <p style="font-size: 1.1rem; margin-top: 1rem;">
                        🎨 Select an image from the left<br>
                        ⚡ Click generate to see AI magic<br>
                        ✨ Get captions instantly
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Instructions
            with st.expander("📖 How to use"):
                st.markdown("""
                1. **Upload an image** using the file uploader
                2. **Adjust settings** in the sidebar (optional)
                3. **Click "Generate Caption"** to create a description
                4. **View results** including caption and generation time
                
                **Note:** Current model has limited vocabulary. For better results:
                - Retrain with more data (Flickr8k/COCO dataset)
                - Use external APIs (Google Vision, Azure, etc.)
                - Try different beam search settings
                """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #a78bfa; margin-top: 2rem;">
            <p style="font-size: 1.1rem;">✨ Built with ❤️ using TensorFlow & Streamlit ✨</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
