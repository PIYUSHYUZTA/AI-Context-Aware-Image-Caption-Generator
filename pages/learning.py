"""Learning Module - Interactive educational content about AI image captioning."""
import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objects as go


def show():
    """Display the learning module."""
    
    st.title("🎓 Learning Module: How AI Image Captioning Works")
    st.markdown("Interactive guide to understanding the technology behind AI-powered image captioning")
    
    # Learning sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Introduction",
        "🖼️ Feature Extraction",
        "🧠 Sequence Generation",
        "🔄 Training Process",
        "🎯 Evaluation Metrics"
    ])
    
    with tab1:
        show_introduction()
    
    with tab2:
        show_feature_extraction()
    
    with tab3:
        show_sequence_generation()
    
    with tab4:
        show_training_process()
    
    with tab5:
        show_evaluation_metrics()


def show_introduction():
    """Introduction to image captioning."""
    st.header("📚 What is Image Captioning?")
    
    st.markdown("""
    **Image captioning** is the task of generating a natural language description of an image. 
    It combines **Computer Vision** and **Natural Language Processing** to understand what's 
    in an image and describe it in human-readable text.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Why is it Important?
        
        - **Accessibility**: Helps visually impaired users understand images
        - **Content Organization**: Auto-tags images for search and retrieval
        - **Education**: Assists in creating educational content
        - **Social Media**: Generates descriptions for posts
        - **Medical Imaging**: Describes medical scans and X-rays
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Key Technologies
        
        - **Deep Learning**: Neural networks that learn from data
        - **Computer Vision**: Understanding visual content
        - **NLP**: Generating natural language
        - **Transfer Learning**: Using pre-trained models
        - **Sequence Models**: Generating word sequences
        """)
    
    st.divider()
    
    st.header("🏗️ System Architecture")
    
    st.markdown("""
    Our image captioning system consists of two main components:
    """)
    
    # Architecture diagram
    col1, col2, col3 = st.columns([1, 0.5, 1])
    
    with col1:
        st.markdown("""
        ### 1️⃣ Encoder (VGG16)
        
        **Purpose**: Extract visual features from images
        
        - Pre-trained on ImageNet (1.4M images)
        - Converts image to 4096-dim vector
        - Captures visual patterns and objects
        - Transfer learning approach
        
        **Input**: 224×224×3 RGB image  
        **Output**: 4096-dimensional feature vector
        """)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 3rem; padding-top: 3rem;">
        ➡️
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        ### 2️⃣ Decoder (LSTM)
        
        **Purpose**: Generate caption from features
        
        - Processes features + word sequence
        - Generates one word at a time
        - Uses attention mechanism
        - Learns language patterns
        
        **Input**: Features + previous words  
        **Output**: Next word prediction
        """)
    
    st.divider()
    
    st.header("🔄 How It Works: Step by Step")
    
    steps = [
        ("1️⃣ Image Input", "User uploads an image (e.g., a dog playing in a park)"),
        ("2️⃣ Preprocessing", "Image is resized to 224×224 and normalized"),
        ("3️⃣ Feature Extraction", "VGG16 extracts visual features (4096 numbers)"),
        ("4️⃣ Caption Start", "System starts with 'startseq' token"),
        ("5️⃣ Word Generation", "LSTM predicts next word based on features + previous words"),
        ("6️⃣ Repeat", "Process repeats until 'endseq' or max length reached"),
        ("7️⃣ Output", "Final caption: 'a dog playing in the park'")
    ]
    
    for step, description in steps:
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**{step}**")
            with col2:
                st.markdown(description)
    
    st.divider()
    
    st.header("💡 Key Concepts")
    
    with st.expander("🔹 What is Transfer Learning?"):
        st.markdown("""
        **Transfer Learning** means using a model trained on one task for another related task.
        
        - VGG16 was trained on ImageNet (classifying 1000 object categories)
        - We use its learned features for caption generation
        - Saves training time and improves performance
        - Like using knowledge from one subject to learn another
        """)
    
    with st.expander("🔹 What is an LSTM?"):
        st.markdown("""
        **LSTM (Long Short-Term Memory)** is a type of neural network good at sequences.
        
        - Remembers important information from earlier in the sequence
        - Forgets irrelevant information
        - Perfect for language generation
        - Can handle long-term dependencies
        
        Example: When generating "a dog is running in the", LSTM remembers "dog" to predict "park"
        """)
    
    with st.expander("🔹 What is Beam Search?"):
        st.markdown("""
        **Beam Search** is a strategy for generating better captions.
        
        - Instead of picking the single best word each time (greedy)
        - Keeps track of multiple possible sequences (beams)
        - Explores different caption possibilities
        - Selects the overall best caption at the end
        
        **Beam Width = 3** means keeping 3 best candidates at each step
        """)


def show_feature_extraction():
    """Explain feature extraction."""
    st.header("🖼️ Feature Extraction with VGG16")
    
    st.markdown("""
    The first step in image captioning is converting an image into a numerical representation 
    that the model can understand. This is called **feature extraction**.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ VGG16 Architecture
        
        VGG16 is a deep convolutional neural network with:
        
        - **16 layers** (13 conv + 3 fully connected)
        - **138 million parameters**
        - Trained on **ImageNet** dataset
        - Excellent at recognizing visual patterns
        
        **Layer Structure:**
        1. Convolutional blocks (extract features)
        2. Max pooling (reduce dimensions)
        3. Fully connected layers (combine features)
        4. Output: 4096-dimensional vector
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 What Features Are Extracted?
        
        The network learns hierarchical features:
        
        - **Early layers**: Edges, colors, textures
        - **Middle layers**: Shapes, patterns, parts
        - **Deep layers**: Objects, scenes, concepts
        
        **Example for "dog in park":**
        - Edges of dog's body
        - Fur texture
        - Dog shape
        - Grass patterns
        - Park scene context
        """)
    
    st.divider()
    
    st.header("📊 Feature Vector Visualization")
    
    st.markdown("""
    The 4096-dimensional feature vector is too large to visualize directly, but we can 
    understand it as a list of numbers representing different aspects of the image.
    """)
    
    # Simulate feature vector
    np.random.seed(42)
    features = np.random.randn(100)  # Show first 100 dimensions
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(100)),
        y=features,
        marker_color=['#667eea' if f > 0 else '#f093fb' for f in features]
    ))
    fig.update_layout(
        title='Sample Feature Vector (First 100 dimensions)',
        xaxis_title='Feature Dimension',
        yaxis_title='Activation Value',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    💡 **Understanding the visualization:**
    - Each bar represents one dimension of the feature vector
    - Positive values (blue) indicate presence of certain features
    - Negative values (pink) indicate absence
    - The actual vector has 4096 dimensions!
    """)
    
    st.divider()
    
    st.header("🎯 Why Use Pre-trained VGG16?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ Advantages
        
        - **Saves time**: No need to train from scratch
        - **Better performance**: Learned from millions of images
        - **Generalization**: Works well on new images
        - **Proven architecture**: Well-tested and reliable
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Training Comparison
        
        | Approach | Training Time | Performance |
        |----------|--------------|-------------|
        | From scratch | Weeks | Lower |
        | Pre-trained VGG16 | Hours | Higher |
        
        **Result**: 10x faster with better accuracy!
        """)


def show_sequence_generation():
    """Explain sequence generation."""
    st.header("🧠 Sequence Generation with LSTM")
    
    st.markdown("""
    After extracting features, we need to generate a caption word by word. 
    This is where the **LSTM (Long Short-Term Memory)** network comes in.
    """)
    
    st.divider()
    
    st.header("🔄 Step-by-Step Caption Generation")
    
    st.markdown("Let's see how the model generates: **'a dog playing in the park'**")
    
    # Interactive step-by-step
    step = st.slider("Generation Step", 0, 6, 0)
    
    steps_data = [
        ("Start", "startseq", "Initialize with start token", ""),
        ("Step 1", "startseq", "Predict first word", "a"),
        ("Step 2", "startseq a", "Predict second word", "dog"),
        ("Step 3", "startseq a dog", "Predict third word", "playing"),
        ("Step 4", "startseq a dog playing", "Predict fourth word", "in"),
        ("Step 5", "startseq a dog playing in", "Predict fifth word", "the"),
        ("Step 6", "startseq a dog playing in the", "Predict sixth word", "park")
    ]
    
    current_step = steps_data[step]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {current_step[0]}")
        st.markdown(f"**Input Sequence**: `{current_step[1]}`")
        st.markdown(f"**Action**: {current_step[2]}")
        if current_step[3]:
            st.success(f"**Predicted Word**: {current_step[3]}")
    
    with col2:
        st.markdown("### 📊 Process")
        st.markdown("""
        1. Encode input words
        2. Combine with image features
        3. LSTM processes sequence
        4. Predict next word
        5. Add to sequence
        6. Repeat
        """)
    
    st.divider()
    
    st.header("🎯 Greedy vs Beam Search")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎲 Greedy Search
        
        **Strategy**: Pick the best word at each step
        
        **Pros:**
        - ⚡ Fast (single path)
        - 💻 Low memory usage
        - 🎯 Simple to implement
        
        **Cons:**
        - 🎭 May miss better overall captions
        - 📉 Lower quality
        - 🔒 No exploration
        
        **Best for**: Quick results, real-time applications
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Beam Search
        
        **Strategy**: Keep top-k candidates at each step
        
        **Pros:**
        - 🏆 Better quality captions
        - 🌟 Explores alternatives
        - 📈 Higher accuracy
        
        **Cons:**
        - 🐌 Slower (multiple paths)
        - 💾 More memory
        - ⚙️ More complex
        
        **Best for**: High-quality results, offline processing
        """)
    
    st.divider()
    
    st.header("💡 Interactive Example")
    
    st.markdown("See how beam width affects caption generation:")
    
    beam_width = st.select_slider(
        "Beam Width",
        options=[1, 3, 5, 10],
        value=3
    )
    
    if beam_width == 1:
        st.info("🎲 **Greedy Search**: Fastest but may miss better captions")
        example = "a dog in the grass"
    elif beam_width == 3:
        st.success("🎯 **Beam Search (k=3)**: Good balance of speed and quality")
        example = "a brown dog playing in the park"
    elif beam_width == 5:
        st.success("🌟 **Beam Search (k=5)**: Better quality, slightly slower")
        example = "a brown dog playing with a ball in the park"
    else:
        st.warning("🔍 **Beam Search (k=10)**: Best quality but slowest")
        example = "a happy brown dog playing with a red ball in the sunny park"
    
    st.markdown(f"**Example Caption**: *{example}*")
    
    # Performance comparison
    speeds = {1: 0.15, 3: 0.45, 5: 0.75, 10: 1.5}
    qualities = {1: 7.2, 3: 8.5, 5: 8.8, 10: 9.0}
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏱️ Estimated Time", f"{speeds[beam_width]:.2f}s")
    with col2:
        st.metric("⭐ Quality Score", f"{qualities[beam_width]:.1f}/10")


