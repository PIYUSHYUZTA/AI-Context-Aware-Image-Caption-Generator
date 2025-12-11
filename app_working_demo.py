"""Working demo app with simulated captions until model is retrained."""
import streamlit as st
from PIL import Image
import numpy as np
import time
from pathlib import Path
import random

# Page configuration
st.set_page_config(
    page_title="AI Image Caption Generator - Demo",
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
    .demo-notice {
        padding: 1rem;
        border-radius: 5px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
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

# Demo captions for different image types
DEMO_CAPTIONS = {
    'default': [
        "a person standing in front of a building",
        "a dog playing in the park",
        "a group of people walking on the street",
        "a child playing with a toy",
        "a cat sitting on a couch",
        "a bird flying in the sky",
        "a car parked on the road",
        "people walking on the beach",
        "a man riding a bicycle",
        "a woman holding an umbrella"
    ],
    'beach': [
        "people walking on the beach",
        "a person standing on the beach",
        "a group of people at the beach",
        "children playing on the beach",
        "a dog running on the beach"
    ],
    'dog': [
        "a dog playing in the park",
        "a dog running through the grass",
        "a dog catching a frisbee",
        "a dog sitting on the ground",
        "a dog playing with a toy"
    ],
    'city': [
        "a person standing in front of a building",
        "people walking on the street",
        "a man walking down the street",
        "a group of people in a city",
        "a person standing near a building"
    ]
}

def get_demo_caption(image_name='default'):
    """Get a demo caption based on image type."""
    for key in DEMO_CAPTIONS:
        if key in image_name.lower():
            return random.choice(DEMO_CAPTIONS[key])
    return random.choice(DEMO_CAPTIONS['default'])

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🖼️ AI Image Caption Generator</h1>', 
                unsafe_allow_html=True)
    
    # Demo notice
    st.markdown("""
    <div class="demo-notice">
        <strong>⚠️ Demo Mode:</strong> This is a demonstration version. The model needs to be retrained with proper data.
        Currently showing example captions. Upload images to see the interface in action!
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Model Configuration")
        use_beam_search = st.checkbox(
            "Use Beam Search",
            value=True,
            help="Beam search produces better captions"
        )
        
        if use_beam_search:
            beam_width = st.slider(
                "Beam Width",
                min_value=1,
                max_value=10,
                value=3
            )
        
        st.divider()
        
        st.subheader("ℹ️ About")
        st.info("""
        **Demo Version**
        
        This app demonstrates the interface and features.
        
        To get real captions:
        1. Prepare dataset (Flickr8k)
        2. Run preprocessing scripts
        3. Train the model
        4. Replace model.h5
        
        See README for details.
        """)
    
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
            help="Supported formats: JPG, JPEG, PNG, BMP"
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
        image_name = 'default'
        
        if st.session_state['sample_image']:
            image_source = st.session_state['sample_image']
            image_name = Path(image_source).stem
            st.session_state['sample_image'] = None
        elif uploaded_file is not None:
            image_source = uploaded_file
            image_name = uploaded_file.name
        
        if image_source is not None:
            try:
                # Load and display image
                if isinstance(image_source, str):
                    image = Image.open(image_source)
                else:
                    image = Image.open(image_source)
                
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                
                st.image(image, caption='Uploaded Image', use_column_width=True)
                
                # Generate caption button
                if st.button("✨ Generate Caption", type="primary"):
                    with st.spinner("🤖 AI is analyzing your image..."):
                        # Simulate processing time
                        start_time = time.time()
                        time.sleep(1.0 + random.uniform(0, 0.5))
                        
                        # Get demo caption
                        caption = get_demo_caption(image_name)
                        elapsed_time = time.time() - start_time
                        
                        # Display caption
                        st.markdown(
                            f'<div class="caption-box">"{caption}"</div>',
                            unsafe_allow_html=True
                        )
                        
                        # Display metrics
                        metric_col1, metric_col2 = st.columns(2)
                        with metric_col1:
                            st.metric("⏱️ Generation Time", f"{elapsed_time:.2f}s")
                        with metric_col2:
                            st.metric("📝 Word Count", len(caption.split()))
                        
                        # Additional info
                        with st.expander("🔍 Technical Details"):
                            st.write(f"**Search Method:** {'Beam Search' if use_beam_search else 'Greedy Search'}")
                            if use_beam_search:
                                st.write(f"**Beam Width:** {beam_width}")
                            st.write(f"**Feature Extraction:** VGG16")
                            st.write(f"**Sequence Model:** LSTM")
                            st.write(f"**Status:** Demo Mode (showing example captions)")
                        
                        st.info("💡 **Note:** This is a demo caption. Train the model with real data for actual AI-generated captions!")
                        
            except Exception as e:
                st.error(f"Error processing image: {e}")
        else:
            st.info("👆 Upload an image to get started!")
            
            with st.expander("📖 How to use"):
                st.markdown("""
                ### Demo Mode Instructions
                
                1. **Upload an image** or click a sample button
                2. **Click "Generate Caption"** to see a demo caption
                3. **View the interface** and features
                
                ### To Get Real Captions
                
                1. **Download Dataset**: Get Flickr8k dataset
                2. **Preprocess Data**: Run preprocessing scripts
                   ```bash
                   python preprocess_captions.py
                   python preprocess_images.py
                   ```
                3. **Train Model**: Train with your data
                   ```bash
                   python train_improved.py
                   ```
                4. **Use Trained Model**: Replace model.h5 and tokenizer.pkl
                
                See **README_PROFESSIONAL.md** for complete instructions.
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Demo Version - Built with TensorFlow, Keras, and Streamlit</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
