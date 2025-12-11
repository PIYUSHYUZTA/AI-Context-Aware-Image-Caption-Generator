"""Enhanced Streamlit application for image caption generation."""
import os

# Set Hugging Face cache to D drive BEFORE importing transformers
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
import time
from pathlib import Path
import io

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor, validate_image
from utils.model_utils import CaptionGenerator
from utils.external_captioner import HybridCaptioner, ExternalCaptioner

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Professional Animations and Effects + GSAP
st.markdown("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated Background with GSAP-ready classes */
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
    
    /* Floating Particles Effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(75, 0, 130, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(147, 51, 234, 0.1) 0%, transparent 50%);
        animation: particleFloat 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleFloat {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, -30px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
    }
    
    /* Main Header with Glow Effect and Entrance Animation */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(167, 139, 250, 0.5);
        animation: titleGlow 3s ease-in-out infinite, headerBounce 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
        letter-spacing: 2px;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 20px rgba(167, 139, 250, 0.6)); }
        50% { filter: brightness(1.2) drop-shadow(0 0 40px rgba(236, 72, 153, 0.8)); }
    }
    
    @keyframes headerBounce {
        0% { transform: translateY(-100px) scale(0.5); opacity: 0; }
        60% { transform: translateY(20px) scale(1.1); opacity: 1; }
        80% { transform: translateY(-10px) scale(0.95); }
        100% { transform: translateY(0) scale(1); }
    }
    
    /* Subtitle with Smooth Slide Animation */
    .subtitle {
        text-align: center;
        color: #c4b5fd;
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 3rem;
        animation: fadeInUp 1.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(50px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Caption Box with Premium GSAP-Ready Design */
    .caption-box {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        color: white;
        font-size: 1.4rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(139, 92, 246, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        animation: slideInScale 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        font-weight: 500;
        line-height: 1.8;
        will-change: transform, opacity;
    }
    
    .caption-box::before {
        content: '✨';
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 2rem;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    .caption-box::after {
        content: '✨';
        position: absolute;
        bottom: 10px;
        right: 10px;
        font-size: 2rem;
        animation: sparkle 2s ease-in-out infinite 1s;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0.3; transform: scale(0.8) rotate(0deg); }
        50% { opacity: 1; transform: scale(1.2) rotate(180deg); }
    }
    
    @keyframes slideInScale {
        from {
            opacity: 0;
            transform: scale(0.8) translateY(30px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    /* Buttons with Smooth GSAP-Enhanced Effects */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        position: relative;
        overflow: hidden;
        cursor: pointer;
        will-change: transform;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 50px rgba(139, 92, 246, 0.7);
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(0.95);
        transition: all 0.1s ease;
    }
    
    /* File Uploader Styling */
    .uploadedFile {
        background: rgba(139, 92, 246, 0.1);
        border: 2px dashed #8b5cf6;
        border-radius: 15px;
        padding: 1rem;
        animation: borderPulse 2s ease-in-out infinite;
    }
    
    @keyframes borderPulse {
        0%, 100% { border-color: #8b5cf6; }
        50% { border-color: #ec4899; }
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d1b4e 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #c4b5fd;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #a78bfa;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Info Box with Glass Effect */
    .info-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(167, 139, 250, 0.3);
        margin: 1rem 0;
        color: #c4b5fd;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
    }
    
    /* Image Container with Glow */
    .stImage {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 
            0 20px 60px rgba(139, 92, 246, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        animation: imageGlow 3s ease-in-out infinite;
    }
    
    @keyframes imageGlow {
        0%, 100% { box-shadow: 0 20px 60px rgba(139, 92, 246, 0.3); }
        50% { box-shadow: 0 20px 60px rgba(236, 72, 153, 0.5); }
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(139, 92, 246, 0.1);
        border-radius: 10px;
        color: #c4b5fd;
        font-weight: 600;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background: rgba(139, 92, 246, 0.15);
        border-left: 4px solid #8b5cf6;
        border-radius: 10px;
        color: #c4b5fd;
    }
    
    /* Spinner Animation */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
        border-right-color: #ec4899 !important;
    }
    
    /* Checkbox and Radio Styling */
    .stCheckbox, .stRadio {
        color: #c4b5fd;
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Divider */
    hr {
        border-color: rgba(139, 92, 246, 0.3);
        margin: 2rem 0;
    }
    
    /* Footer Styling */
    .footer-text {
        text-align: center;
        color: #a78bfa;
        font-size: 0.95rem;
        margin-top: 3rem;
        padding: 1rem;
        animation: fadeIn 2s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* GSAP Animation Classes */
    .gsap-fade-in {
        opacity: 0;
    }
    
    .gsap-slide-up {
        opacity: 0;
        transform: translateY(50px);
    }
    
    .gsap-scale-in {
        opacity: 0;
        transform: scale(0.8);
    }
    
    .gsap-rotate-in {
        opacity: 0;
        transform: rotate(-10deg) scale(0.9);
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Icon Animations */
    .icon-bounce {
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Card Hover Effect */
    .hover-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .hover-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.4);
    }
    
    /* GSAP Animation Classes */
    .gsap-fade-in {
        opacity: 0;
    }
    
    .gsap-slide-up {
        opacity: 0;
        transform: translateY(50px);
    }
    
    .gsap-scale-in {
        opacity: 0;
        transform: scale(0.8);
    }
</style>

<script>
// GSAP Animations - Enhanced UI interactions
document.addEventListener('DOMContentLoaded', function() {
    // Load GSAP if not already loaded
    if (typeof gsap === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js';
        script.onload = initAnimations;
        document.head.appendChild(script);
    } else {
        initAnimations();
    }
    
    function initAnimations() {
        // Animate main header with elastic bounce
        gsap.from('.main-header', {
            duration: 1.2,
            y: -50,
            opacity: 0,
            ease: 'elastic.out(1, 0.5)',
            delay: 0.2
        });
        
        // Animate subtitle
        gsap.from('.subtitle', {
            duration: 1,
            y: 30,
            opacity: 0,
            ease: 'power3.out',
            delay: 0.5
        });
        
        // Watch for caption box and animate it
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('caption-box')) {
                        gsap.from(node, {
                            duration: 0.8,
                            scale: 0.8,
                            opacity: 0,
                            rotation: -5,
                            ease: 'back.out(1.7)',
                            clearProps: 'all'
                        });
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Enhanced button interactions
        document.querySelectorAll('.stButton>button').forEach(button => {
            button.addEventListener('mouseenter', function() {
                gsap.to(this, {
                    duration: 0.3,
                    scale: 1.05,
                    y: -5,
                    boxShadow: '0 20px 50px rgba(139, 92, 246, 0.6)',
                    ease: 'power2.out'
                });
            });
            
            button.addEventListener('mouseleave', function() {
                gsap.to(this, {
                    duration: 0.3,
                    scale: 1,
                    y: 0,
                    boxShadow: '0 10px 30px rgba(99, 102, 241, 0.4)',
                    ease: 'power2.out'
                });
            });
            
            button.addEventListener('click', function() {
                gsap.timeline()
                    .to(this, {
                        duration: 0.1,
                        scale: 0.95,
                        ease: 'power2.in'
                    })
                    .to(this, {
                        duration: 0.3,
                        scale: 1.05,
                        ease: 'elastic.out(1, 0.3)'
                    });
            });
        });
        
        // Animate images when they appear
        const imageObserver = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.tagName === 'IMG' || (node.querySelector && node.querySelector('img'))) {
                        const img = node.tagName === 'IMG' ? node : node.querySelector('img');
                        gsap.from(img, {
                            duration: 0.8,
                            scale: 0.9,
                            opacity: 0,
                            rotation: -5,
                            ease: 'back.out(1.4)',
                            clearProps: 'all'
                        });
                    }
                });
            });
        });
        
        imageObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Animate sidebar
        gsap.from('[data-testid="stSidebar"]', {
            duration: 0.8,
            x: -100,
            opacity: 0,
            ease: 'power3.out',
            delay: 0.3
        });
        
        // Animate metrics when they appear
        const metricsObserver = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.querySelector && node.querySelector('[data-testid="stMetricValue"]')) {
                        const metrics = node.querySelectorAll('[data-testid="stMetricValue"]');
                        metrics.forEach((metric, i) => {
                            gsap.from(metric, {
                                duration: 0.6,
                                scale: 0,
                                opacity: 0,
                                ease: 'back.out(2)',
                                delay: i * 0.1
                            });
                        });
                    }
                });
            });
        });
        
        metricsObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Continuous floating animation for info boxes
        gsap.utils.toArray('.info-box').forEach((box, i) => {
            gsap.to(box, {
                duration: 3 + i,
                y: -10,
                repeat: -1,
                yoyo: true,
                ease: 'sine.inOut',
                delay: i * 0.5
            });
        });
    }
});
</script>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load model, tokenizer, and feature extractor."""
    try:
        with st.spinner("Loading AI models... This may take a moment."):
            # Try to load local models
            local_generator = None
            local_extractor = None
            
            try:
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
            
            # Create hybrid captioner
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
    
    # Header with Icons and Animation
    st.markdown('''
        <h1 class="main-header">✨ AI-Powered Image Caption Generator ✨</h1>
        <p class="subtitle">🎨 Transform Your Images into Beautiful Descriptions with AI Magic 🚀</p>
    ''', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Caption method selection
        st.subheader("🤖 Caption Method")
        caption_method = st.radio(
            "Choose caption generation method:",
            ["External API (BLIP - Best Quality)", "Local Model (Fast)"],
            index=0,
            help="External API provides better captions but requires internet"
        )
        use_external = "External" in caption_method
        
        st.divider()
        
        # Model settings (for local model)
        if not use_external:
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
        else:
            use_beam_search = True
            beam_width = 5
        
        st.divider()
        
        # About section with better styling
        st.subheader("ℹ️ About")
        if use_external:
            st.markdown("""
            <div class="info-box">
                <p>� <nstrong>External API Mode</strong></p>
                <p>🎯 <strong>BLIP Model</strong> - State-of-the-art captioning</p>
                <p>🔮 <strong>Transformer-based</strong> - Advanced AI</p>
                <p>⚡ <strong>High Quality</strong> - Professional results</p>
                <p style="margin-top: 1rem;">📸 Upload an image and watch AI create magic!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <p>🧠 <strong>Local Model Mode</strong></p>
                <p>🎯 <strong>VGG16</strong> - Image feature extraction</p>
                <p>🔮 <strong>LSTM</strong> - Sequence generation</p>
                <p>⚡ <strong>Fast & Private</strong> - No internet needed</p>
                <p style="margin-top: 1rem;">📸 Upload an image and watch AI create magic!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Statistics with icons
        st.subheader("📊 Model Statistics")
        try:
            tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
            vocab_size = len(tokenizer.word_index) + 1
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("📚 Vocabulary", f"{vocab_size:,}")
            with col_b:
                st.metric("📏 Max Length", config.get('model.max_length', 34))
        except:
            pass
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Your Image")
        st.markdown("*Drag and drop or browse to select*")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=config.get('app.supported_formats', ['jpg', 'jpeg', 'png']),
            help="Supported formats: JPG, JPEG, PNG"
        )
        
        # Sample images
        st.markdown("---")
        st.write("Or try a sample image:")
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        
        # Sample images with actual files
        with sample_col1:
            if st.button("🏖️ Beach"):
                if Path('samples/beach.jpg').exists():
                    st.session_state['sample_image'] = 'samples/beach.jpg'
                    st.rerun()
                else:
                    st.warning("Sample image not found. Please upload your own image.")
        with sample_col2:
            if st.button("🐕 Dog"):
                if Path('samples/dog.jpg').exists():
                    st.session_state['sample_image'] = 'samples/dog.jpg'
                    st.rerun()
                else:
                    st.warning("Sample image not found. Please upload your own image.")
        with sample_col3:
            if st.button("🌆 City"):
                if Path('samples/city.jpg').exists():
                    st.session_state['sample_image'] = 'samples/city.jpg'
                    st.rerun()
                else:
                    st.warning("Sample image not found. Please upload your own image.")
    
    with col2:
        st.markdown("### 🎯 AI Generated Caption")
        st.markdown("*Your image description will appear here*")
        
        # Check for sample image
        image_source = None
        if 'sample_image' in st.session_state and st.session_state['sample_image']:
            image_source = st.session_state['sample_image']
            st.session_state['sample_image'] = None  # Clear after use
        elif uploaded_file is not None:
            image_source = uploaded_file
        
        if image_source is not None:
            try:
                # Display image
                if isinstance(image_source, str):
                    # Sample image from file path
                    image = Image.open(image_source)
                else:
                    # Uploaded file
                    image = Image.open(image_source)
                st.image(image, caption='Uploaded Image', use_container_width=True)
                
                # Generate caption button with better text
                if st.button("🚀 Generate Caption with AI", type="primary"):
                    # Load models
                    hybrid_captioner = load_models()
                    
                    if hybrid_captioner:
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # Check if external API is available
                            if use_external and not hybrid_captioner.is_external_available():
                                st.warning("⚠️ External API not available. Installing required packages...")
                                st.info("Run: `pip install transformers torch` to enable external API")
                                use_external_actual = False
                            else:
                                use_external_actual = use_external
                            
                            # Update local model settings if using local
                            if not use_external_actual and hybrid_captioner.local_generator:
                                hybrid_captioner.local_generator.use_beam_search = use_beam_search
                                hybrid_captioner.local_generator.beam_width = beam_width
                            
                            # Generate caption
                            if use_external_actual:
                                status_text.text("🌐 Connecting to external API...")
                                progress_bar.progress(20)
                            else:
                                status_text.text("🔍 Extracting image features...")
                                progress_bar.progress(30)
                            
                            start_time = time.time()
                            
                            status_text.text("✨ Generating caption with AI...")
                            progress_bar.progress(60)
                            
                            caption, method, metadata = hybrid_captioner.generate(
                                image,
                                use_external=use_external_actual,
                                num_beams=beam_width if use_external_actual else None
                            )
                            
                            elapsed_time = time.time() - start_time
                            
                            # Complete
                            progress_bar.progress(100)
                            status_text.text("✅ Caption generated successfully!")
                            time.sleep(0.5)
                            progress_bar.empty()
                            status_text.empty()
                            
                            # Display caption
                            st.markdown(
                                f'<div class="caption-box">"{caption}"</div>',
                                unsafe_allow_html=True
                            )
                            
                            # Display metrics with better layout
                            st.markdown("---")
                            metric_col1, metric_col2, metric_col3 = st.columns(3)
                            with metric_col1:
                                st.metric("⏱️ Time", f"{elapsed_time:.2f}s")
                            with metric_col2:
                                st.metric("📝 Words", len(caption.split()))
                            with metric_col3:
                                method_display = "External API" if method == "external_api" else "Local Model"
                                st.metric("🔧 Method", method_display)
                            
                            # Additional info
                            with st.expander("🔍 Technical Details"):
                                st.write(f"**Generation Method:** {method_display}")
                                if method == "external_api":
                                    st.write(f"**Model:** {metadata.get('model', 'BLIP')}")
                                    st.write(f"**Beam Width:** {metadata.get('num_beams', 5)}")
                                else:
                                    st.write(f"**Search Method:** {'Beam Search' if use_beam_search else 'Greedy Search'}")
                                    if use_beam_search:
                                        st.write(f"**Beam Width:** {beam_width}")
                                    st.write(f"**Vocabulary Size:** {metadata.get('vocab_size', 'N/A')}")
                                    st.write(f"**Feature Extraction:** VGG16")
                                    st.write(f"**Sequence Model:** LSTM")
                            
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
                <div class="info-box" style="text-align: center; padding: 3rem;">
                    <h2 style="color: #c4b5fd;">👆 Upload an Image to Begin</h2>
                    <p style="font-size: 1.1rem; margin-top: 1rem;">
                        🎨 Select an image from the left panel<br>
                        ⚡ Click generate to see AI magic<br>
                        ✨ Get beautiful captions instantly
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Instructions
            with st.expander("📖 How to use"):
                st.markdown("""
                1. **Upload an image** using the file uploader on the left
                2. **Adjust settings** in the sidebar (optional)
                3. **Click "Generate Caption"** to create a description
                4. **View results** including the caption and generation time
                
                **Tips:**
                - Use clear, well-lit images for best results
                - Beam search produces better captions but takes longer
                - Try different beam widths to see variations
                """)
    
    # Footer with animation
    st.markdown("---")
    st.markdown("""
        <div class="footer-text">
            <p style="font-size: 1.1rem; font-weight: 500;">
                ✨ Built with ❤️ using TensorFlow, Keras, and Streamlit ✨
            </p>
            <p style="margin-top: 0.5rem; opacity: 0.8;">
                🚀 Powered by Deep Learning | 🎨 Designed for Excellence | ⚡ Fast & Accurate
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
