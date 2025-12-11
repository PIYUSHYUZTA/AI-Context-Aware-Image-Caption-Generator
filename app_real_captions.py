"""Real AI Image Caption Generator using pre-trained transformer model."""
import streamlit as st
from PIL import Image
import time
from pathlib import Path
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator - Real AI",
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
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d1ecf1;
        border-left: 4px solid #0c5460;
        margin: 1rem 0;
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
def load_caption_model():
    """Load BLIP model for image captioning."""
    try:
        with st.spinner("🚀 Loading AI model (first time may take a minute)..."):
            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            return processor, model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def generate_caption(image, processor, model, max_length=50, num_beams=5):
    """Generate caption for image using BLIP model."""
    try:
        # Process image
        inputs = processor(image, return_tensors="pt")
        
        # Generate caption
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        # Decode caption
        caption = processor.decode(output[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error generating caption: {e}"

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🖼️ AI Image Caption Generator</h1>', 
                unsafe_allow_html=True)
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>✨ Real AI Captions:</strong> Using Salesforce BLIP model - a state-of-the-art image captioning model trained on millions of images!
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Model Configuration")
        num_beams = st.slider(
            "Beam Search Width",
            min_value=1,
            max_value=10,
            value=5,
            help="Higher values produce better captions but are slower"
        )
        
        max_length = st.slider(
            "Maximum Caption Length",
            min_value=20,
            max_value=100,
            value=50,
            help="Maximum number of words in caption"
        )
        
        st.divider()
        
        st.subheader("ℹ️ About")
        st.info("""
        **BLIP Model**
        
        - Trained on 129M images
        - State-of-the-art accuracy
        - Real-time processing
        - Understands complex scenes
        
        This is a REAL AI model that generates accurate captions!
        """)
        
        st.divider()
        
        st.subheader("📊 Model Info")
        st.metric("Model", "BLIP-Base")
        st.metric("Parameters", "~250M")
        st.metric("Training Data", "129M images")
    
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
                else:
                    st.warning("Sample not found. Upload your own image!")
        with sample_col2:
            if st.button("🐕 Dog"):
                if Path('samples/dog.jpg').exists():
                    st.session_state['sample_image'] = 'samples/dog.jpg'
                    st.rerun()
                else:
                    st.warning("Sample not found. Upload your own image!")
        with sample_col3:
            if st.button("🌆 City"):
                if Path('samples/city.jpg').exists():
                    st.session_state['sample_image'] = 'samples/city.jpg'
                    st.rerun()
                else:
                    st.warning("Sample not found. Upload your own image!")
    
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
                if st.button("✨ Generate Real AI Caption", type="primary"):
                    # Load model
                    processor, model = load_caption_model()
                    
                    if processor and model:
                        with st.spinner("🤖 AI is analyzing your image..."):
                            start_time = time.time()
                            
                            # Generate caption
                            caption = generate_caption(
                                image, 
                                processor, 
                                model,
                                max_length=max_length,
                                num_beams=num_beams
                            )
                            
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
                            st.metric("🎯 Model", "BLIP")
                        
                        # Additional info
                        with st.expander("🔍 Technical Details"):
                            st.write(f"**Model:** Salesforce BLIP (Base)")
                            st.write(f"**Beam Search Width:** {num_beams}")
                            st.write(f"**Max Length:** {max_length}")
                            st.write(f"**Processing Time:** {elapsed_time:.2f}s")
                            st.write(f"**Model Size:** ~250M parameters")
                            st.write(f"**Training Data:** 129M images")
                        
                        st.success("✅ This is a REAL AI-generated caption based on the actual image content!")
                    else:
                        st.error("Failed to load model. Please check your internet connection.")
                        
            except Exception as e:
                st.error(f"Error processing image: {e}")
        else:
            st.info("👆 Upload an image to get started!")
            
            with st.expander("📖 How to use"):
                st.markdown("""
                ### Getting Started
                
                1. **Upload an image** - Any JPG, PNG, or BMP file
                2. **Click "Generate Real AI Caption"** - Wait a few seconds
                3. **View your caption** - See what the AI sees!
                
                ### Features
                
                - ✅ **Real AI** - Uses state-of-the-art BLIP model
                - ✅ **Accurate** - Trained on 129M images
                - ✅ **Fast** - Results in 2-5 seconds
                - ✅ **Smart** - Understands complex scenes
                
                ### Tips
                
                - Use clear, well-lit images for best results
                - Higher beam width = better quality (but slower)
                - Try different types of images (people, animals, objects, scenes)
                - The model works best with common objects and scenes
                
                ### Examples
                
                Try uploading images of:
                - 🏖️ Outdoor scenes (beaches, parks, mountains)
                - 🐕 Animals (dogs, cats, birds, wildlife)
                - 👥 People (portraits, groups, activities)
                - 🌆 Urban scenes (buildings, streets, cities)
                - 🍕 Food (meals, dishes, ingredients)
                - 🚗 Vehicles (cars, bikes, planes)
                - 🏠 Indoor scenes (rooms, furniture, objects)
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Powered by Salesforce BLIP Model | Built with Transformers & Streamlit</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
