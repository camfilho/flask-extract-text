from flask import Flask, request, jsonify
from pypdf import PdfReader
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        pdf_url = data.get('url')

        if not pdf_url:
            return jsonify({"error": "No URL provided"}), 400

        # Download the PDF file
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Read the PDF content
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)

        # Extract text from each page
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()

        return jsonify({"extracted_text": extracted_text})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error downloading PDF: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/extract-text-from-buffer', methods=['POST'])
def extract_text_from_buffer():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        # Get the uploaded file
        pdf_file = request.files['file']
        pdf_buffer = BytesIO(pdf_file.read())  # Read file content into BytesIO object
        reader = PdfReader(pdf_buffer)

        # Extract text from each page
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()

        return jsonify({"extracted_text": extracted_text})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
