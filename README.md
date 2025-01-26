# Leveraging-Large-Language-Models-for-Agriculture
# ml-lifecycle-fastapi3
# Machine Learning Life Cycle with FastAPI


This project demonstrates a machine learning life cycle, including data fetching, preprocessing, model loading, and serving via FastAPI.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Leveraging Large Language Models for Agriculture: A Practical Guide with Flask and TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF

### Large Language Models (LLMs) have revolutionized the way we interact with and process textual data. From generating human-like text to summarizing complex documents, LLMs have found applications across various domains, including agriculture. In this article, we’ll explore how to build a simple yet powerful Flask API that leverages the TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF model to generate text based on agricultural data fetched from multiple websites.

### Overview of the Code

### The provided Python script is a comprehensive example of how to:

Fetch and preprocess agricultural data from multiple websites.

Load a pre-trained LLM (TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF).

Create a Flask API to generate text using the loaded model.

Let’s break down the key components of the code.

### Step 1: Data Fetching and Preprocessing
### Fetching Data from Websites

#### The script starts by fetching data from a list of agricultural websites using the requests library. The fetch_data_from_websites function:

Takes a list of URLs as input.

Uses BeautifulSoup to parse the HTML content and extract text from <p> tags.

Filters out empty or irrelevant text and stores the cleaned data.

```python
def fetch_data_from_websites(urls: List[str]) -> List[str]:
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
```
### Saving the Datacd/ic

The fetched data is then saved to a text file (agriculture_data.txt) for future use or training purposes.
```python
def preprocess_and_save_data(raw_texts: List[str], output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        for text in raw_texts:
            f.write(text + "\n")
```
### Step 2: Loading the LLM
The script uses the ctransformers library to load the TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF model. This model is a fine-tuned version of the Mistral-7B architecture, optimized for generating high-quality text.
```python
model_path = "TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF"
model = AutoModelForCausalLM.from_pretrained(model_path, model_type="llama")
```
The AutoModelForCausalLM class is used to load the model, and the model_type="llama" parameter specifies the architecture. If the model is successfully loaded, a confirmation message is printed.

### Step 3: Creating the Flask API

The Flask API provides a simple endpoint (/generate) to interact with the loaded LLM. Users can send a POST request with an input text and receive a generated response.
### API Endpoint
cd/ic
The /generate endpoint:

Accepts JSON input with two fields: input_text and max_length.

Uses the LLM to generate text based on the input.

    Returns the generated text as a JSON response.
```python
@app.route('/generate', methods=['POST'])
def generate_text_api():
    data = request.json
    input_text = data.get('input_text', '')
    max_length = data.get('max_length', 100)

    if not input_text:
        return jsonify({"error": "input_text is required"}), 400

    try:
        output = model.generate(
            input_text,
            max_new_tokens=max_length,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.1
        )
        return jsonify({"generated_text": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```
### Step 4: Running the API

The Flask API can be run locally or deployed to a server. By default, it listens on 0.0.0.0 and port 5000.
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
### Potential Applications in Agriculture

This code can be adapted for various agricultural use cases, such as:

Generating Reports: Automatically generate summaries of agricultural research or news articles.
