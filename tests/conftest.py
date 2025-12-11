"""Pytest configuration and fixtures."""
import pytest
import numpy as np
from PIL import Image
from unittest.mock import Mock


@pytest.fixture
def sample_image():
    """Create a sample PIL image."""
    return Image.new('RGB', (224, 224), color='red')


@pytest.fixture
def sample_features():
    """Create sample image features."""
    return np.random.rand(1, 4096).astype(np.float32)


@pytest.fixture
def mock_tokenizer():
    """Create mock tokenizer."""
    tokenizer = Mock()
    tokenizer.word_index = {
        'startseq': 1,
        'a': 2,
        'cat': 3,
        'on': 4,
        'mat': 5,
        'endseq': 6
    }
    tokenizer.texts_to_sequences = Mock(return_value=[[1, 2, 3, 4, 5, 6]])
    return tokenizer


@pytest.fixture
def mock_model():
    """Create mock model."""
    model = Mock()
    model.predict = Mock(return_value=np.array([[0.1, 0.2, 0.3, 0.4]]))
    return model
