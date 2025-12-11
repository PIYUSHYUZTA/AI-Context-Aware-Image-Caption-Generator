"""Professional AI Image Caption Generator - Production Ready"""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

import streamlit as st
from PIL import Image
import time
from pathlib import Path
from utils.external_captioner import HybridCaptioner

st.set_page_config(page_title="AI Caption Generator", page_icon="🎨", layout="wide")

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        letter-spacing: -2px;
    }
    
    .main-subtitle {
        font-size: 1.4rem;
        color: rgba(255,255,255,0.95);
        font-weight: 400;
    }
    
    .content-card {
        background: white;
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
    }
    
    .caption-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .caption-text {
        font-size: 2rem;
        font-weight: 600;
        color: white;
        text-align: center;
        line-height: 1.7;
    }
    
    .metric-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: #f7fafc;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
    }
    
    .sample-btn {
        background: white;
        border: 2px solid #e2e8f0;
        color: #2d3748;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .sample-btn:hover {
        border-color: #667eea;
        color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
    }
    
    .image-display {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        margin: 1.5rem 0;
    }
    
    [data-testid="stFileUploader"] {
        background: #f7fafc;
        border: 2px dashed #cbd5e0;
        border-radius: 16px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: #edf2f7;
    }
    
    [data-testid="stFileUploader"] label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .success-message {
        background: #48bb78;
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

@st.cache_resource
def load_caption_model():
    """Load AI model once and cache it"""
    return HybridCaptioner(
        local_generator=None,
        local_feature_extractor=None,
        use_external_by_default=True
    )

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">AI Image Caption Generator</h1>
        <p class="main-subtitle">Transform your images into beautiful descriptions using advanced AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📤 Upload Image</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image file (JPG, PNG)",
            type=['jpg', 'jpeg', 'png']
        )
        
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2d3748; font-size: 1.2rem; margin-bottom: 1rem;">🖼️ Or Try Sample Images</h3>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("🐕 Dog"):
                st.session_state['sample'] = 'samples/dog.jpg'
                st.rerun()
        
        with c2:
            if st.button("🏖️ Beach"):
                st.session_state['sample'] = 'samples/beach.jpg'
                st.rerun()
        
        with c3:
            if st.button("🌆 City"):
                st.session_state['sample'] = 'samples/city.jpg'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Info box
        st.markdown("""
        <div class="content-card" style="margin-top: 1.5rem;">
            <h3 style="color: #2d3748; font-size: 1.2rem; margin-bottom: 1rem;">💡 How It Works</h3>
            <p style="color: #4a5568; line-height: 1.7;">
                This application uses the <strong>BLIP</strong> (Bootstrapping Language-Image Pre-training) 
                model from Salesforce to analyze images and generate natural language descriptions. 
                Simply upload an image or select a sample to see AI in action!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">🎯 Generated Caption</h2>', unsafe_allow_html=True)
        
        # Get image
        img_source = None
        if 'sample' in st.session_state and st.session_state['sample']:
            img_source = st.session_state['sample']
            st.session_state['sample'] = None
        elif uploaded_file:
            img_source = uploaded_file
        
        if img_source:
            try:
                # Load image
                image = Image.open(img_source)
                
                # Display image
                st.markdown('<div class="image-display">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Generate button
                if st.button("🚀 Generate Caption", type="primary"):
                    model = load_caption_model()
                    
                    progress = st.progress(0)
                    status = st.empty()
                    
                    try:
                        status.markdown("🔍 **Analyzing image...**")
                        progress.progress(30)
                        time.sleep(0.3)
                        
                        status.markdown("✨ **Generating caption with AI...**")
                        progress.progress(60)
                        
                        start = time.time()
                        
                        # Generate caption
                        caption, method, metadata = model.generate(
                            image,
                            use_external=True,
                            num_beams=8,
                            max_length=50
                        )
                        
                        elapsed = time.time() - start
                        
                        progress.progress(100)
                        status.markdown("✅ **Complete!**")
                        time.sleep(0.5)
                        
                        progress.empty()
                        status.empty()
                        
                        # Display caption
                        st.markdown(f"""
                        <div class="caption-result">
                            <div class="caption-text">"{caption}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Metrics
                        st.markdown(f"""
                        <div class="metric-container">
                            <div class="metric-card">
                                <div class="metric-value">{elapsed:.1f}s</div>
                                <div class="metric-label">Processing Time</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{len(caption.split())}</div>
                                <div class="metric-label">Words</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{len(caption)}</div>
                                <div class="metric-label">Characters</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">BLIP</div>
                                <div class="metric-label">AI Model</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('<div class="success-message">✅ Caption generated successfully!</div>', unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.history.insert(0, {
                            'caption': caption,
                            'time': elapsed
                        })
                        
                    except Exception as e:
                        progress.empty()
                        status.empty()
                        st.error(f"❌ Error: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error loading image: {str(e)}")
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; background: #f7fafc; border-radius: 16px; border: 2px dashed #cbd5e0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🖼️</div>
                <h3 style="color: #2d3748; margin-bottom: 0.5rem;">No Image Selected</h3>
                <p style="color: #718096;">Upload an image or select a sample to get started</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # History
    if st.session_state.history:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📜 Recent History</h2>', unsafe_allow_html=True)
        
        for idx, item in enumerate(st.session_state.history[:5]):
            with st.expander(f"Caption #{idx + 1} - {item['time']:.2f}s"):
                st.write(f"**{item['caption']}**")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
