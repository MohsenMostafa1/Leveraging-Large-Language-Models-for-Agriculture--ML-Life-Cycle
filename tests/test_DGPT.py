from fastapi.testclient import TestClient
from src.main import app  # Import your FastAPI app from the src directory

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
    assert response.status_code == 422  # FastAPI returns 422 for validation errors
