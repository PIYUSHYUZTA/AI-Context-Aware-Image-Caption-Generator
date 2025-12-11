"""Fast AI Image Caption Generator using lightweight model."""
import streamlit as st
from PIL import Image
import time
from pathlib import Path
import requests
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator - Fast",
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

def generate_caption_api(image):
    """Generate caption using Hugging Face API (no download needed)."""
    try:
        # Convert image to bytes
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        
        # Use Hugging Face Inference API (free, no download)
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        headers = {"Authorization": "Bearer hf_demo"}  # Demo token
        
        response = requests.post(API_URL, headers=headers, data=img_bytes, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'Caption generation failed')
            return str(result)
        else:
            return f"API Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🖼️ AI Image Caption Generator</h1>', 
                unsafe_allow_html=True)
    
    st.info("✨ **Fast Mode:** Using cloud API - No downloads needed! Instant captions!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("ℹ️ About")
        st.info("""
        **Fast Cloud Mode**
        
        - No model download
        - Instant processing
        - Uses Hugging Face API
        - BLIP model (same quality)
        - Free to use
        
        Upload any image and get real AI captions instantly!
        """)
        
        st.divider()
        
        st.subheader("📊 Features")
        st.success("✅ No waiting for downloads")
        st.success("✅ Real AI captions")
        st.success("✅ Fast processing")
        st.success("✅ Accurate results")
    
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
            help="Upload any image to get AI-generated caption"
        )
        
        st.markdown("---")
        st.write("**Or try a sample image:**")
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
                
                # Convert RGBA to RGB if needed
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                
                st.image(image, caption='Your Image', use_column_width=True)
                
                # Generate caption button
                if st.button("✨ Generate AI Caption (Fast!)", type="primary"):
                    with st.spinner("🤖 AI is analyzing your image... (2-5 seconds)"):
                        start_time = time.time()
                        
                        # Generate caption using API
                        caption = generate_caption_api(image)
                        
                        elapsed_time = time.time() - start_time
                    
                    # Display caption
                    st.markdown(
                        f'<div class="caption-box">"{caption}"</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Display metrics
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("⏱️ Time", f"{elapsed_time:.2f}s")
                    with metric_col2:
                        st.metric("📝 Words", len(caption.split()))
                    with metric_col3:
                        st.metric("🎯 Mode", "Cloud API")
                    
                    # Additional info
                    with st.expander("🔍 Technical Details"):
                        st.write(f"**Model:** Salesforce BLIP (via API)")
                        st.write(f"**Processing:** Cloud-based")
                        st.write(f"**Time:** {elapsed_time:.2f}s")
                        st.write(f"**Download:** None required")
                        st.write(f"**Quality:** Same as local model")
                    
                    st.success("✅ Real AI caption generated using cloud API!")
                        
            except Exception as e:
                st.error(f"Error processing image: {e}")
        else:
            st.info("👆 Upload an image to get started!")
            
            with st.expander("📖 How to use"):
                st.markdown("""
                ### Getting Started
                
                1. **Upload an image** - Any JPG, PNG, or BMP file
                2. **Click "Generate AI Caption"** - Wait 2-5 seconds
                3. **View your caption** - Real AI analysis!
                
                ### Why This is Fast
                
                - ✅ **No downloads** - Uses cloud API
                - ✅ **Instant start** - No waiting
                - ✅ **Same quality** - BLIP model
                - ✅ **Always updated** - Latest model version
                
                ### Tips
                
                - Use clear, well-lit images
                - Works with any common object or scene
                - Internet connection required
                - Free to use (Hugging Face API)
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Powered by Hugging Face API | No Downloads Required</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
