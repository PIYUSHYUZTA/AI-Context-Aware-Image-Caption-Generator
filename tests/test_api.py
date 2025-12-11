"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import io
from PIL import Image
import numpy as np


@pytest.fixture
def client():
    """Create test client."""
    with patch('api.load_models'):
        from api import app
        return TestClient(app)


@pytest.fixture
def sample_image():
    """Create sample image for testing."""
    img = Image.new('RGB', (224, 224), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data


def test_model_info(client):
    """Test model info endpoint."""
    with patch('api.caption_generator') as mock_gen:
        mock_gen.tokenizer.word_index = {'test': 1}
        mock_gen.max_length = 34
        
        response = client.get("/api/v1/model-info")
        assert response.status_code == 200


def test_generate_caption_no_file(client):
    """Test caption generation without file."""
    response = client.post("/api/v1/caption")
    assert response.status_code == 422  # Validation error


def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data


def test_clear_cache(client):
    """Test cache clearing."""
    response = client.delete("/api/v1/cache")
    assert response.status_code == 200
    assert "message" in response.json()
