"""Premium Professional UI - AI Caption Generator"""
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache/transformers'
os.environ['HF_DATASETS_CACHE'] = 'D:/huggingface_cache/datasets'

import streamlit as st
from PIL import Image
import time
from pathlib import Path
from utils.external_captioner import HybridCaptioner

st.set_page_config(page_title="AI Caption Pro", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# Premium Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark Premium Background */
    .stApp {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 20% 30%, rgba(88, 86, 214, 0.2) 0px, transparent 50%),
            radial-gradient(at 80% 70%, rgba(139, 92, 246, 0.2) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(59, 130, 246, 0.15) 0px, transparent 50%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Container */
    .block-container {
        padding: 3rem 4rem !important;
        max-width: 1600px !important;
    }
    
    /* Premium Header */
    .premium-header {
        text-align: center;
        padding: 4rem 0 3rem 0;
        position: relative;
    }
    
    .premium-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(59, 130, 246, 0.2));
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        color: #a78bfa;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .premium-title {
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -3px;
        line-height: 1.1;
    }
    
    .premium-subtitle {
        font-size: 1.4rem;
        color: #94a3b8;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateY(-5px);
        box-shadow: 
            0 30px 80px rgba(139, 92, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-icon {
        font-size: 1.8rem;
        filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.5));
    }
    
    /* Premium Upload Area */
    [data-testid="stFileUploader"] {
        background: rgba(139, 92, 246, 0.05);
        border: 2px dashed rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 3rem 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(139, 92, 246, 0.08);
        border-color: rgba(139, 92, 246, 0.6);
        transform: scale(1.02);
    }
    
    [data-testid="stFileUploader"] label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 10px 30px rgba(139, 92, 246, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 15px 40px rgba(139, 92, 246, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Image Display */
    .image-showcase {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 
            0 25px 70px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .image-showcase:hover {
        transform: scale(1.02);
        box-shadow: 
            0 30px 90px rgba(139, 92, 246, 0.4),
            0 0 0 1px rgba(139, 92, 246, 0.3);
    }
    
    /* Caption Result */
    .caption-showcase {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        border-radius: 24px;
        padding: 3.5rem;
        margin: 2.5rem 0;
        box-shadow: 
            0 25px 70px rgba(139, 92, 246, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .caption-showcase::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .caption-text {
        font-size: 2.2rem;
        font-weight: 600;
        color: white;
        text-align: center;
        line-height: 1.6;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
    }
    
    .caption-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(139, 92, 246, 0.05);
        border-left: 4px solid #8b5cf6;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .info-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.75rem;
    }
    
    .info-text {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.7;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
        background: rgba(139, 92, 246, 0.03);
        border: 2px dashed rgba(139, 92, 246, 0.2);
        border-radius: 24px;
        margin: 2rem 0;
    }
    
    .empty-icon {
        font-size: 6rem;
        opacity: 0.3;
        margin-bottom: 1.5rem;
        filter: grayscale(1);
    }
    
    .empty-title {
        font-size: 1.8rem;
        color: #e2e8f0;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .empty-text {
        font-size: 1.1rem;
        color: #94a3b8;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%);
        border-radius: 10px;
    }
    
    /* Success Message */
    .success-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 16px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
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
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .premium-title {
            font-size: 3rem;
        }
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

@st.cache_resource
def load_ai_model():
    return HybridCaptioner(None, None, True)

def main():
    # Premium Header
    st.markdown("""
    <div class="premium-header fade-in">
        <div class="premium-badge">✨ Powered by AI</div>
        <h1 class="premium-title">AI Caption Pro</h1>
        <p class="premium-subtitle">Transform your images into stunning descriptions using state-of-the-art artificial intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><span class="section-icon">📤</span>Upload Image</div>', unsafe_allow_html=True)
        
        uploaded = st.file_uploader("Choose image", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><span class="section-icon">🖼️</span>Sample Images</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🐕 Dog"):
                st.session_state['img'] = 'samples/dog.jpg'
                st.rerun()
        with c2:
            if st.button("🏖️ Beach"):
                st.session_state['img'] = 'samples/beach.jpg'
                st.rerun()
        with c3:
            if st.button("🌆 City"):
                st.session_state['img'] = 'samples/city.jpg'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box fade-in">
            <div class="info-title">💡 How It Works</div>
            <div class="info-text">
                Our AI uses the <strong>BLIP</strong> model to analyze visual content and generate 
                natural language descriptions. Simply upload an image and let the AI work its magic!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><span class="section-icon">🎯</span>Generated Caption</div>', unsafe_allow_html=True)
        
        img_src = None
        if 'img' in st.session_state and st.session_state['img']:
            img_src = st.session_state['img']
            st.session_state['img'] = None
        elif uploaded:
            img_src = uploaded
        
        if img_src:
            try:
                image = Image.open(img_src)
                
                st.markdown('<div class="image-showcase">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Generate Caption", type="primary"):
                    model = load_ai_model()
                    
                    prog = st.progress(0)
                    stat = st.empty()
                    
                    try:
                        stat.markdown("🔍 **Analyzing image...**")
                        prog.progress(30)
                        time.sleep(0.3)
                        
                        stat.markdown("✨ **Generating caption...**")
                        prog.progress(60)
                        
                        start = time.time()
                        caption, method, meta = model.generate(image, True, num_beams=8, max_length=50)
                        elapsed = time.time() - start
                        
                        prog.progress(100)
                        stat.markdown("✅ **Complete!**")
                        time.sleep(0.5)
                        prog.empty()
                        stat.empty()
                        
                        st.markdown(f"""
                        <div class="caption-showcase">
                            <div class="caption-icon">💬</div>
                            <div class="caption-text">"{caption}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-value">{elapsed:.1f}s</div>
                                <div class="metric-label">Time</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{len(caption.split())}</div>
                                <div class="metric-label">Words</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{len(caption)}</div>
                                <div class="metric-label">Chars</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">BLIP</div>
                                <div class="metric-label">Model</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('<div class="success-badge">✅ Caption Generated Successfully!</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        prog.empty()
                        stat.empty()
                        st.error(f"❌ {str(e)}")
            
            except Exception as e:
                st.error(f"❌ {str(e)}")
        
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🖼️</div>
                <div class="empty-title">No Image Selected</div>
                <div class="empty-text">Upload an image or choose a sample to begin</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
