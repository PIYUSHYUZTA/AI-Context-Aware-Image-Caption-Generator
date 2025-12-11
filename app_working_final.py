"""Working Image Caption Generator with lightweight model."""
import streamlit as st
from PIL import Image
import time
from pathlib import Path
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .caption-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load lightweight ViT-GPT2 model (smaller, faster)."""
    try:
        with st.spinner("🚀 Loading AI model (first time: ~30 seconds)..."):
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

def generate_caption(image, model, feature_extractor, tokenizer, device, max_length=16, num_beams=4):
    """Generate caption for image."""
    try:
        # Preprocess image
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        
        # Generate caption
        with torch.no_grad():
            output_ids = model.generate(
                pixel_values,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        # Decode caption
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption
        
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🖼️ AI Image Caption Generator</h1>', 
                unsafe_allow_html=True)
    
    st.success("✨ **Working Version:** Using ViT-GPT2 model - Fast & Accurate!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        num_beams = st.slider(
            "Beam Search Width",
            min_value=1,
            max_value=8,
            value=4,
            help="Higher = better quality"
        )
        
        max_length = st.slider(
            "Max Caption Length",
            min_value=10,
            max_value=30,
            value=16,
            help="Maximum words"
        )
        
        st.divider()
        
        st.subheader("ℹ️ About")
        st.info("""
        **ViT-GPT2 Model**
        
        - Vision Transformer + GPT2
        - Lightweight & Fast
        - Real AI captions
        - Works offline
        - ~300MB download (first time)
        
        Upload any image!
        """)
        
        st.divider()
        
        st.subheader("📊 Model Info")
        st.metric("Model", "ViT-GPT2")
        st.metric("Size", "~300MB")
        st.metric("Speed", "1-3 sec")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    # Initialize session state
    if 'sample_image' not in st.session_state:
        st.session_state['sample_image'] = None
    
    with col1:
        st.subheader("📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload any image"
        )
        
        st.markdown("---")
        st.write("**Or try a sample:**")
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        
        with sample_col1:
            if st.button("🏖️ Beach"):
                if Path('samples/beach.jpg').exists():
                    st.session_state['sample_image'] = 'samples/beach.jpg'
                    st.rerun()
        with sample_col2:
            if st.button("🐕 Dog"):
                if Path('samples/dog.jpg').exists():
                    st.session_state['sample_image'] = 'samples/dog.jpg'
                    st.rerun()
        with sample_col3:
            if st.button("🌆 City"):
                if Path('samples/city.jpg').exists():
                    st.session_state['sample_image'] = 'samples/city.jpg'
                    st.rerun()
    
    with col2:
        st.subheader("🎯 Generated Caption")
        
        # Check for image source
        image_source = None
        
        if st.session_state['sample_image']:
            image_source = st.session_state['sample_image']
            st.session_state['sample_image'] = None
        elif uploaded_file is not None:
            image_source = uploaded_file
        
        if image_source is not None:
            try:
                # Load and display image
                if isinstance(image_source, str):
                    image = Image.open(image_source)
                else:
                    image = Image.open(image_source)
                
                # Convert RGBA to RGB
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                
                st.image(image, caption='Your Image', use_column_width=True)
                
                # Generate caption button
                if st.button("✨ Generate Real AI Caption", type="primary"):
                    # Load model
                    model, feature_extractor, tokenizer, device = load_model()
                    
                    if model:
                        with st.spinner("🤖 AI is analyzing..."):
                            start_time = time.time()
                            
                            # Generate caption
                            caption = generate_caption(
                                image,
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
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric("⏱️ Time", f"{elapsed_time:.2f}s")
                        with metric_col2:
                            st.metric("📝 Words", len(caption.split()))
                        with metric_col3:
                            st.metric("🎯 Model", "ViT-GPT2")
                        
                        # Details
                        with st.expander("🔍 Technical Details"):
                            st.write(f"**Model:** ViT-GPT2")
                            st.write(f"**Beam Width:** {num_beams}")
                            st.write(f"**Max Length:** {max_length}")
                            st.write(f"**Time:** {elapsed_time:.2f}s")
                            st.write(f"**Device:** {'GPU' if torch.cuda.is_available() else 'CPU'}")
                        
                        st.success("✅ Real AI caption generated!")
                    else:
                        st.error("Failed to load model")
                        
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("👆 Upload an image to get started!")
            
            with st.expander("📖 How to use"):
                st.markdown("""
                ### Quick Start
                
                1. **Upload image** - Any photo
                2. **Click button** - Generate caption
                3. **Wait 1-3 seconds** - Get result!
                
                ### First Time
                
                - Model downloads (~300MB)
                - Takes 30-60 seconds
                - Only happens once
                - Then it's fast!
                
                ### Tips
                
                - Clear images work best
                - Any common object/scene
                - Adjust beam width for quality
                - Works offline after download
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Powered by ViT-GPT2 | Real AI Captions</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
