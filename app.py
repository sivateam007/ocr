import os
import io
import tempfile
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

app = Flask(__name__)

# Optional: Set Tesseract path if needed (Render's default path is fine)
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@app.route('/')
def home():
    return "Tamil OCR API is running! Use POST /ocr with a file."

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    language = request.form.get('lang', 'tam')  # default Tamil

    try:
        if file.filename.lower().endswith('.pdf'):
            # Convert PDF to images
            images = convert_from_bytes(file.read(), dpi=300)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img, lang=language) + "\n"
        else:
            # Assume it's an image
            img = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(img, lang=language)

        return jsonify({'success': True, 'text': text.strip()})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Bind to 0.0.0.0 to make it accessible from outside
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))