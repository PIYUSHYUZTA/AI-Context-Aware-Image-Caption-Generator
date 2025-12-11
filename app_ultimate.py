"""Ultimate AI Image Caption Generator - Feature Rich Version."""
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import time
from pathlib import Path
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import json
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations
st.markdown("""
<style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .caption-box {
        padding: 2rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.4rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .caption-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .feature-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        font-size: 0.9rem;
        margin: 0.3rem;
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .history-item {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'caption_history' not in st.session_state:
    st.session_state.caption_history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'sample_image' not in st.session_state:
    st.session_state.sample_image = None

@st.cache_resource
def load_model():
    """Load ViT-GPT2 model."""
    try:
        with st.spinner("🚀 Loading AI model..."):
            model_name = "nlpconnect/vit-gpt2-image-captioning"
            
            model = VisionEncoderDecoderModel.from_pretrained(model_name)
            feature_extractor = ViTImageProcessor.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            
            return model, feature_extractor, tokenizer, device
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None

def enhance_image(image, brightness=1.0, contrast=1.0, sharpness=1.0):
    """Enhance image quality."""
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)
    return image

def generate_caption(image, model, feature_extractor, tokenizer, device, max_length=16, num_beams=4):
    """Generate caption for image."""
    try:
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        
        with torch.no_grad():
            output_ids = model.generate(
                pixel_values,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main application function."""
    
    # Header with badges
    st.markdown('<h1 class="main-header">🎨 AI Image Caption Generator Pro</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <span class='feature-badge'>🤖 Real AI</span>
        <span class='feature-badge'>⚡ Fast</span>
        <span class='feature-badge'>🎯 Accurate</span>
        <span class='feature-badge'>🎨 Enhanced</span>
        <span class='feature-badge'>📊 Analytics</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Advanced Settings")
        
        # Model settings
        st.subheader("🧠 AI Configuration")
        num_beams = st.slider("Beam Search Width", 1, 8, 4, help="Higher = better quality")
        max_length = st.slider("Max Caption Length", 10, 30, 16, help="Maximum words")
        
        st.divider()
        
        # Image enhancement
        st.subheader("🎨 Image Enhancement")
        enhance = st.checkbox("Enable Enhancement", value=False)
        
        if enhance:
            brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
            contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
            sharpness = st.slider("Sharpness", 0.5, 2.0, 1.0, 0.1)
        else:
            brightness = contrast = sharpness = 1.0
        
        st.divider()
        
        # Statistics
        st.subheader("📊 Session Stats")
        st.metric("Captions Generated", len(st.session_state.caption_history))
        st.metric("Favorites", len(st.session_state.favorites))
        
        if st.session_state.caption_history:
            avg_time = sum(h['time'] for h in st.session_state.caption_history) / len(st.session_state.caption_history)
            st.metric("Avg Time", f"{avg_time:.2f}s")
        
        st.divider()
        
        # About
        st.subheader("ℹ️ About")
        st.info("""
        **ViT-GPT2 Model**
        
        ✅ Vision Transformer
        ✅ GPT-2 Language Model
        ✅ Real-time Processing
        ✅ Offline Capable
        
        Version 2.0 Pro
        """)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📸 Generate", "📜 History", "⭐ Favorites"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Image")
            
            uploaded_file = st.file_uploader(
                "Choose an image...",
                type=['jpg', 'jpeg', 'png', 'bmp'],
                help="Upload any image"
            )
            
            st.markdown("---")
            st.write("**🎯 Quick Test:**")
            sample_col1, sample_col2, sample_col3 = st.columns(3)
            
            with sample_col1:
                if st.button("🏖️ Beach", use_container_width=True):
                    if Path('samples/beach.jpg').exists():
                        st.session_state.sample_image = 'samples/beach.jpg'
                        st.rerun()
            with sample_col2:
                if st.button("🐕 Dog", use_container_width=True):
                    if Path('samples/dog.jpg').exists():
                        st.session_state.sample_image = 'samples/dog.jpg'
                        st.rerun()
            with sample_col3:
                if st.button("🌆 City", use_container_width=True):
                    if Path('samples/city.jpg').exists():
                        st.session_state.sample_image = 'samples/city.jpg'
                        st.rerun()
        
        with col2:
            st.subheader("🎯 AI Caption")
            
            # Check for image
            image_source = None
            if st.session_state.sample_image:
                image_source = st.session_state.sample_image
                st.session_state.sample_image = None
            elif uploaded_file:
                image_source = uploaded_file
            
            if image_source:
                try:
                    # Load image
                    if isinstance(image_source, str):
                        image = Image.open(image_source)
                        image_name = Path(image_source).name
                    else:
                        image = Image.open(image_source)
                        image_name = uploaded_file.name
                    
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    
                    # Apply enhancements
                    display_image = enhance_image(image, brightness, contrast, sharpness) if enhance else image
                    
                    st.image(display_image, caption='Your Image', use_container_width=True)
                    
                    # Generate button
                    if st.button("✨ Generate AI Caption", type="primary", use_container_width=True):
                        model, feature_extractor, tokenizer, device = load_model()
                        
                        if model:
                            with st.spinner("🤖 AI is analyzing your image..."):
                                start_time = time.time()
                                
                                caption = generate_caption(
                                    display_image,
                                    model,
                                    feature_extractor,
                                    tokenizer,
                                    device,
                                    max_length=max_length,
                                    num_beams=num_beams
                                )
                                
                                elapsed_time = time.time() - start_time
                            
                            # Display caption
                            st.markdown(
                                f'<div class="caption-box">"{caption}"</div>',
                                unsafe_allow_html=True
                            )
                            
                            # Metrics
                            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                            with metric_col1:
                                st.markdown('<div class="metric-card"><h3>⏱️</h3><h2>{:.2f}s</h2><p>Time</p></div>'.format(elapsed_time), unsafe_allow_html=True)
                            with metric_col2:
                                st.markdown('<div class="metric-card"><h3>📝</h3><h2>{}</h2><p>Words</p></div>'.format(len(caption.split())), unsafe_allow_html=True)
                            with metric_col3:
                                st.markdown('<div class="metric-card"><h3>🎯</h3><h2>{}</h2><p>Beams</p></div>'.format(num_beams), unsafe_allow_html=True)
                            with metric_col4:
                                st.markdown('<div class="metric-card"><h3>🎨</h3><h2>{}</h2><p>Enhanced</p></div>'.format('Yes' if enhance else 'No'), unsafe_allow_html=True)
                            
                            # Action buttons
                            action_col1, action_col2, action_col3 = st.columns(3)
                            
                            with action_col1:
                                if st.button("⭐ Add to Favorites", use_container_width=True):
                                    st.session_state.favorites.append({
                                        'caption': caption,
                                        'image_name': image_name,
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    st.success("Added to favorites!")
                            
                            with action_col2:
                                # Export JSON
                                export_data = {
                                    'caption': caption,
                                    'image_name': image_name,
                                    'timestamp': datetime.now().isoformat(),
                                    'processing_time': elapsed_time,
                                    'settings': {
                                        'beam_width': num_beams,
                                        'max_length': max_length,
                                        'enhanced': enhance
                                    }
                                }
                                json_str = json.dumps(export_data, indent=2)
                                st.download_button(
                                    "📥 Export JSON",
                                    json_str,
                                    file_name=f"caption_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            with action_col3:
                                if st.button("🔄 Try Again", use_container_width=True):
                                    st.rerun()
                            
                            # Technical details
                            with st.expander("🔍 Technical Details"):
                                st.write(f"**Model:** ViT-GPT2")
                                st.write(f"**Beam Width:** {num_beams}")
                                st.write(f"**Max Length:** {max_length}")
                                st.write(f"**Processing Time:** {elapsed_time:.3f}s")
                                st.write(f"**Device:** {'GPU' if torch.cuda.is_available() else 'CPU'}")
                                st.write(f"**Image Enhancement:** {'Enabled' if enhance else 'Disabled'}")
                                if enhance:
                                    st.write(f"**Brightness:** {brightness}")
                                    st.write(f"**Contrast:** {contrast}")
                                    st.write(f"**Sharpness:** {sharpness}")
                            
                            # Add to history
                            st.session_state.caption_history.append({
                                'caption': caption,
                                'image_name': image_name,
                                'time': elapsed_time,
                                'timestamp': datetime.now().isoformat()
                            })
                            
                            st.success("✅ Caption generated successfully!")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.info("👆 Upload an image or click a sample button to get started!")
                
                with st.expander("📖 Quick Guide"):
                    st.markdown("""
                    ### How to Use
                    
                    1. **Upload** - Click browse or drag & drop
                    2. **Enhance** - Optional image improvements
                    3. **Generate** - Click the button
                    4. **Export** - Save as JSON or add to favorites
                    
                    ### Pro Tips
                    
                    - 🎨 Enable enhancement for low-quality images
                    - ⚡ Lower beam width for faster results
                    - 🎯 Higher beam width for better quality
                    - 📊 Check history tab for past captions
                    """)
    
    with tab2:
        st.subheader("📜 Caption History")
        
        if st.session_state.caption_history:
            if st.button("🗑️ Clear History"):
                st.session_state.caption_history = []
                st.rerun()
            
            st.markdown("---")
            
            for idx, entry in enumerate(reversed(st.session_state.caption_history)):
                st.markdown(f"""
                <div class='history-item'>
                    <strong>#{len(st.session_state.caption_history) - idx} - {entry['image_name']}</strong><br>
                    <em>"{entry['caption']}"</em><br>
                    <small>⏱️ {entry['time']:.2f}s | 🕐 {entry['timestamp'][:19]}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No captions generated yet. Start by uploading an image!")
    
    with tab3:
        st.subheader("⭐ Favorite Captions")
        
        if st.session_state.favorites:
            if st.button("🗑️ Clear Favorites"):
                st.session_state.favorites = []
                st.rerun()
            
            st.markdown("---")
            
            for idx, fav in enumerate(st.session_state.favorites):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div class='history-item'>
                        <strong>⭐ {fav['image_name']}</strong><br>
                        <em>"{fav['caption']}"</em><br>
                        <small>🕐 {fav['timestamp'][:19]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state.favorites.pop(idx)
                        st.rerun()
        else:
            st.info("No favorites yet. Add captions from the Generate tab!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='color: gray; font-size: 0.9rem;'>
            <strong>AI Image Caption Generator Pro v2.0</strong><br>
            Powered by ViT-GPT2 | Built with ❤️ using Transformers & Streamlit<br>
            <span class='feature-badge'>Production Ready</span>
            <span class='feature-badge'>Enterprise Grade</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
