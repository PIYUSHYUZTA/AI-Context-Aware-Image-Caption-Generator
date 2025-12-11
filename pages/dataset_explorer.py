"""Dataset Explorer - Visualize and analyze training data."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from pickle import load
from collections import Counter
import random

from utils.config import config
from utils.logger import logger


def load_descriptions():
    """Load descriptions from file."""
    descriptions = {}
    desc_file = Path('descriptions.txt')
    
    if desc_file.exists():
        with open(desc_file, 'r') as f:
            for line in f:
                tokens = line.strip().split()
                if len(tokens) < 2:
                    continue
                image_id = tokens[0]
                caption = ' '.join(tokens[1:])
                
                if image_id not in descriptions:
                    descriptions[image_id] = []
                descriptions[image_id].append(caption)
    
    return descriptions


def show():
    """Display dataset explorer."""
    
    st.title("📈 Dataset Explorer")
    st.markdown("Explore and analyze the training dataset, vocabulary, and statistics")
    
    # Load data
    descriptions = load_descriptions()
    
    if not descriptions:
        st.warning("⚠️ No dataset found. Please run preprocessing first.")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "🔤 Word Analysis",
        "📝 Caption Browser",
        "📈 Visualizations"
    ])
    
    with tab1:
        show_overview(descriptions)
    
    with tab2:
        show_word_analysis(descriptions)
    
    with tab3:
        show_caption_browser(descriptions)
    
    with tab4:
        show_visualizations(descriptions)


def show_overview(descriptions):
    """Show dataset overview."""
    st.subheader("📊 Dataset Overview")
    
    # Calculate statistics
    total_images = len(descriptions)
    total_captions = sum(len(caps) for caps in descriptions.values())
    all_captions = [cap for caps in descriptions.values() for cap in caps]
    
    # Word statistics
    all_words = []
    for caption in all_captions:
        all_words.extend(caption.split())
    
    unique_words = len(set(all_words))
    total_words = len(all_words)
    avg_words_per_caption = total_words / total_captions if total_captions > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📷 Total Images", f"{total_images:,}")
    with col2:
        st.metric("📝 Total Captions", f"{total_captions:,}")
    with col3:
        st.metric("🔤 Unique Words", f"{unique_words:,}")
    with col4:
        st.metric("📊 Avg Words/Caption", f"{avg_words_per_caption:.1f}")
    
    st.divider()
    
    # Caption length distribution
    st.subheader("📏 Caption Length Distribution")
    
    caption_lengths = [len(cap.split()) for cap in all_captions]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.histogram(
            x=caption_lengths,
            nbins=20,
            title='Distribution of Caption Lengths',
            labels={'x': 'Number of Words', 'y': 'Frequency'},
            color_discrete_sequence=['#667eea']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Statistics")
        stats = {
            'Metric': ['Min', 'Max', 'Mean', 'Median', 'Std Dev'],
            'Value': [
                f"{np.min(caption_lengths)} words",
                f"{np.max(caption_lengths)} words",
                f"{np.mean(caption_lengths):.2f} words",
                f"{np.median(caption_lengths):.0f} words",
                f"{np.std(caption_lengths):.2f} words"
            ]
        }
        st.dataframe(pd.DataFrame(stats), hide_index=True, use_container_width=True)
    
    st.divider()
    
    # Captions per image
    st.subheader("📸 Captions per Image")
    
    captions_per_image = [len(caps) for caps in descriptions.values()]
    
    fig = px.histogram(
        x=captions_per_image,
        title='Distribution of Captions per Image',
        labels={'x': 'Number of Captions', 'y': 'Number of Images'},
        color_discrete_sequence=['#764ba2']
    )
    st.plotly_chart(fig, use_container_width=True)


def show_word_analysis(descriptions):
    """Show word analysis."""
    st.subheader("🔤 Word Analysis")
    
    # Get all words
    all_captions = [cap for caps in descriptions.values() for cap in caps]
    all_words = []
    for caption in all_captions:
        all_words.extend(caption.split())
    
    # Word frequency
    word_freq = Counter(all_words)
    most_common = word_freq.most_common(50)
    
    # Display top words
    st.markdown("### 📊 Top 30 Most Frequent Words")
    
    top_30 = most_common[:30]
    df = pd.DataFrame(top_30, columns=['Word', 'Frequency'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            df,
            x='Word',
            y='Frequency',
            title='Word Frequency Distribution',
            color='Frequency',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🔝 Top 10")
        for i, (word, freq) in enumerate(top_30[:10], 1):
            st.markdown(f"{i}. **{word}**: {freq:,}")
    
    st.divider()
    
    # Word cloud data
    st.markdown("### ☁️ Word Cloud Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Words", f"{len(all_words):,}")
    with col2:
        st.metric("Unique Words", f"{len(word_freq):,}")
    with col3:
        st.metric("Vocabulary Diversity", f"{len(word_freq)/len(all_words):.2%}")
    
    # Show full frequency table
    with st.expander("📋 View Full Word Frequency Table"):
        full_df = pd.DataFrame(most_common, columns=['Word', 'Frequency'])
        st.dataframe(full_df, use_container_width=True, height=400)
    
    st.divider()
    
    # Word length analysis
    st.markdown("### 📏 Word Length Analysis")
    
    word_lengths = [len(word) for word in all_words]
    
    fig = px.histogram(
        x=word_lengths,
        nbins=15,
        title='Distribution of Word Lengths',
        labels={'x': 'Word Length (characters)', 'y': 'Frequency'},
        color_discrete_sequence=['#f093fb']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Word search
    st.divider()
    st.markdown("### 🔍 Word Search")
    
    search_word = st.text_input("Search for a word:", placeholder="e.g., dog, cat, running")
    
    if search_word:
        search_word = search_word.lower()
        if search_word in word_freq:
            count = word_freq[search_word]
            st.success(f"✅ Found '{search_word}' - appears {count:,} times")
            
            # Find example captions
            examples = [cap for cap in all_captions if search_word in cap.lower()][:5]
            
            if examples:
                st.markdown("**Example captions:**")
                for i, ex in enumerate(examples, 1):
                    st.markdown(f"{i}. *{ex}*")
        else:
            st.warning(f"⚠️ Word '{search_word}' not found in dataset")


def show_caption_browser(descriptions):
    """Show caption browser."""
    st.subheader("📝 Caption Browser")
    
    st.markdown("Browse through the dataset captions")
    
    # Random sample button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🎲 Random Sample", use_container_width=True):
            st.session_state['random_samples'] = random.sample(list(descriptions.items()), min(5, len(descriptions)))
    
    with col2:
        num_samples = st.number_input("Number of samples", min_value=1, max_value=20, value=5)
    
    # Display samples
    if 'random_samples' in st.session_state:
        samples = st.session_state['random_samples'][:num_samples]
        
        for image_id, captions in samples:
            with st.container():
                st.markdown(f"### 📷 Image: `{image_id}`")
                
                for i, caption in enumerate(captions, 1):
                    st.markdown(f"{i}. *{caption}*")
                
                st.markdown("---")
    else:
        st.info("👆 Click 'Random Sample' to view captions")
    
    st.divider()
    
    # Search by image ID
    st.markdown("### 🔍 Search by Image ID")
    
    image_ids = list(descriptions.keys())
    selected_id = st.selectbox("Select an image ID:", [""] + image_ids)
    
    if selected_id:
        captions = descriptions[selected_id]
        st.markdown(f"**Image ID**: `{selected_id}`")
        st.markdown(f"**Number of captions**: {len(captions)}")
        
        for i, caption in enumerate(captions, 1):
            st.markdown(f"{i}. *{caption}*")
    
    st.divider()
    
    # Statistics
    st.markdown("### 📊 Caption Statistics")
    
    all_captions = [cap for caps in descriptions.values() for cap in caps]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Captions", len(all_captions))
    with col2:
        avg_length = np.mean([len(cap.split()) for cap in all_captions])
        st.metric("Avg Length", f"{avg_length:.1f} words")
    with col3:
        st.metric("Total Images", len(descriptions))


def show_visualizations(descriptions):
    """Show advanced visualizations."""
    st.subheader("📈 Advanced Visualizations")
    
    all_captions = [cap for caps in descriptions.values() for cap in caps]
    all_words = []
    for caption in all_captions:
        all_words.extend(caption.split())
    
    # Word frequency heatmap
    st.markdown("### 🔥 Word Frequency Heatmap (Top 20)")
    
    word_freq = Counter(all_words)
    top_20 = word_freq.most_common(20)
    
    # Create matrix for heatmap
    words = [w for w, _ in top_20]
    freqs = [f for _, f in top_20]
    
    # Reshape for heatmap (4x5 grid)
    matrix = np.array(freqs[:20]).reshape(4, 5)
    word_matrix = np.array(words[:20]).reshape(4, 5)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        text=word_matrix,
        texttemplate='%{text}<br>%{z}',
        colorscale='Viridis',
        showscale=True
    ))
    fig.update_layout(
        title='Top 20 Words Frequency Heatmap',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Caption length vs word diversity
    st.markdown("### 📊 Caption Length vs Unique Words")
    
    caption_data = []
    for caps in list(descriptions.values())[:100]:  # Sample for performance
        for cap in caps:
            words = cap.split()
            caption_data.append({
                'Length': len(words),
                'Unique Words': len(set(words)),
                'Caption': cap[:50] + '...' if len(cap) > 50 else cap
            })
    
    df = pd.DataFrame(caption_data)
    
    fig = px.scatter(
        df,
        x='Length',
        y='Unique Words',
        title='Caption Length vs Vocabulary Diversity',
        hover_data=['Caption'],
        color='Unique Words',
        color_continuous_scale='Plasma'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Word co-occurrence
    st.markdown("### 🔗 Common Word Pairs")
    
    # Find bigrams
    bigrams = []
    for caption in all_captions:
        words = caption.split()
        for i in range(len(words) - 1):
            bigrams.append(f"{words[i]} {words[i+1]}")
    
    bigram_freq = Counter(bigrams)
    top_bigrams = bigram_freq.most_common(15)
    
    bigram_df = pd.DataFrame(top_bigrams, columns=['Word Pair', 'Frequency'])
    
    fig = px.bar(
        bigram_df,
        x='Frequency',
        y='Word Pair',
        orientation='h',
        title='Top 15 Word Pairs',
        color='Frequency',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)