def show_training_process():
    """Explain the training process."""
    st.header("🔄 Training Process")
    
    st.markdown("""
    Training an image captioning model involves teaching it to predict the next word 
    given an image and previous words. Let's understand how this works!
    """)
    
    st.divider()
    
    st.header("📚 Training Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🖼️ Input Data
        
        Each training example consists of:
        
        1. **Image**: Visual content
        2. **Caption**: Text description
        3. **Sequence**: Words in order
        
        **Example:**
        - Image: [dog photo]
        - Caption: "a dog playing in park"
        - Sequences:
          - startseq → a
          - startseq a → dog
          - startseq a dog → playing
          - ...
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Learning Objective
        
        The model learns to:
        
        1. **Understand images**: Extract meaningful features
        2. **Generate language**: Predict next word
        3. **Combine both**: Use image context for words
        
        **Loss Function:**
        - Categorical cross-entropy
        - Measures prediction error
        - Lower loss = better predictions
        """)
    
    st.divider()
    
    st.header("🔄 Training Loop")
    
    st.markdown("""
    The training process repeats these steps for many epochs:
    """)
    
    steps = [
        ("1️⃣ Forward Pass", "Feed image + words through model", "Get predictions"),
        ("2️⃣ Calculate Loss", "Compare predictions with actual words", "Measure error"),
        ("3️⃣ Backward Pass", "Calculate gradients", "Find how to improve"),
        ("4️⃣ Update Weights", "Adjust model parameters", "Make better predictions"),
        ("5️⃣ Repeat", "Process next batch", "Continue learning")
    ]
    
    for step, action, result in steps:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                st.markdown(f"**{step}**")
            with col2:
                st.markdown(action)
            with col3:
                st.markdown(f"*→ {result}*")
    
    st.divider()
    
    st.header("📊 Training Progress")
    
    # Simulated training curve
    epochs = list(range(1, 21))
    train_loss = [2.5 - (i * 0.1) + np.random.uniform(-0.05, 0.05) for i in epochs]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=epochs,
        y=train_loss,
        mode='lines+markers',
        name='Training Loss',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='Training Loss Over Time',
        xaxis_title='Epoch',
        yaxis_title='Loss',
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    💡 **What this shows:**
    - Loss decreases over time (model is learning!)
    - Early epochs: Rapid improvement
    - Later epochs: Fine-tuning
    - Goal: Minimize loss while avoiding overfitting
    """)
    
    st.divider()
    
    st.header("⚙️ Hyperparameters")
    
    st.markdown("Key settings that affect training:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎛️ Model Parameters
        
        - **Embedding Dimension**: 256
          - Size of word representations
        - **LSTM Units**: 256
          - Memory capacity of LSTM
        - **Dropout Rate**: 0.5
          - Prevents overfitting
        - **Vocabulary Size**: ~5000
          - Number of unique words
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Training Parameters
        
        - **Batch Size**: 32
          - Images processed together
        - **Learning Rate**: 0.001
          - Step size for updates
        - **Epochs**: 20
          - Full passes through data
        - **Optimizer**: Adam
          - Adaptive learning algorithm
        """)


def show_evaluation_metrics():
    """Explain evaluation metrics."""
    st.header("🎯 Evaluation Metrics")
    
    st.markdown("""
    How do we measure if our captions are good? We use several metrics that compare 
    generated captions with human-written reference captions.
    """)
    
    st.divider()
    
    st.header("📊 Common Metrics")
    
    # BLEU Score
    with st.expander("🔹 BLEU Score (Bilingual Evaluation Understudy)", expanded=True):
        st.markdown("""
        **What it measures**: N-gram overlap between generated and reference captions
        
        **How it works:**
        - Compares 1-grams, 2-grams, 3-grams, 4-grams
        - Calculates precision for each n-gram
        - Combines with brevity penalty
        
        **Range**: 0 to 1 (higher is better)
        
        **Example:**
        - Reference: "a dog playing in the park"
        - Generated: "a dog playing in a park"
        - BLEU-4: ~0.85 (very good match!)
        
        **Pros**: Standard metric, easy to compute
        **Cons**: Doesn't capture meaning, favors exact matches
        """)
    
    # METEOR
    with st.expander("🔹 METEOR (Metric for Evaluation of Translation with Explicit ORdering)"):
        st.markdown("""
        **What it measures**: Alignment between generated and reference with synonyms
        
        **How it works:**
        - Considers exact matches
        - Includes synonyms and stemming
        - Accounts for word order
        
        **Range**: 0 to 1 (higher is better)
        
        **Example:**
        - Reference: "a dog running quickly"
        - Generated: "a canine sprinting fast"
        - METEOR: Higher than BLEU (recognizes synonyms!)
        
        **Pros**: Better semantic understanding
        **Cons**: More complex to compute
        """)
    
    # CIDEr
    with st.expander("🔹 CIDEr (Consensus-based Image Description Evaluation)"):
        st.markdown("""
        **What it measures**: Consensus with multiple reference captions
        
        **How it works:**
        - Uses TF-IDF weighting
        - Compares with multiple references
        - Emphasizes important words
        
        **Range**: 0 to 10+ (higher is better)
        
        **Example:**
        - References: ["dog in park", "dog playing outside", "canine in garden"]
        - Generated: "dog playing in park"
        - CIDEr: High (matches consensus!)
        
        **Pros**: Designed for image captioning
        **Cons**: Requires multiple references
        """)
    
    # ROUGE
    with st.expander("🔹 ROUGE (Recall-Oriented Understudy for Gisting Evaluation)"):
        st.markdown("""
        **What it measures**: Recall of n-grams and sequences
        
        **How it works:**
        - ROUGE-N: N-gram recall
        - ROUGE-L: Longest common subsequence
        - Focuses on recall vs precision
        
        **Range**: 0 to 1 (higher is better)
        
        **Pros**: Good for longer texts
        **Cons**: May favor longer captions
        """)
    
    st.divider()
    
    st.header("📈 Metric Comparison")
    
    # Sample scores
    metrics_data = {
        'Metric': ['BLEU-1', 'BLEU-4', 'METEOR', 'CIDEr', 'ROUGE-L'],
        'Score': [0.72, 0.35, 0.28, 0.95, 0.56],
        'Range': ['0-1', '0-1', '0-1', '0-10', '0-1']
    }
    
    df = pd.DataFrame(metrics_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Metric'],
            y=df['Score'],
            marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
        ))
        fig.update_layout(
            title='Sample Evaluation Scores',
            xaxis_title='Metric',
            yaxis_title='Score',
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### 📊 Interpretation
        
        **BLEU-1**: Good word overlap
        
        **BLEU-4**: Moderate phrase matching
        
        **METEOR**: Decent semantic match
        
        **CIDEr**: Strong consensus
        
        **ROUGE-L**: Good sequence match
        """)
    
    st.divider()
    
    st.header("💡 Which Metric to Use?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 For Research
        
        Use **multiple metrics**:
        - BLEU-4 (standard)
        - METEOR (semantics)
        - CIDEr (consensus)
        
        Compare with baselines
        """)
    
    with col2:
        st.markdown("""
        ### 🏭 For Production
        
        Focus on **user satisfaction**:
        - Human evaluation
        - A/B testing
        - User feedback
        
        Metrics are guidelines
        """)
    
    with col3:
        st.markdown("""
        ### 🎓 For Learning
        
        Start with **BLEU**:
        - Easy to understand
        - Quick to compute
        - Good baseline
        
        Then explore others
        """)
