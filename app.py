"""AI Image Caption Generator - Production Version"""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

import streamlit as st
from PIL import Image
import time
from pathlib import Path
import json
from datetime import datetime

from utils.external_captioner import HybridCaptioner

# Page config
st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="🎨",
    layout="wide"
)

# Initialize session
if 'history' not in st.session_state:
    st.session_state.history = []

# Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        text-align: center;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .caption-box {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .caption-text {
        font-size: 2rem;
        font-weight: 600;
        color: #667eea;
        text-align: center;
        line-height: 1.6;
    }
    
    .metric-box {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: white;
        color: #667eea;
        border: none;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.1);
        border: 2px dashed rgba(255,255,255,0.5);
        border-radius: 20px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"] label {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    h1, h2, h3 { color: white !important; }
    p, span, div { color: rgba(255,255,255,0.9); }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the AI model"""
    return HybridCaptioner(
        local_generator=None,
        local_feature_extractor=None,
        use_external_by_default=True
    )


def main():
    # Header
    st.markdown('<h1 class="main-title">AI Image Caption Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform your images into beautiful descriptions with AI</p>', unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 Upload Your Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['jpg', 'jpeg', 'png'],
            label_visibility="visible"
        )
        
        st.markdown("---")
        st.markdown("### 🖼️ Or Try a Sample")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🐕 Dog", key="dog_btn"):
                if Path('samples/dog.jpg').exists():
                    st.session_state['selected_image'] = 'samples/dog.jpg'
                    st.rerun()
        
        with col_b:
            if st.button("🏖️ Beach", key="beach_btn"):
                if Path('samples/beach.jpg').exists():
                    st.session_state['selected_image'] = 'samples/beach.jpg'
                    st.rerun()
        
        with col_c:
            if st.button("🌆 City", key="city_btn"):
                if Path('samples/city.jpg').exists():
                    st.session_state['selected_image'] = 'samples/city.jpg'
                    st.rerun()
    
    with col2:
        st.markdown("### 🎯 Generated Caption")
        
        # Get image source
        image_source = None
        if 'selected_image' in st.session_state and st.session_state['selected_image']:
            image_source = st.session_state['selected_image']
            st.session_state['selected_image'] = None
        elif uploaded_file is not None:
            image_source = uploaded_file
        
        if image_source is not None:
            try:
                # Load and display image
                if isinstance(image_source, str):
                    image = Image.open(image_source)
                else:
                    image = Image.open(image_source)
                
                st.image(image, use_container_width=True)
                
                st.markdown("")
                
                # Generate button
                if st.button("🚀 Generate Caption", type="primary"):
                    model = load_model()
                    
                    with st.spinner("🔮 AI is analyzing your image..."):
                        try:
                            start_time = time.time()
                            
                            # Generate caption
                            caption, method, metadata = model.generate(
                                image,
                                use_external=True,
                                num_beams=8,
                                max_length=50
                            )
                            
                            elapsed_time = time.time() - start_time
                            
                            # Display caption
                            st.markdown(f"""
                            <div class="caption-box">
                                <div class="caption-text">"{caption}"</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Metrics
                            st.markdown("---")
                            m1, m2, m3, m4 = st.columns(4)
                            
                            with m1:
                                st.markdown(f"""
                                <div class="metric-box">
                                    <div class="metric-value">{elapsed_time:.1f}s</div>
                                    <div class="metric-label">Time</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with m2:
                                st.markdown(f"""
                                <div class="metric-box">
                                    <div class="metric-value">{len(caption.split())}</div>
                                    <div class="metric-label">Words</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with m3:
                                st.markdown(f"""
                                <div class="metric-box">
                                    <div class="metric-value">{len(caption)}</div>
                                    <div class="metric-label">Characters</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with m4:
                                st.markdown(f"""
                                <div class="metric-box">
                                    <div class="metric-value">BLIP</div>
                                    <div class="metric-label">AI Model</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Save to history
                            st.session_state.history.insert(0, {
                                'caption': caption,
                                'time': elapsed_time,
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            
                            # Success message
                            st.success("✅ Caption generated successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error loading image: {str(e)}")
        
        else:
            st.info("👈 Upload an image or select a sample to get started")
    
    # History section
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 Recent History")
        
        for idx, item in enumerate(st.session_state.history[:5]):
            with st.expander(f"🕐 {item['timestamp']}"):
                st.write(f"**Caption:** {item['caption']}")
                st.write(f"**Time:** {item['time']:.2f}s")


if __name__ == "__main__":
    main()
