"""Tests for utility functions."""
import pytest
import numpy as np
from PIL import Image
from utils.image_utils import FeatureExtractor, validate_image
from utils.model_utils import word_for_id
from utils.advanced_metrics import meteor_score, rouge_l_score, semantic_similarity


def test_feature_extractor_singleton():
    """Test FeatureExtractor is singleton."""
    extractor1 = FeatureExtractor()
    extractor2 = FeatureExtractor()
    assert extractor1 is extractor2


def test_feature_extraction_from_pil():
    """Test feature extraction from PIL image."""
    extractor = FeatureExtractor()
    img = Image.new('RGB', (224, 224), color='blue')
    features = extractor.extract_from_pil(img)
    
    assert features.shape == (1, 4096)
    assert features.dtype == np.float32


def test_validate_image_nonexistent():
    """Test validation of non-existent image."""
    is_valid, error = validate_image('nonexistent.jpg')
    assert not is_valid
    assert "does not exist" in error


def test_word_for_id():
    """Test word ID to word conversion."""
    from tensorflow.keras.preprocessing.text import Tokenizer
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(['hello world'])
    
    word = word_for_id(1, tokenizer)
    assert word in ['hello', 'world']


def test_meteor_score():
    """Test METEOR score calculation."""
    reference = ['a', 'cat', 'on', 'the', 'mat']
    hypothesis = ['a', 'cat', 'on', 'mat']
    
    score = meteor_score(reference, hypothesis)
    assert 0 <= score <= 1


def test_rouge_l_score():
    """Test ROUGE-L score calculation."""
    reference = ['the', 'cat', 'sat', 'on', 'mat']
    hypothesis = ['cat', 'on', 'the', 'mat']
    
    score = rouge_l_score(reference, hypothesis)
    assert 0 <= score <= 1


def test_semantic_similarity():
    """Test semantic similarity calculation."""
    reference = ['dog', 'running', 'park']
    hypothesis = ['dog', 'park']
    
    score = semantic_similarity(reference, hypothesis)
    assert 0 <= score <= 1
    assert score > 0  # Should have some overlap


def test_semantic_similarity_no_overlap():
    """Test semantic similarity with no overlap."""
    reference = ['cat', 'mouse']
    hypothesis = ['dog', 'bird']
    
    score = semantic_similarity(reference, hypothesis)
    assert score == 0.0
