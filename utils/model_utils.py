"""Model-related utilities."""
import numpy as np
from typing import Optional, List, Tuple
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from utils.logger import logger


def word_for_id(integer: int, tokenizer: Tokenizer) -> Optional[str]:
    """Convert word ID to word string.
    
    Args:
        integer: Word ID
        tokenizer: Fitted tokenizer
        
    Returns:
        Word string or None if not found
    """
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_caption_greedy(
    model,
    tokenizer: Tokenizer,
    photo: np.ndarray,
    max_length: int
) -> str:
    """Generate caption using greedy search (optimized).
    
    Args:
        model: Trained caption model
        tokenizer: Fitted tokenizer
        photo: Image features
        max_length: Maximum caption length
        
    Returns:
        Generated caption string
    """
    in_text = 'startseq'
    endseq_idx = tokenizer.word_index.get('endseq', 0)
    
    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat_idx = np.argmax(yhat)
        word = word_for_id(yhat_idx, tokenizer)
        
        if word is None or word == 'endseq':
            break
        
        in_text += ' ' + word
    
    # Remove startseq from result
    return in_text.replace('startseq', '').strip()


def generate_caption_beam_search(
    model,
    tokenizer: Tokenizer,
    photo: np.ndarray,
    max_length: int,
    beam_width: int = 3
) -> str:
    """Generate caption using beam search (optimized).
    
    Args:
        model: Trained caption model
        tokenizer: Fitted tokenizer
        photo: Image features
        max_length: Maximum caption length
        beam_width: Number of beams to keep
        
    Returns:
        Generated caption string
    """
    # Start with startseq
    start_seq = [tokenizer.word_index.get('startseq', 0)]
    endseq_idx = tokenizer.word_index.get('endseq', 0)
    
    # List of (sequence, score, finished) tuples
    sequences = [[start_seq, 0.0, False]]
    
    for step in range(max_length):
        all_candidates = []
        
        # Collect all active sequences for batch prediction
        active_sequences = []
        active_indices = []
        
        for i, (seq, score, finished) in enumerate(sequences):
            if finished or seq[-1] == endseq_idx:
                # Keep finished sequences as-is
                all_candidates.append([seq, score, True])
            else:
                active_sequences.append(seq)
                active_indices.append(i)
        
        # If all sequences are finished, break early
        if not active_sequences:
            break
        
        # Batch predict for all active sequences
        if active_sequences:
            # Pad all sequences at once
            padded = pad_sequences(active_sequences, maxlen=max_length)
            
            # Batch predict - much faster than individual predictions
            photo_batch = np.repeat(photo, len(active_sequences), axis=0)
            preds = model.predict([photo_batch, padded], verbose=0)
            
            # Process predictions for each active sequence
            for i, (seq, score, _) in enumerate([sequences[idx] for idx in active_indices]):
                pred = preds[i]
                
                # Get top beam_width predictions
                top_indices = np.argsort(pred)[-beam_width:]
                
                for idx in top_indices:
                    candidate_seq = seq + [int(idx)]
                    # Use log probability for better numerical stability
                    candidate_score = score - np.log(pred[idx] + 1e-10)
                    is_finished = (idx == endseq_idx)
                    all_candidates.append([candidate_seq, candidate_score, is_finished])
        
        # Order by score and keep top beam_width
        ordered = sorted(all_candidates, key=lambda x: x[1])
        sequences = ordered[:beam_width]
        
        # Early stopping if all beams are finished
        if all(finished for _, _, finished in sequences):
            break
    
    # Return best sequence
    best_seq = sequences[0][0]
    
    # Convert to words
    caption_words = []
    for idx in best_seq:
        word = word_for_id(idx, tokenizer)
        if word and word not in ['startseq', 'endseq']:
            caption_words.append(word)
    
    return ' '.join(caption_words)


def create_sequences(
    tokenizer: Tokenizer,
    max_length: int,
    descriptions: dict,
    photos: dict,
    vocab_size: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create training sequences from descriptions and photos.
    
    Args:
        tokenizer: Fitted tokenizer
        max_length: Maximum sequence length
        descriptions: Dictionary of descriptions
        photos: Dictionary of photo features
        vocab_size: Vocabulary size
        
    Returns:
        Tuple of (image_features, input_sequences, output_words)
    """
    from tensorflow.keras.utils import to_categorical
    
    X1, X2, y = [], [], []
    
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            seq = tokenizer.texts_to_sequences([desc])[0]
            
            for i in range(1, len(seq)):
                in_seq, out_seq = seq[:i], seq[i]
                in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                
                X1.append(photos[key][0])
                X2.append(in_seq)
                y.append(out_seq)
    
    return np.array(X1), np.array(X2), np.array(y)


class CaptionGenerator:
    """Wrapper class for caption generation."""
    
    def __init__(
        self,
        model,
        tokenizer: Tokenizer,
        max_length: int,
        beam_width: int = 3,
        use_beam_search: bool = True
    ):
        """Initialize caption generator.
        
        Args:
            model: Trained caption model
            tokenizer: Fitted tokenizer
            max_length: Maximum caption length
            beam_width: Beam width for beam search
            use_beam_search: Whether to use beam search
        """
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.beam_width = beam_width
        self.use_beam_search = use_beam_search
    
    def generate(self, photo_features: np.ndarray) -> str:
        """Generate caption for image features.
        
        Args:
            photo_features: Extracted image features
            
        Returns:
            Generated caption
        """
        try:
            if self.use_beam_search:
                caption = generate_caption_beam_search(
                    self.model,
                    self.tokenizer,
                    photo_features,
                    self.max_length,
                    self.beam_width
                )
            else:
                caption = generate_caption_greedy(
                    self.model,
                    self.tokenizer,
                    photo_features,
                    self.max_length
                )
            
            # Clean up caption
            caption = caption.replace('startseq', '').replace('endseq', '').strip()
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return "Error generating caption"
