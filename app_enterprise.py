"""Enterprise-Grade AI Image Caption Generator with Advanced Features."""
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
    page_title="AI Caption Pro",
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
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
    
    [data-testid="stSidebar"] h1, h2, h3 {
        color: #e2e8f0;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        font-weight: 400;
    }
    
    /* Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Stats */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Caption Display */
    .caption-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .caption-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .caption-text {
        font-size: 1.8rem;
        font-weight: 500;
        color: white;
        text-align: center;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
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
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-text {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* History */
    .history-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .history-caption {
        color: #e2e8f0;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .history-meta {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    
    /* Code block */
    code {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        color: #a78bfa;
    }
    
    /* Hide elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Text colors */
    p, span, div, label {
        color: #94a3b8;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    
    strong {
        color: #e2e8f0;
    }
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
    
    # Keep only last 10
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]


def export_history():
    """Export history as JSON."""
    if st.session_state.history:
        return json.dumps(st.session_state.history, indent=2)
    return None


def main():
    """Main application."""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Model selection
        use_external = st.radio(
            "AI Model",
            ["BLIP (Best Quality)", "Local Model (Fast)"],
            index=0
        ) == "BLIP (Best Quality)"
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            beam_width = st.slider("Beam Width", 1, 10, 8, help="Higher = better quality, slower")
            max_length = st.slider("Max Caption Length", 20, 100, 50)
            temperature = st.slider("Creativity", 0.1, 2.0, 1.0, 0.1)
        
        st.divider()
        
        # Statistics
        st.markdown("### 📊 Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{st.session_state.total_processed}</div>
                <div class="stat-label">Processed</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{len(st.session_state.history)}</div>
                <div class="stat-label">In History</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # History
        st.markdown("### 📜 Recent History")
        if st.session_state.history:
            for item in st.session_state.history[:5]:
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-caption">"{item['caption'][:50]}..."</div>
                    <div class="history-meta">{item['timestamp']} • {item['time']:.2f}s</div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("📥 Export History"):
                export_data = export_history()
                if export_data:
                    st.download_button(
                        "Download JSON",
                        export_data,
                        "caption_history.json",
                        "application/json"
                    )
            
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("No history yet")
        
        st.divider()
        
        # About
        st.markdown("### ℹ️ About")
        st.markdown("""
        **AI Caption Pro** v1.0
        
        Enterprise-grade image captioning powered by state-of-the-art AI models.
        
        **Features:**
        - BLIP AI Model
        - Batch Processing
        - Export Capabilities
        - History Tracking
        - Advanced Settings
        """)
    
    # Main content
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">AI Caption Pro</h1>
        <p class="main-subtitle">Enterprise-Grade Image Caption Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features showcase
    st.markdown("### ✨ Key Features")
    cols = st.columns(4)
    
    features = [
        ("🤖", "AI Powered", "BLIP model with 129M parameters"),
        ("⚡", "Fast Processing", "Generate captions in seconds"),
        ("📊", "Analytics", "Track usage and performance"),
        ("💾", "Export Data", "Download history as JSON")
    ]
    
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Main functionality
    tab1, tab2, tab3 = st.tabs(["📸 Single Image", "📁 Batch Processing", "📈 Analytics"])
    
    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("#### Upload Image")
            uploaded_file = st.file_uploader(
                "Choose an image",
                type=['jpg', 'jpeg', 'png'],
                label_visibility="collapsed"
            )
            
            st.markdown("**Or try a sample:**")
            cols = st.columns(3)
            samples = [
                ('samples/dog.jpg', '🐕 Dog'),
                ('samples/beach.jpg', '🏖️ Beach'),
                ('samples/city.jpg', '🌆 City')
            ]
            
            for idx, (path, label) in enumerate(samples):
                with cols[idx]:
                    if st.button(label, key=f"sample_{idx}"):
                        if Path(path).exists():
                            st.session_state['sample_image'] = path
                            st.rerun()
        
        with col2:
            st.markdown("#### Generated Caption")
            
            image_source = None
            if 'sample_image' in st.session_state and st.session_state['sample_image']:
                image_source = st.session_state['sample_image']
                st.session_state['sample_image'] = None
            elif uploaded_file is not None:
                image_source = uploaded_file
            
            if image_source is not None:
                try:
                    if isinstance(image_source, str):
                        image = Image.open(image_source)
                    else:
                        image = Image.open(image_source)
                    
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(image, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if st.button("🚀 Generate Caption", type="primary"):
                        hybrid_captioner = load_models()
                        
                        if hybrid_captioner:
                            with st.spinner("Processing..."):
                                try:
                                    start_time = time.time()
                                    
                                    caption, method, metadata = hybrid_captioner.generate(
                                        image,
                                        use_external=use_external,
                                        num_beams=beam_width,
                                        max_length=max_length
                                    )
                                    
                                    elapsed_time = time.time() - start_time
                                    
                                    st.markdown(f"""
                                    <div class="caption-box">
                                        <div class="caption-text">"{caption}"</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Metrics
                                    st.markdown(f"""
                                    <div class="metric-grid">
                                        <div class="metric-item">
                                            <div class="metric-number">{elapsed_time:.2f}s</div>
                                            <div class="metric-text">Time</div>
                                        </div>
                                        <div class="metric-item">
                                            <div class="metric-number">{len(caption.split())}</div>
                                            <div class="metric-text">Words</div>
                                        </div>
                                        <div class="metric-item">
                                            <div class="metric-number">{len(caption)}</div>
                                            <div class="metric-text">Characters</div>
                                        </div>
                                        <div class="metric-item">
                                            <div class="metric-number">{"BLIP" if method == "external_api" else "Local"}</div>
                                            <div class="metric-text">Model</div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Save to history
                                    save_to_history(caption, elapsed_time, method)
                                    
                                    # Copy button
                                    st.code(caption, language=None)
                                    
                                except Exception as e:
                                    st.error(f"❌ Error: {e}")
                
                except Exception as e:
                    st.error(f"❌ Error loading image: {e}")
            else:
                st.info("👈 Upload an image to get started")
    
    with tab2:
        st.markdown("#### Batch Processing")
        st.info("🚀 Upload multiple images and process them all at once")
        
        uploaded_files = st.file_uploader(
            "Choose multiple images",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} images uploaded")
            
            if st.button("🚀 Process All Images", type="primary"):
                hybrid_captioner = load_models()
                
                if hybrid_captioner:
                    progress_bar = st.progress(0)
                    results = []
                    
                    for idx, file in enumerate(uploaded_files):
                        try:
                            image = Image.open(file)
                            start_time = time.time()
                            
                            caption, method, metadata = hybrid_captioner.generate(
                                image,
                                use_external=use_external,
                                num_beams=beam_width
                            )
                            
                            elapsed_time = time.time() - start_time
                            
                            results.append({
                                'Filename': file.name,
                                'Caption': caption,
                                'Time (s)': f"{elapsed_time:.2f}",
                                'Words': len(caption.split()),
                                'Model': "BLIP" if method == "external_api" else "Local"
                            })
                            
                            save_to_history(caption, elapsed_time, method)
                            
                        except Exception as e:
                            results.append({
                                'Filename': file.name,
                                'Caption': f"Error: {e}",
                                'Time (s)': "0",
                                'Words': 0,
                                'Model': "N/A"
                            })
                        
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    progress_bar.empty()
                    
                    # Display results
                    st.markdown("### 📊 Results")
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    # Export
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results (CSV)",
                        csv,
                        "batch_results.csv",
                        "text/csv"
                    )
    
    with tab3:
        st.markdown("#### Analytics Dashboard")
        
        if st.session_state.history:
            # Create dataframe
            df = pd.DataFrame(st.session_state.history)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_time = df['time'].mean()
                st.metric("⏱️ Avg Processing Time", f"{avg_time:.2f}s")
            
            with col2:
                total = len(df)
                st.metric("📊 Total Processed", total)
            
            with col3:
                avg_words = df['caption'].apply(lambda x: len(x.split())).mean()
                st.metric("📝 Avg Words", f"{avg_words:.1f}")
            
            st.divider()
            
            # Recent captions
            st.markdown("#### Recent Captions")
            for item in st.session_state.history[:10]:
                with st.expander(f"📝 {item['timestamp']}"):
                    st.write(f"**Caption:** {item['caption']}")
                    st.write(f"**Time:** {item['time']:.2f}s")
                    st.write(f"**Model:** {item['method']}")
        else:
            st.info("No data yet. Process some images to see analytics!")


if __name__ == "__main__":
    main()
