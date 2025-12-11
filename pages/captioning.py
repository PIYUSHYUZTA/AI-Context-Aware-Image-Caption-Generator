"""Image Captioning Module - Generate captions for images."""
import streamlit as st
from PIL import Image
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
import time
from pathlib import Path
import os

from utils.config import config
from utils.logger import logger
from utils.pretrained_caption import PretrainedCaptioner
from utils.ai_caption_apis import get_captioner


@st.cache_resource
def load_pretrained_model():
    """Load pre-trained ViT-GPT2 model for captioning."""
    try:
        captioner = PretrainedCaptioner()
        logger.info("Pre-trained ViT-GPT2 model loaded successfully")
        return captioner
    except Exception as e:
        logger.error(f"Error loading pre-trained model: {e}")
        return None


def show():
    """Display the image captioning interface."""
    
    st.title("🎨 AI Image Captioning")
    st.markdown("Upload an image and let AI generate a descriptive caption!")
    
    # Settings in sidebar
    with st.sidebar:
        st.subheader("🤖 AI Model Selection")
        
        ai_provider = st.selectbox(
            "Choose AI Provider",
            ["ViT-GPT2 (Free, Offline)", "OpenAI GPT-4 Vision (Best Quality)", "Google Gemini (Free Tier)"],
            help="Select which AI model to use for caption generation"
        )
        
        st.divider()
        
        # API Key inputs based on selection
        if "OpenAI" in ai_provider:
            st.subheader("🔑 OpenAI API Key")
            openai_key = st.text_input(
                "API Key",
                type="password",
                help="Get your API key from https://platform.openai.com/api-keys",
                key="openai_key"
            )
            if not openai_key:
                openai_key = os.getenv('OPENAI_API_KEY')
            
            st.info("💡 Get API key: https://platform.openai.com/api-keys")
            st.warning("⚠️ Cost: ~$0.01 per image")
            
        elif "Gemini" in ai_provider:
            st.subheader("🔑 Google API Key")
            gemini_key = st.text_input(
                "API Key",
                type="password",
                help="Get your API key from https://makersuite.google.com/app/apikey",
                key="gemini_key"
            )
            if not gemini_key:
                gemini_key = os.getenv('GOOGLE_API_KEY')
            
            st.info("💡 Get API key: https://makersuite.google.com/app/apikey")
            st.success("✅ Free tier: 60 requests/minute")
        
        st.divider()
        
        st.subheader("⚙️ Caption Settings")
        
        if "ViT-GPT2" in ai_provider:
            num_captions = st.slider(
                "Number of Captions",
                min_value=1,
                max_value=5,
                value=1,
                help="Generate multiple diverse captions"
            )
            
            max_length = st.slider(
                "Max Caption Length",
                min_value=20,
                max_value=100,
                value=50,
                help="Maximum number of words in caption"
            )
        else:
            st.subheader("⚙️ Caption Options")
            
            num_options = st.slider(
                "Number of Caption Options",
                min_value=3,
                max_value=10,
                value=5,
                help="How many different captions to generate"
            )
        
        st.divider()
        
        st.subheader("📊 Model Info")
        if "ViT-GPT2" in ai_provider:
            st.metric("Model", "ViT-GPT2")
            st.metric("Cost", "Free")
            st.metric("Speed", "Fast (2-5s)")
        elif "OpenAI" in ai_provider:
            st.metric("Model", "GPT-4 Vision")
            st.metric("Cost", "~$0.01/image")
            st.metric("Quality", "Best")
        else:
            st.metric("Model", "Gemini 1.5 Flash")
            st.metric("Cost", "Free Tier")
            st.metric("Quality", "Excellent")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Supported formats: JPG, JPEG, PNG, BMP"
        )
        
        # Sample images
        st.markdown("---")
        st.markdown("**Or try a sample:**")
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
        st.markdown("### 🎯 Generated Caption")
        
        # Check for image
        image_source = None
        if 'sample_image' in st.session_state and st.session_state['sample_image']:
            image_source = st.session_state['sample_image']
            st.session_state['sample_image'] = None
        elif uploaded_file is not None:
            image_source = uploaded_file
        
        if image_source is not None:
            try:
                # Display image
                if isinstance(image_source, str):
                    image = Image.open(image_source)
                else:
                    image = Image.open(image_source)
                
                st.image(image, caption='Input Image', use_container_width=True)
                
                # Generate caption button
                if st.button("🚀 Generate Caption with AI", type="primary", use_container_width=True):
                    
                    try:
                        start_time = time.time()
                        
                        # Use different AI based on selection
                        if "ViT-GPT2" in ai_provider:
                            # Use offline model
                            with st.spinner("🔍 Analyzing image with ViT-GPT2..."):
                                captioner = load_pretrained_model()
                                
                                if captioner:
                                    if num_captions == 1:
                                        caption = captioner.generate_caption(image, max_length=max_length)
                                        captions = [caption]
                                    else:
                                        captions = captioner.generate_multiple_captions(
                                            image, 
                                            num_captions=num_captions,
                                            max_length=max_length
                                        )
                                    hashtags = None
                                else:
                                    st.error("❌ Error loading model")
                                    st.stop()
                        
                        elif "OpenAI" in ai_provider:
                            # Use OpenAI GPT-4 Vision
                            if not openai_key:
                                st.error("❌ Please enter your OpenAI API key in the sidebar")
                                st.stop()
                            
                            with st.spinner("🔍 Analyzing image with GPT-4 Vision..."):
                                captioner = get_captioner("openai", openai_key)
                                captions = captioner.generate_multiple_options(image, num_options=num_options)
                                hashtags = None
                        
                        else:  # Gemini
                            # Use Google Gemini
                            if not gemini_key:
                                st.error("❌ Please enter your Google API key in the sidebar")
                                st.stop()
                            
                            with st.spinner("🔍 Analyzing image with Gemini..."):
                                captioner = get_captioner("gemini", gemini_key)
                                captions = captioner.generate_multiple_options(image, num_options=num_options)
                                hashtags = None
                        
                        elapsed_time = time.time() - start_time
                        
                        # Display results
                        st.success(f"✅ Generated {len(captions)} caption options!")
                        
                        # Show all caption options
                        st.markdown("### 📝 Choose Your Favorite Caption:")
                        
                        for i, caption in enumerate(captions, 1):
                            with st.container():
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                            padding: 1.5rem; border-radius: 10px; color: white; 
                                            font-size: 1.1rem; margin: 1rem 0;">
                                    <strong>Option {i}:</strong><br>{caption}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Copy button for each option
                                col1, col2 = st.columns([4, 1])
                                with col2:
                                    if st.button(f"📋 Copy", key=f"copy_{i}", use_container_width=True):
                                        st.success(f"✅ Option {i} copied!")
                        
                        # Show alternative captions if generated from ViT-GPT2
                        if "ViT-GPT2" in ai_provider and len(captions) > 1:
                            st.info("💡 Tip: Try OpenAI or Gemini for more varied caption options!")
                        
                        # Metrics
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("⏱️ Time", f"{elapsed_time:.2f}s")
                        with col_b:
                            st.metric("📝 Words", len(captions[0].split()))
                        with col_c:
                            model_name = "ViT-GPT2" if "ViT-GPT2" in ai_provider else ("GPT-4" if "OpenAI" in ai_provider else "Gemini")
                            st.metric("🎯 Model", model_name)
                        
                        # Technical details
                        with st.expander("🔍 Technical Details"):
                            st.write(f"**AI Provider:** {ai_provider}")
                            st.write(f"**Processing Time:** {elapsed_time:.3f} seconds")
                            st.write(f"**Captions Generated:** {len(captions)}")
                            if hashtags:
                                st.write(f"**Hashtags:** {hashtags}")
                            
                            if "ViT-GPT2" in ai_provider:
                                st.write(f"**Cost:** Free")
                            elif "OpenAI" in ai_provider:
                                st.write(f"**Estimated Cost:** ~$0.01")
                            else:
                                st.write(f"**Cost:** Free (within limits)")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        logger.error(f"Caption generation error: {e}")
                        
            except Exception as e:
                st.error(f"❌ Error processing image: {e}")
                logger.error(f"Error in captioning: {e}")
        else:
            st.info("👆 Upload an image or select a sample to begin")
            
            with st.expander("📖 How to use"):
                st.markdown("""
                1. Upload an image using the file uploader
                2. Adjust settings in the sidebar (optional)
                3. Click "Generate Caption with AI" to create a description
                4. View accurate, ChatGPT-quality captions!
                
                **Features:**
                - 🌟 Uses state-of-the-art BLIP model
                - 🎯 Trained on millions of images
                - 📝 Generates accurate, natural descriptions
                - 🔄 Can generate multiple diverse captions
                - ⚡ Production-grade quality
                
                **Tips:**
                - Works with any image type
                - Generate multiple captions for variety
                - Adjust max length for shorter/longer descriptions
                """)
