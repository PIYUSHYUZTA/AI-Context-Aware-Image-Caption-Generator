"""Evaluation Center - Evaluate caption quality with metrics."""
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from pickle import load
from tensorflow.keras.models import load_model
import time

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


def calculate_bleu_score(reference, candidate):
    """Calculate simple BLEU-1 score."""
    ref_words = set(reference.lower().split())
    cand_words = candidate.lower().split()
    
    if not cand_words:
        return 0.0
    
    matches = sum(1 for word in cand_words if word in ref_words)
    precision = matches / len(cand_words)
    
    # Brevity penalty
    bp = 1.0 if len(cand_words) >= len(ref_words) else np.exp(1 - len(ref_words) / len(cand_words))
    
    return bp * precision


def calculate_metrics(reference, generated):
    """Calculate evaluation metrics."""
    ref_words = reference.lower().split()
    gen_words = generated.lower().split()
    
    # BLEU-1 score
    bleu1 = calculate_bleu_score(reference, generated)
    
    # Word overlap
    ref_set = set(ref_words)
    gen_set = set(gen_words)
    overlap = len(ref_set & gen_set) / len(ref_set | gen_set) if ref_set | gen_set else 0
    
    # Length ratio
    length_ratio = len(gen_words) / len(ref_words) if ref_words else 0
    
    # Exact match
    exact_match = 1.0 if reference.lower() == generated.lower() else 0.0
    
    return {
        'BLEU-1': bleu1,
        'Word Overlap': overlap,
        'Length Ratio': length_ratio,
        'Exact Match': exact_match
    }


def show():
    """Display evaluation center."""
    
    st.title("🎯 Evaluation Center")
    st.markdown("Evaluate caption quality with standard metrics")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Single Evaluation",
        "📈 Batch Evaluation",
        "📚 Metrics Guide"
    ])
    
    with tab1:
        show_single_evaluation()
    
    with tab2:
        show_batch_evaluation()
    
    with tab3:
        show_metrics_guide()


