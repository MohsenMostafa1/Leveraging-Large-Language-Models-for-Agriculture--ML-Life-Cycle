import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

# Create a TestClient instance
client = TestClient(app)

def test_generate_endpoint():
    # Test the /generate endpoint with valid input
    response = client.post(
        "/generate",
        json={"input_text": "What is agriculture?", "max_length": 50},
    )
    assert response.status_code == 200
    assert "generated_text" in response.json()

def test_generate_endpoint_invalid_input():
    # Test the /generate endpoint with invalid input (missing input_text)
    response = client.post(
        "/generate",
        json={"max_length": 50},  # Missing input_text
    )
    assert response.status_code == 422  # FastAPI returns 422 for validation errorss
