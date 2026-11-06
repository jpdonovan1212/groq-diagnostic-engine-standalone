import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that health endpoint returns correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_diagnose_empty_code():
    """Test that empty code raises validation error"""
    response = client.post(
        "/diagnose",
        json={
            "language": "python",
            "code": "",
            "context": None
        }
    )
    assert response.status_code == 422  # Pydantic validation error


def test_diagnose_invalid_language():
    """Test that unsupported language raises validation error"""
    response = client.post(
        "/diagnose",
        json={
            "language": "cobol",
            "code": "print('hello')",
            "context": None
        }
    )
    assert response.status_code == 422


def test_diagnose_valid_request():
    """Test successful diagnosis request"""
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="[CLEAN]"))]
    
    with patch("main.Groq") as MockGroq:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        MockGroq.return_value = mock_client
        
        response = client.post(
            "/diagnose",
            json={
                "language": "python",
                "code": "print('hello')",
                "context": "Test context"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "[CLEAN]"
        assert data["model_used"] == "llama-3.1-8b-instant"


def test_diagnose_missing_api_key():
    """Test that missing API key returns 500 error"""
    with patch.dict('os.environ', {}, clear=True):
        response = client.post(
            "/diagnose",
            json={
                "language": "python",
                "code": "print('hello')",
                "context": None
            }
        )
        assert response.status_code == 500
        assert "GROQ_API_KEY" in response.json()["detail"]
