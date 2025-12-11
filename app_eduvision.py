"""
EduVision AI - Educational Image Analysis Platform
A comprehensive tool for image captioning with analytics, learning modules, and model comparison
"""
import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="EduVision AI - Educational Image Analysis",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .nav-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .nav-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .nav-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .nav-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .nav-desc {
        color: #666;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main navigation page."""
    
    st.markdown('<h1 class="main-header">🎓 EduVision AI Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Educational Image Analysis with AI - Learn, Analyze, Compare</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        
        page = st.radio(
            "Select Module:",
            [
                "🏠 Home",
                "🎨 Image Captioning",
                "📊 Analytics Dashboard", 
                "🎓 Learning Module",
                "🔬 Model Comparison Lab",
                "📈 Dataset Explorer",
                "🎯 Evaluation Center"
            ]
        )
        
        st.divider()
        
        st.subheader("ℹ️ About")
        st.info("""
        **EduVision AI** is an educational platform for understanding and analyzing AI-powered image captioning.
        
        Perfect for:
        - 📚 Learning about AI/ML
        - 🔍 Data Analysis
        - 🎓 Educational Research
        - 📊 Model Evaluation
        """)
    
    # Route to different pages
    if page == "🏠 Home":
        show_home()
    elif page == "🎨 Image Captioning":
        import pages.captioning as captioning
        captioning.show()
    elif page == "📊 Analytics Dashboard":
        import pages.analytics as analytics
        analytics.show()
    elif page == "🎓 Learning Module":
        import pages.learning as learning
        learning.show()
    elif page == "🔬 Model Comparison Lab":
        import pages.comparison as comparison
        comparison.show()
    elif page == "📈 Dataset Explorer":
        import pages.dataset_explorer as dataset_explorer
        dataset_explorer.show()
    elif page == "🎯 Evaluation Center":
        import pages.evaluation as evaluation
        evaluation.show()

def show_home():
    """Show home page with module overview."""
    
    st.markdown("## Welcome to EduVision AI! 👋")
    st.markdown("""
    This platform combines **AI-powered image captioning** with comprehensive **educational tools** 
    for learning, analysis, and research. Perfect for students, educators, and researchers in 
    AI/ML, data analysis, and educational technology.
    """)
    
    st.divider()
    
    # Module cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🎨</div>
            <div class="nav-title">Image Captioning</div>
            <div class="nav-desc">Generate AI-powered captions for your images using deep learning models</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🎓</div>
            <div class="nav-title">Learning Module</div>
            <div class="nav-desc">Interactive tutorials on how AI image captioning works</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">📈</div>
            <div class="nav-title">Dataset Explorer</div>
            <div class="nav-desc">Visualize and analyze training data, vocabulary, and statistics</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">📊</div>
            <div class="nav-title">Analytics Dashboard</div>
            <div class="nav-desc">Comprehensive metrics, visualizations, and performance analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🔬</div>
            <div class="nav-title">Model Comparison Lab</div>
            <div class="nav-desc">Compare different models and generation strategies side-by-side</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🎯</div>
            <div class="nav-title">Evaluation Center</div>
            <div class="nav-desc">Batch evaluation with BLEU, METEOR, and other quality metrics</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick stats
    st.markdown("## 📊 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Modules", "6")
    with col2:
        st.metric("🧠 AI Models", "VGG16 + LSTM")
    with col3:
        st.metric("📚 Features", "15+")
    with col4:
        st.metric("🎓 Educational", "Yes")
    
    st.divider()
    
    # Getting started
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    1. **🎨 Try Image Captioning** - Upload an image and see AI generate captions
    2. **🎓 Learn How It Works** - Understand the technology behind the scenes
    3. **📊 Explore Analytics** - Dive into model performance and data insights
    4. **🔬 Compare Models** - See how different approaches perform
    5. **📈 Analyze Dataset** - Explore the training data and vocabulary
    6. **🎯 Evaluate Results** - Measure caption quality with standard metrics
    """)
    
    st.info("👈 Use the sidebar to navigate between different modules!")

if __name__ == "__main__":
    main()
