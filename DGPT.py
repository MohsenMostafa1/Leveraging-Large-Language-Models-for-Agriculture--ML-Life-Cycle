# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ctransformers import AutoModelForCausalLM  # Use ctransformers for GGUF models
from typing import List
import requests
from bs4 import BeautifulSoup

# Define a Pydantic model for request validation
class GenerateRequest(BaseModel):
    input_text: str
    max_length: int = 100  # Default max_length for generated text

# Initialize FastAPI app
app = FastAPI()

# Function to fetch data from websites (unchanged)
def fetch_data_from_websites(urls: List[str]) -> List[str]:
    """
    Fetch and preprocess data from a list of websites.
    """
    all_texts = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            all_texts.append(text)
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
    return all_texts

# Function to preprocess and save data (unchanged)
def preprocess_and_save_data(raw_texts: List[str], output_file: str):
    """
    Save raw data to a text file for training.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for text in raw_texts:
            f.write(text + "\n")

# Step 1: Data Fetching (unchanged)
urls = [
    "https://www.aphis.usda.gov/",
    "https://www.nal.usda.gov",
    "https://www.cabi.org/",
    "https://www.fao.org/home/en",
    "https://www.eppo.int/",
    "https://www.isppweb.org/",
]
raw_texts = fetch_data_from_websites(urls)
data_file = "agriculture_data.txt"
preprocess_and_save_data(raw_texts, data_file)

# Step 2: Load TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF Model with CPU
model_path = "TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF"  # Path to the GGUF model file

try:
    # Load the model with CPU only
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        model_type="llama",  # Specify the model type (e.g., Llama-based models)
        gpu_layers=0  # Disable GPU acceleration (run on CPU)
    )
    print(f"Successfully loaded model: {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Step 3: Create FastAPI endpoint
@app.post("/generate")
async def generate_text_api(request: GenerateRequest):
    """
    API endpoint to generate text using the CapybaraHermes-2.5-Mistral-7B-GGUF model.
    """
    input_text = request.input_text

    if not input_text:
        raise HTTPException(status_code=400, detail="input_text is required")

    try:
        # Call the model directly with the input text
        output = model(input_text)
        return {"generated_text": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Step 4: Run the FastAPI app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
