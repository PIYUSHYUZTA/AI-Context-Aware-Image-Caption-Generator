"""Professional Streamlit application for image caption generation."""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

import streamlit as st
from PIL import Image
import time
from pathlib import Path

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator
from utils.external_captioner import HybridCaptioner

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #0f0f23;
        background-image: 
            radial-gradient(at 0% 0%, rgba(102, 126, 234, 0.2) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(118, 75, 162, 0.2) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(102, 126, 234, 0.2) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(118, 75, 162, 0.2) 0px, transparent 50%);
    }
    
    /* Main container */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* Header */
    .header-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        color: #a0aec0;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Upload section */
    .upload-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: rgba(102, 126, 234, 0.8);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .upload-text {
        color: #e2e8f0;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Caption display */
    .caption-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .caption-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .caption-text {
        color: white;
        font-size: 1.6rem;
        font-weight: 500;
        text-align: center;
        line-height: 1.8;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Image display */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 2rem 0;
    }
    
    /* Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.6);
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #a0aec0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Info box */
    .info-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .info-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .info-text {
        color: #a0aec0;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stFileUploader"] label {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #a0aec0 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Section headers */
    h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Text elements */
    p, span, div {
        color: #a0aec0;
    }
    
    strong {
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load model, tokenizer, and feature extractor."""
    try:
        local_generator = None
        local_extractor = None
        
        try:
            from pickle import load
            from tensorflow.keras.models import load_model
            
            tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
            model = load_model(config.get('paths.model_file'))
            local_extractor = FeatureExtractor()
            
            max_length = config.get('model.max_length', 34)
            beam_width = config.get('inference.beam_width', 3)
            use_beam_search = config.get('inference.use_beam_search', True)
            
            local_generator = CaptionGenerator(
                model=model,
                tokenizer=tokenizer,
                max_length=max_length,
                beam_width=beam_width,
                use_beam_search=use_beam_search
            )
            logger.info("Local models loaded successfully")
        except Exception as e:
            logger.warning(f"Local models not available: {e}")
        
        hybrid_captioner = HybridCaptioner(
            local_generator=local_generator,
            local_feature_extractor=local_extractor,
            use_external_by_default=True
        )
        
        logger.info("Caption system initialized")
        return hybrid_captioner
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        st.error(f"Error loading models: {e}")
        return None


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="header-title">AI Image Caption Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Transform your images into descriptive captions using advanced AI</p>', unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Supported formats: JPG, JPEG, PNG",
            label_visibility="collapsed"
        )
        
        # Sample images
        st.markdown("---")
        st.markdown("**Or try a sample:**")
        
        sample_cols = st.columns(3)
        sample_images = [
            ('samples/dog.jpg', '🐕 Dog'),
            ('samples/beach.jpg', '🏖️ Beach'),
            ('samples/city.jpg', '🌆 City')
        ]
        
        for idx, (path, label) in enumerate(sample_images):
            with sample_cols[idx]:
                if st.button(label, use_container_width=True):
                    if Path(path).exists():
                        st.session_state['sample_image'] = path
                        st.rerun()
        
        # Info section
        st.markdown("---")
        st.markdown("""
        <div class="info-box">
            <div class="info-title">💡 How it works</div>
            <div class="info-text">
                This application uses the BLIP (Bootstrapping Language-Image Pre-training) model 
                to analyze images and generate natural language descriptions. Upload any image 
                to see AI-powered captioning in action.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <div class="info-title">✨ Best Results</div>
            <div class="info-text">
                • Use clear, well-lit images<br>
                • Ensure high resolution (>500px)<br>
                • Keep subject clearly visible<br>
                • Avoid blurry or dark photos
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Generated Caption")
        
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
                
                # Display image
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Generate button
                if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
                    hybrid_captioner = load_models()
                    
                    if hybrid_captioner:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            status_text.text("🔍 Analyzing image...")
                            progress_bar.progress(30)
                            
                            start_time = time.time()
                            
                            status_text.text("✨ Generating caption...")
                            progress_bar.progress(60)
                            
                            caption, method, metadata = hybrid_captioner.generate(
                                image,
                                use_external=True,
                                num_beams=8
                            )
                            
                            elapsed_time = time.time() - start_time
                            
                            progress_bar.progress(100)
                            status_text.text("✅ Complete!")
                            time.sleep(0.5)
                            progress_bar.empty()
                            status_text.empty()
                            
                            # Display caption
                            st.markdown(f"""
                            <div class="caption-container">
                                <p class="caption-text">"{caption}"</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Metrics
                            st.markdown("---")
                            metric_cols = st.columns(3)
                            
                            with metric_cols[0]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-value">{elapsed_time:.2f}s</div>
                                    <div class="metric-label">Processing Time</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with metric_cols[1]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-value">{len(caption.split())}</div>
                                    <div class="metric-label">Words</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with metric_cols[2]:
                                method_display = "BLIP AI" if method == "external_api" else "Local"
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-value">{method_display}</div>
                                    <div class="metric-label">Model</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            logger.info(f"Generated caption: {caption} (method: {method}, time: {elapsed_time:.2f}s)")
                            
                        except Exception as e:
                            progress_bar.empty()
                            status_text.empty()
                            st.error(f"Error generating caption: {e}")
                            logger.error(f"Caption generation error: {e}")
                
            except Exception as e:
                st.error(f"Error processing image: {e}")
                logger.error(f"Error in main app: {e}")
        else:
            st.markdown("""
            <div class="upload-section">
                <div class="upload-text">👈 Upload an image to get started</div>
                <p style="color: rgba(255,255,255,0.8); margin-top: 1rem;">
                    Select an image from your computer or choose a sample image
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <div class="info-title">🤖 About the AI Model</div>
                <div class="info-text">
                    <strong>BLIP (Salesforce)</strong> - A state-of-the-art vision-language model 
                    trained on millions of image-text pairs. It uses transformer architecture 
                    to understand visual content and generate natural language descriptions.
                </div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