def show_single_evaluation():
    """Single image evaluation."""
    st.subheader("📊 Single Image Evaluation")
    
    st.markdown("Evaluate a single image caption against reference captions")
    
    # Load models
    model, tokenizer, feature_extractor = load_models()
    
    if not all([model, tokenizer, feature_extractor]):
        st.error("❌ Error loading models")
        return
    
    # Image upload
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=['jpg', 'jpeg', 'png', 'bmp']
        )
    
    with col2:
        st.markdown("**Sample:**")
        if st.button("🐕 Use Dog Sample"):
            if Path('samples/dog.jpg').exists():
                st.session_state['eval_image'] = 'samples/dog.jpg'
                st.rerun()
    
    # Get image
    image_source = None
    if 'eval_image' in st.session_state and st.session_state['eval_image']:
        image_source = st.session_state['eval_image']
        st.session_state['eval_image'] = None
    elif uploaded_file is not None:
        image_source = uploaded_file
    
    if image_source is not None:
        try:
            # Load image
            if isinstance(image_source, str):
                image = Image.open(image_source)
            else:
                image = Image.open(image_source)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption='Input Image', use_container_width=True)
            
            with col2:
                # Reference captions
                st.markdown("### 📝 Reference Captions")
                
                num_refs = st.number_input("Number of references", min_value=1, max_value=5, value=1)
                
                references = []
                for i in range(num_refs):
                    ref = st.text_input(f"Reference {i+1}", key=f"ref_{i}", 
                                       placeholder="Enter reference caption...")
                    if ref:
                        references.append(ref)
            
            # Generate caption
            if st.button("🚀 Generate & Evaluate", type="primary", use_container_width=True):
                
                # Settings
                use_beam = st.session_state.get('use_beam_eval', True)
                beam_width = st.session_state.get('beam_width_eval', 3)
                
                with st.spinner("Generating caption..."):
                    # Extract features
                    features = feature_extractor.extract_from_pil(image)
                    
                    # Generate caption
                    generator = CaptionGenerator(
                        model=model,
                        tokenizer=tokenizer,
                        max_length=config.get('model.max_length', 34),
                        beam_width=beam_width,
                        use_beam_search=use_beam
                    )
                    
                    start_time = time.time()
                    generated = generator.generate(features)
                    elapsed = time.time() - start_time
                
                st.success("✅ Caption generated!")
                
                # Display generated caption
                st.markdown("### 🎯 Generated Caption")
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; 
                            font-size: 1.2rem; text-align: center;">
                    "{generated}"
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("⏱️ Generation Time", f"{elapsed:.3f}s")
                
                # Evaluate against references
                if references:
                    st.divider()
                    st.markdown("### 📊 Evaluation Metrics")
                    
                    # Calculate metrics for each reference
                    all_metrics = []
                    for i, ref in enumerate(references):
                        metrics = calculate_metrics(ref, generated)
                        metrics['Reference'] = f"Ref {i+1}"
                        all_metrics.append(metrics)
                    
                    # Display metrics
                    df = pd.DataFrame(all_metrics)
                    
                    # Average metrics
                    avg_metrics = {
                        'Reference': 'Average',
                        'BLEU-1': df['BLEU-1'].mean(),
                        'Word Overlap': df['Word Overlap'].mean(),
                        'Length Ratio': df['Length Ratio'].mean(),
                        'Exact Match': df['Exact Match'].mean()
                    }
                    
                    df = pd.concat([df, pd.DataFrame([avg_metrics])], ignore_index=True)
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Visualize metrics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = px.bar(
                            df[df['Reference'] != 'Average'],
                            x='Reference',
                            y='BLEU-1',
                            title='BLEU-1 Score by Reference',
                            color='BLEU-1',
                            color_continuous_scale='Viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(
                            df[df['Reference'] != 'Average'],
                            x='Reference',
                            y='Word Overlap',
                            title='Word Overlap by Reference',
                            color='Word Overlap',
                            color_continuous_scale='Plasma'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Overall score
                    overall_score = (avg_metrics['BLEU-1'] + avg_metrics['Word Overlap']) / 2
                    
                    st.markdown("### 🏆 Overall Quality Score")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("BLEU-1", f"{avg_metrics['BLEU-1']:.3f}")
                    with col2:
                        st.metric("Word Overlap", f"{avg_metrics['Word Overlap']:.3f}")
                    with col3:
                        st.metric("Overall Score", f"{overall_score:.3f}")
                    
                    # Quality assessment
                    if overall_score >= 0.7:
                        st.success("🌟 Excellent caption quality!")
                    elif overall_score >= 0.5:
                        st.info("👍 Good caption quality")
                    elif overall_score >= 0.3:
                        st.warning("⚠️ Moderate caption quality")
                    else:
                        st.error("❌ Low caption quality")
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
            logger.error(f"Error in evaluation: {e}")
    
    else:
        st.info("👆 Upload an image to start evaluation")
        
        # Settings
        with st.expander("⚙️ Generation Settings"):
            st.checkbox("Use Beam Search", value=True, key='use_beam_eval')
            st.slider("Beam Width", 1, 10, 3, key='beam_width_eval')


def show_batch_evaluation():
    """Batch evaluation interface."""
    st.subheader("📈 Batch Evaluation")
    
    st.info("🚧 Batch evaluation feature coming soon!")
    
    st.markdown("""
    This feature will allow you to:
    
    - Upload multiple images at once
    - Provide reference captions for each
    - Generate captions for all images
    - Calculate aggregate metrics
    - Export results to CSV
    - Visualize performance distribution
    
    **Stay tuned!**
    """)
    
    # Mock data for demonstration
    st.divider()
    st.markdown("### 📊 Sample Batch Results")
    
    sample_data = {
        'Image': [f'image_{i}.jpg' for i in range(1, 11)],
        'BLEU-1': np.random.uniform(0.4, 0.9, 10),
        'BLEU-4': np.random.uniform(0.2, 0.6, 10),
        'METEOR': np.random.uniform(0.3, 0.7, 10),
        'Word Overlap': np.random.uniform(0.5, 0.9, 10)
    }
    
    df = pd.DataFrame(sample_data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(
            df.melt(id_vars=['Image'], var_name='Metric', value_name='Score'),
            x='Metric',
            y='Score',
            title='Metric Distribution',
            color='Metric'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            df,
            x='Image',
            y=['BLEU-1', 'BLEU-4', 'METEOR'],
            title='Metrics Across Images',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)


def show_metrics_guide():
    """Show metrics guide."""
    st.subheader("📚 Evaluation Metrics Guide")
    
    st.markdown("""
    Understanding the metrics used to evaluate caption quality.
    """)
    
    # BLEU
    with st.expander("🔹 BLEU Score", expanded=True):
        st.markdown("""
        **BLEU (Bilingual Evaluation Understudy)**
        
        Measures n-gram overlap between generated and reference captions.
        
        **Formula:**
        ```
        BLEU = BP × exp(Σ wn × log(pn))
        ```
        
        Where:
        - BP = Brevity Penalty
        - pn = n-gram precision
        - wn = weights (usually uniform)
        
        **Range**: 0 to 1 (higher is better)
        
        **Interpretation:**
        - 0.7 - 1.0: Excellent
        - 0.5 - 0.7: Good
        - 0.3 - 0.5: Moderate
        - 0.0 - 0.3: Poor
        
        **Pros**: Standard metric, easy to compute
        **Cons**: Doesn't capture semantics
        """)
    
    # Word Overlap
    with st.expander("🔹 Word Overlap"):
        st.markdown("""
        **Word Overlap (Jaccard Similarity)**
        
        Measures the ratio of common words between captions.
        
        **Formula:**
        ```
        Overlap = |A ∩ B| / |A ∪ B|
        ```
        
        Where A and B are sets of words.
        
        **Range**: 0 to 1 (higher is better)
        
        **Example:**
        - Reference: "a dog playing in park"
        - Generated: "a dog running in garden"
        - Common: {a, dog, in}
        - Union: {a, dog, playing, running, in, park, garden}
        - Overlap: 3/7 = 0.43
        
        **Pros**: Simple, intuitive
        **Cons**: Ignores word order
        """)
    
    # Length Ratio
    with st.expander("🔹 Length Ratio"):
        st.markdown("""
        **Length Ratio**
        
        Compares the length of generated caption to reference.
        
        **Formula:**
        ```
        Ratio = len(generated) / len(reference)
        ```
        
        **Interpretation:**
        - 1.0: Same length
        - < 1.0: Shorter than reference
        - > 1.0: Longer than reference
        
        **Ideal**: Close to 1.0
        
        **Note**: Used as part of brevity penalty in BLEU
        """)
    
    # Comparison table
    st.divider()
    st.markdown("### 📊 Metrics Comparison")
    
    comparison = {
        'Metric': ['BLEU-1', 'BLEU-4', 'METEOR', 'CIDEr', 'Word Overlap'],
        'Focus': ['Unigrams', '4-grams', 'Semantics', 'Consensus', 'Vocabulary'],
        'Range': ['0-1', '0-1', '0-1', '0-10', '0-1'],
        'Speed': ['Fast', 'Fast', 'Medium', 'Slow', 'Fast'],
        'Best For': ['Quick eval', 'Phrase match', 'Meaning', 'Multiple refs', 'Simple check']
    }
    
    st.dataframe(pd.DataFrame(comparison), use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Tips
    st.markdown("### 💡 Evaluation Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Best Practices:**
        
        - Use multiple reference captions
        - Combine multiple metrics
        - Consider human evaluation
        - Test on diverse images
        - Compare with baselines
        """)
    
    with col2:
        st.markdown("""
        **Common Pitfalls:**
        
        - Relying on single metric
        - Ignoring semantic meaning
        - Not considering context
        - Overfitting to metrics
        - Ignoring edge cases
        """)
