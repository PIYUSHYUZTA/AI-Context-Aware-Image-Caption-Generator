"""Modern Professional UI for Image Caption Generator."""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import time
from pathlib import Path
import base64
from io import BytesIO

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator
from utils.external_captioner import HybridCaptioner

st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Professional CSS with Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Dark Theme Background */
    .stApp {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 20% 30%, rgba(88, 86, 214, 0.15) 0px, transparent 50%),
            radial-gradient(at 80% 70%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(59, 130, 246, 0.1) 0px, transparent 50%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Container */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Animated Gradient Header */
    .hero-section {
        text-align: center;
        padding: 3rem 0 4rem 0;
        position: relative;
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite;
        letter-spacing: -3px;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 50px;
        color: #a78bfa;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.2);
    }
    
    /* Section Title */
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-icon {
        font-size: 2rem;
    }
    
    /* Upload Zone */
    .upload-zone {
        background: rgba(102, 126, 234, 0.05);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .upload-zone::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .upload-zone:hover::before {
        left: 100%;
    }
    
    .upload-zone:hover {
        background: rgba(102, 126, 234, 0.08);
        border-color: rgba(102, 126, 234, 0.6);
        transform: scale(1.02);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
    
    .upload-text {
        font-size: 1.3rem;
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .upload-hint {
        font-size: 1rem;
        color: #94a3b8;
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    [data-testid="stFileUploader"] > div {
        background: rgba(102, 126, 234, 0.05);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"] > div:hover {
        background: rgba(102, 126, 234, 0.08);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    [data-testid="stFileUploader"] label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #94a3b8 !important;
    }
    
    /* Sample Buttons */
    .sample-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.6);
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }
    
    /* Primary Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
        padding: 1.2rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Caption Display */
    .caption-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .caption-result::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .caption-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .caption-text {
        font-size: 1.8rem;
        font-weight: 500;
        color: white;
        line-height: 1.6;
        text-align: center;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Image Display */
    .image-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .image-container:hover {
        transform: scale(1.02);
        box-shadow: 0 24px 72px rgba(102, 126, 234, 0.3);
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Info Cards */
    .info-card {
        background: rgba(102, 126, 234, 0.05);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        background: rgba(102, 126, 234, 0.08);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateX(5px);
    }
    
    .info-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-text {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.7;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(102, 126, 234, 0.05);
        border: 2px dashed rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        margin: 2rem 0;
    }
    
    .empty-icon {
        font-size: 5rem;
        opacity: 0.3;
        margin-bottom: 1rem;
    }
    
    .empty-title {
        font-size: 1.5rem;
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .empty-text {
        font-size: 1rem;
        color: #94a3b8;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        
        .sample-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load caption generation models."""
    try:
        local_generator = None
        local_extractor = None
        
        try:
            from pickle import load
            from tensorflow.keras.models import load_model
            
            tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
            model = load_model(config.get('paths.model_file'))
            local_extractor = FeatureExtractor()
            
            local_generator = CaptionGenerator(
                model=model,
                tokenizer=tokenizer,
                max_length=config.get('model.max_length', 34),
                beam_width=config.get('inference.beam_width', 3),
                use_beam_search=config.get('inference.use_beam_search', True)
            )
        except Exception as e:
            logger.warning(f"Local models not available: {e}")
        
        hybrid_captioner = HybridCaptioner(
            local_generator=local_generator,
            local_feature_extractor=local_extractor,
            use_external_by_default=True
        )
        
        return hybrid_captioner
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return None


def main():
    """Main application."""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section fade-in-up">
        <div class="hero-badge">✨ Powered by AI</div>
        <h1 class="hero-title">Image Caption Generator</h1>
        <p class="hero-subtitle">Transform your images into meaningful descriptions using advanced AI technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card fade-in-up">
            <div class="section-title">
                <span class="section-icon">📤</span>
                Upload Image
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sample Images
        st.markdown('<div class="glass-card fade-in-up" style="margin-top: 1.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="section-icon">🖼️</span>Try Samples</div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        samples = [
            ('samples/dog.jpg', '🐕 Dog'),
            ('samples/beach.jpg', '🏖️ Beach'),
            ('samples/city.jpg', '🌆 City')
        ]
        
        for idx, (path, label) in enumerate(samples):
            with cols[idx]:
                if st.button(label, use_container_width=True):
                    if Path(path).exists():
                        st.session_state['sample_image'] = path
                        st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Info Cards
        st.markdown("""
        <div class="info-card fade-in-up" style="margin-top: 1.5rem;">
            <div class="info-title">💡 How It Works</div>
            <div class="info-text">
                Our AI uses the BLIP model to analyze visual content and generate natural language descriptions. 
                Simply upload an image and let the AI do the magic!
            </div>
        </div>
        
        <div class="info-card fade-in-up">
            <div class="info-title">🎯 Best Practices</div>
            <div class="info-text">
                • Use clear, well-lit images<br>
                • Ensure resolution above 500px<br>
                • Keep subject clearly visible<br>
                • Avoid heavily compressed images
            </div>
        </div>
        
        <div class="info-card fade-in-up">
            <div class="info-title">🤖 AI Technology</div>
            <div class="info-text">
                <strong>BLIP</strong> (Bootstrapping Language-Image Pre-training) by Salesforce - 
                A state-of-the-art vision-language model trained on millions of image-text pairs.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card fade-in-up">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><span class="section-icon">🎯</span>Generated Caption</div>', unsafe_allow_html=True)
        
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
                st.markdown('<br>', unsafe_allow_html=True)
                if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
                    hybrid_captioner = load_models()
                    
                    if hybrid_captioner:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            status_text.markdown('<p style="color: #94a3b8; text-align: center;">🔍 Analyzing image...</p>', unsafe_allow_html=True)
                            progress_bar.progress(30)
                            time.sleep(0.3)
                            
                            start_time = time.time()
                            
                            status_text.markdown('<p style="color: #94a3b8; text-align: center;">✨ Generating caption...</p>', unsafe_allow_html=True)
                            progress_bar.progress(60)
                            
                            caption, method, metadata = hybrid_captioner.generate(
                                image,
                                use_external=True,
                                num_beams=8
                            )
                            
                            elapsed_time = time.time() - start_time
                            
                            progress_bar.progress(100)
                            status_text.markdown('<p style="color: #10b981; text-align: center;">✅ Complete!</p>', unsafe_allow_html=True)
                            time.sleep(0.5)
                            progress_bar.empty()
                            status_text.empty()
                            
                            # Display caption
                            st.markdown(f"""
                            <div class="caption-result fade-in-up">
                                <div class="caption-icon">💬</div>
                                <div class="caption-text">"{caption}"</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Metrics
                            st.markdown(f"""
                            <div class="metrics-grid fade-in-up">
                                <div class="metric-card">
                                    <div class="metric-value">{elapsed_time:.2f}s</div>
                                    <div class="metric-label">Processing Time</div>
                                </div>
                                <div class="metric-card">
                                    <div class="metric-value">{len(caption.split())}</div>
                                    <div class="metric-label">Words</div>
                                </div>
                                <div class="metric-card">
                                    <div class="metric-value">BLIP</div>
                                    <div class="metric-label">AI Model</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            logger.info(f"Caption: {caption} ({elapsed_time:.2f}s)")
                            
                        except Exception as e:
                            progress_bar.empty()
                            status_text.empty()
                            st.error(f"❌ Error: {e}")
                            logger.error(f"Error: {e}")
                
            except Exception as e:
                st.error(f"❌ Error processing image: {e}")
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🖼️</div>
                <div class="empty-title">No Image Selected</div>
                <div class="empty-text">Upload an image or select a sample to get started</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
