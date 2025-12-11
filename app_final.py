"""Final Production-Ready AI Caption Generator."""
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
import pandas as pd

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator
from utils.external_captioner import HybridCaptioner

st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_processed' not in st.session_state:
    st.session_state.total_processed = 0

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d1b4e 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Header */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Caption Box */
    .caption-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .caption-text {
        font-size: 1.8rem;
        font-weight: 500;
        color: white;
        text-align: center;
        line-height: 1.8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
    }
    
    /* Image */
    .image-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        text-transform: uppercase;
    }
    
    /* Text colors */
    p, span, div, label {
        color: #94a3b8;
    }
    
    h1, h2, h3 {
        color: #e2e8f0 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load AI models."""
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


def save_to_history(caption, elapsed_time, method):
    """Save caption to history."""
    st.session_state.history.insert(0, {
        'caption': caption,
        'time': elapsed_time,
        'method': method,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.session_state.total_processed += 1
    
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]


def main():
    """Main application."""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        use_external = st.radio(
            "AI Model",
            ["BLIP (Best Quality)", "Local Model (Fast)"],
            index=0
        ) == "BLIP (Best Quality)"
        
        with st.expander("🔧 Advanced"):
            beam_width = st.slider("Beam Width", 1, 10, 8)
            max_length = st.slider("Max Length", 20, 100, 50)
        
        st.divider()
        
        st.markdown("### 📊 Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Processed", st.session_state.total_processed)
        with col2:
            st.metric("History", len(st.session_state.history))
        
        st.divider()
        
        st.markdown("### 📜 History")
        if st.session_state.history:
            for item in st.session_state.history[:5]:
                with st.expander(f"🕐 {item['timestamp']}"):
                    st.write(f"**Caption:** {item['caption']}")
                    st.write(f"**Time:** {item['time']:.2f}s")
            
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.session_state.total_processed = 0
                st.rerun()
        else:
            st.info("No history yet")
    
    # Main content
    st.markdown('<h1 class="main-title">AI Caption Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Transform images into descriptions with AI</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📸 Single Image", "📁 Batch Process", "📈 Analytics"])
    
    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("### Upload Image")
            uploaded_file = st.file_uploader(
                "Choose image",
                type=['jpg', 'jpeg', 'png'],
                label_visibility="collapsed"
            )
            
            st.markdown("**Or try sample:**")
            cols = st.columns(3)
            samples = [
                ('samples/dog.jpg', '🐕 Dog'),
                ('samples/beach.jpg', '🏖️ Beach'),
                ('samples/city.jpg', '🌆 City')
            ]
            
            for idx, (path, label) in enumerate(samples):
                with cols[idx]:
                    if st.button(label, key=f"s{idx}"):
                        if Path(path).exists():
                            st.session_state['sample'] = path
                            st.rerun()
        
        with col2:
            st.markdown("### Generated Caption")
            
            img_src = None
            if 'sample' in st.session_state and st.session_state['sample']:
                img_src = st.session_state['sample']
                st.session_state['sample'] = None
            elif uploaded_file:
                img_src = uploaded_file
            
            if img_src:
                try:
                    img = Image.open(img_src) if isinstance(img_src, str) else Image.open(img_src)
                    
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(img, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if st.button("🚀 Generate Caption", type="primary"):
                        captioner = load_models()
                        
                        if captioner:
                            with st.spinner("Processing..."):
                                try:
                                    start = time.time()
                                    
                                    caption, method, meta = captioner.generate(
                                        img,
                                        use_external=use_external,
                                        num_beams=beam_width,
                                        max_length=max_length
                                    )
                                    
                                    elapsed = time.time() - start
                                    
                                    st.markdown(f"""
                                    <div class="caption-box">
                                        <div class="caption-text">"{caption}"</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    cols = st.columns(4)
                                    with cols[0]:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <div class="metric-value">{elapsed:.2f}s</div>
                                            <div class="metric-label">Time</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    with cols[1]:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <div class="metric-value">{len(caption.split())}</div>
                                            <div class="metric-label">Words</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    with cols[2]:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <div class="metric-value">{len(caption)}</div>
                                            <div class="metric-label">Chars</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    with cols[3]:
                                        model_name = "BLIP" if method == "external_api" else "Local"
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <div class="metric-value">{model_name}</div>
                                            <div class="metric-label">Model</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    save_to_history(caption, elapsed, method)
                                    
                                    st.code(caption, language=None)
                                    
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                                    logger.error(f"Error: {e}")
                
                except Exception as e:
                    st.error(f"❌ Error loading image: {str(e)}")
            else:
                st.info("👈 Upload an image to start")
    
    with tab2:
        st.markdown("### Batch Processing")
        st.info("Upload multiple images and process them all at once")
        
        files = st.file_uploader(
            "Choose images",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True
        )
        
        if files:
            st.success(f"✅ {len(files)} images uploaded")
            
            if st.button("🚀 Process All", type="primary"):
                captioner = load_models()
                
                if captioner:
                    progress = st.progress(0)
                    results = []
                    
                    for idx, file in enumerate(files):
                        try:
                            img = Image.open(file)
                            start = time.time()
                            
                            caption, method, meta = captioner.generate(
                                img,
                                use_external=use_external,
                                num_beams=beam_width
                            )
                            
                            elapsed = time.time() - start
                            
                            results.append({
                                'Filename': file.name,
                                'Caption': caption,
                                'Time': f"{elapsed:.2f}s",
                                'Words': len(caption.split()),
                                'Model': "BLIP" if method == "external_api" else "Local"
                            })
                            
                            save_to_history(caption, elapsed, method)
                            
                        except Exception as e:
                            results.append({
                                'Filename': file.name,
                                'Caption': f"Error: {str(e)}",
                                'Time': "0s",
                                'Words': 0,
                                'Model': "N/A"
                            })
                        
                        progress.progress((idx + 1) / len(files))
                    
                    progress.empty()
                    
                    st.markdown("### 📊 Results")
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        "results.csv",
                        "text/csv"
                    )
    
    with tab3:
        st.markdown("### Analytics Dashboard")
        
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_time = df['time'].mean()
                st.metric("⏱️ Avg Time", f"{avg_time:.2f}s")
            
            with col2:
                total = len(df)
                st.metric("📊 Total", total)
            
            with col3:
                avg_words = df['caption'].apply(lambda x: len(x.split())).mean()
                st.metric("📝 Avg Words", f"{avg_words:.1f}")
            
            st.divider()
            
            st.markdown("### Recent Captions")
            for item in st.session_state.history[:10]:
                with st.expander(f"🕐 {item['timestamp']}"):
                    st.write(f"**Caption:** {item['caption']}")
                    st.write(f"**Time:** {item['time']:.2f}s")
                    st.write(f"**Model:** {item['method']}")
            
            st.divider()
            
            json_data = json.dumps(st.session_state.history, indent=2)
            st.download_button(
                "📥 Export JSON",
                json_data,
                "history.json",
                "application/json"
            )
        else:
            st.info("No data yet. Process some images!")


if __name__ == "__main__":
    main()
