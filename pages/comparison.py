"""Model Comparison Lab - Compare different models and strategies."""
import streamlit as st
from PIL import Image
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
import time
from pathlib import Path
import pandas as pd

from utils.config import config
from utils.logger import logger
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator


@st.cache_resource
def load_models():
    """Load model components."""
    try:
        tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
        model = load_model(config.get('paths.model_file'))
        feature_extractor = FeatureExtractor()
        return model, tokenizer, feature_extractor
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return None, None, None


def show():
    """Display model comparison interface."""
    
    st.title("🔬 Model Comparison Lab")
    st.markdown("Compare different caption generation strategies side-by-side")
    
    # Load models
    model, tokenizer, feature_extractor = load_models()
    
    if not all([model, tokenizer, feature_extractor]):
        st.error("❌ Error loading models. Please check model files.")
        return
    
    st.divider()
    
    # Image upload
    st.subheader("📤 Upload Image for Comparison")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png', 'bmp']
        )
    
    with col2:
        st.markdown("**Or use sample:**")
        if st.button("🐕 Dog Sample"):
            if Path('samples/dog.jpg').exists():
                st.session_state['comparison_image'] = 'samples/dog.jpg'
                st.rerun()
    
    # Get image
    image_source = None
    if 'comparison_image' in st.session_state and st.session_state['comparison_image']:
        image_source = st.session_state['comparison_image']
        st.session_state['comparison_image'] = None
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
            st.image(image, caption='Input Image', width=400)
            
            st.divider()
            
            # Comparison settings
            st.subheader("⚙️ Comparison Settings")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                compare_greedy = st.checkbox("Greedy Search", value=True)
            with col2:
                compare_beam3 = st.checkbox("Beam Search (k=3)", value=True)
            with col3:
                compare_beam5 = st.checkbox("Beam Search (k=5)", value=True)
            
            # Run comparison
            if st.button("🚀 Run Comparison", type="primary", use_container_width=True):
                
                # Extract features once
                with st.spinner("🔍 Extracting image features..."):
                    features = feature_extractor.extract_from_pil(image)
                
                results = []
                
                # Greedy search
                if compare_greedy:
                    with st.spinner("Running Greedy Search..."):
                        generator = CaptionGenerator(
                            model=model,
                            tokenizer=tokenizer,
                            max_length=config.get('model.max_length', 34),
                            beam_width=1,
                            use_beam_search=False
                        )
                        start_time = time.time()
                        caption = generator.generate(features)
                        elapsed = time.time() - start_time
                        
                        results.append({
                            'Method': 'Greedy Search',
                            'Caption': caption,
                            'Time (s)': elapsed,
                            'Words': len(caption.split()),
                            'Beam Width': 1
                        })
                
                # Beam search k=3
                if compare_beam3:
                    with st.spinner("Running Beam Search (k=3)..."):
                        generator = CaptionGenerator(
                            model=model,
                            tokenizer=tokenizer,
                            max_length=config.get('model.max_length', 34),
                            beam_width=3,
                            use_beam_search=True
                        )
                        start_time = time.time()
                        caption = generator.generate(features)
                        elapsed = time.time() - start_time
                        
                        results.append({
                            'Method': 'Beam Search (k=3)',
                            'Caption': caption,
                            'Time (s)': elapsed,
                            'Words': len(caption.split()),
                            'Beam Width': 3
                        })
                
                # Beam search k=5
                if compare_beam5:
                    with st.spinner("Running Beam Search (k=5)..."):
                        generator = CaptionGenerator(
                            model=model,
                            tokenizer=tokenizer,
                            max_length=config.get('model.max_length', 34),
                            beam_width=5,
                            use_beam_search=True
                        )
                        start_time = time.time()
                        caption = generator.generate(features)
                        elapsed = time.time() - start_time
                        
                        results.append({
                            'Method': 'Beam Search (k=5)',
                            'Caption': caption,
                            'Time (s)': elapsed,
                            'Words': len(caption.split()),
                            'Beam Width': 5
                        })
                
                # Display results
                st.success("✅ Comparison complete!")
                
                st.divider()
                
                st.subheader("📊 Comparison Results")
                
                # Display each result
                for i, result in enumerate(results):
                    with st.container():
                        st.markdown(f"### {result['Method']}")
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        padding: 1.5rem; border-radius: 10px; color: white; 
                                        font-size: 1.2rem; margin: 0.5rem 0;">
                                "{result['Caption']}"
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.metric("⏱️ Time", f"{result['Time (s)']:.3f}s")
                            st.metric("📝 Words", result['Words'])
                        
                        if i < len(results) - 1:
                            st.markdown("---")
                
                st.divider()
                
                # Comparison table
                st.subheader("📈 Performance Comparison")
                
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Analysis
                st.subheader("🔍 Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ⚡ Speed Ranking")
                    speed_sorted = sorted(results, key=lambda x: x['Time (s)'])
                    for i, r in enumerate(speed_sorted, 1):
                        st.markdown(f"{i}. **{r['Method']}**: {r['Time (s)']:.3f}s")
                
                with col2:
                    st.markdown("### 📝 Caption Length")
                    for r in results:
                        st.markdown(f"**{r['Method']}**: {r['Words']} words")
                
                # Insights
                st.info("""
                💡 **Key Insights:**
                - Greedy search is fastest but may produce simpler captions
                - Beam search explores more possibilities for better quality
                - Higher beam width = better quality but slower generation
                - Trade-off between speed and caption quality
                """)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
            logger.error(f"Error in comparison: {e}")
    
    else:
        st.info("👆 Upload an image to start comparing different generation methods")
        
        # Educational content
        st.divider()
        
        st.subheader("📚 About Generation Strategies")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎲 Greedy Search
            
            **How it works:**
            - Selects the most probable word at each step
            - Fast and simple
            - Single path exploration
            
            **Best for:**
            - Real-time applications
            - Quick previews
            - Resource-constrained environments
            
            **Trade-offs:**
            - May miss better overall captions
            - Can get stuck in local optima
            - Less diverse outputs
            """)
        
        with col2:
            st.markdown("""
            ### 🔍 Beam Search
            
            **How it works:**
            - Maintains k best candidates at each step
            - Explores multiple paths
            - Selects best overall sequence
            
            **Best for:**
            - High-quality captions
            - Offline processing
            - Research and evaluation
            
            **Trade-offs:**
            - Slower than greedy
            - More memory usage
            - Complexity increases with beam width
            """)
        
        st.divider()
        
        st.subheader("🎯 Choosing the Right Strategy")
        
        st.markdown("""
        | Use Case | Recommended Strategy | Reason |
        |----------|---------------------|---------|
        | Real-time app | Greedy Search | Speed is critical |
        | Photo gallery | Beam Search (k=3) | Balance of quality and speed |
        | Research | Beam Search (k=5+) | Maximum quality |
        | Mobile app | Greedy Search | Limited resources |
        | Accessibility tool | Beam Search (k=3) | Quality matters |
        """)
