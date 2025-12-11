"""Visualization utilities for model explainability."""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from typing import Optional, Tuple
import io


def create_attention_heatmap(
    image: np.ndarray,
    attention_weights: np.ndarray,
    alpha: float = 0.6
) -> np.ndarray:
    """
    Create attention heatmap overlay on image.
    
    Args:
        image: Original image (H, W, 3)
        attention_weights: Attention weights (H', W')
        alpha: Overlay transparency
        
    Returns:
        Image with attention heatmap overlay
    """
    # Resize attention to match image
    h, w = image.shape[:2]
    attention_resized = cv2.resize(attention_weights, (w, h))
    
    # Normalize attention
    attention_norm = (attention_resized - attention_resized.min()) / (
        attention_resized.max() - attention_resized.min() + 1e-8
    )
    
    # Create heatmap
    heatmap = cv2.applyColorMap(
        (attention_norm * 255).astype(np.uint8),
        cv2.COLORMAP_JET
    )
    
    # Overlay on image
    overlay = cv2.addWeighted(image, 1-alpha, heatmap, alpha, 0)
    
    return overlay


def plot_training_history(
    history: dict,
    save_path: Optional[str] = None
) -> None:
    """
    Plot training history.
    
    Args:
        history: Training history dictionary
        save_path: Path to save plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss plot
    axes[0].plot(history.get('loss', []), label='Training Loss', linewidth=2)
    if 'val_loss' in history:
        axes[0].plot(history['val_loss'], label='Validation Loss', linewidth=2)
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Loss', fontsize=12)
    axes[0].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Accuracy plot
    if 'accuracy' in history:
        axes[1].plot(history['accuracy'], label='Training Accuracy', linewidth=2)
        if 'val_accuracy' in history:
            axes[1].plot(history['val_accuracy'], label='Validation Accuracy', linewidth=2)
        axes[1].set_xlabel('Epoch', fontsize=12)
        axes[1].set_ylabel('Accuracy', fontsize=12)
        axes[1].set_title('Model Accuracy', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_caption_comparison(
    image: np.ndarray,
    captions: dict,
    save_path: Optional[str] = None
) -> None:
    """
    Plot image with multiple caption comparisons.
    
    Args:
        image: Image array
        captions: Dictionary of caption types and texts
        save_path: Path to save plot
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Display image
    ax.imshow(image)
    ax.axis('off')
    
    # Add captions as text
    y_pos = 1.05
    for caption_type, caption_text in captions.items():
        ax.text(
            0.5, y_pos,
            f"{caption_type}: {caption_text}",
            transform=ax.transAxes,
            fontsize=11,
            ha='center',
            va='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )
        y_pos += 0.08
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def create_word_cloud(
    captions: list,
    save_path: Optional[str] = None
) -> None:
    """
    Create word cloud from captions.
    
    Args:
        captions: List of caption strings
        save_path: Path to save word cloud
    """
    try:
        from wordcloud import WordCloud
        
        # Combine all captions
        text = ' '.join(captions)
        
        # Create word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(text)
        
        # Plot
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Caption Word Cloud', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
        
    except ImportError:
        print("wordcloud package not installed. Install with: pip install wordcloud")


def plot_metrics_comparison(
    metrics: dict,
    save_path: Optional[str] = None
) -> None:
    """
    Plot comparison of evaluation metrics.
    
    Args:
        metrics: Dictionary of metric names and values
        save_path: Path to save plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())
    
    # Create bar plot
    bars = ax.bar(metric_names, metric_values, color='steelblue', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{height:.3f}',
            ha='center',
            va='bottom',
            fontsize=10
        )
    
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Evaluation Metrics Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def enhance_image_quality(
    image: np.ndarray,
    apply_clahe: bool = True,
    denoise: bool = True
) -> np.ndarray:
    """
    Enhance image quality for better feature extraction.
    
    Args:
        image: Input image
        apply_clahe: Apply CLAHE for contrast enhancement
        denoise: Apply denoising
        
    Returns:
        Enhanced image
    """
    enhanced = image.copy()
    
    # Convert to LAB color space for CLAHE
    if apply_clahe:
        lab = cv2.cvtColor(enhanced, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge and convert back
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    # Denoise
    if denoise:
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
    
    return enhanced
