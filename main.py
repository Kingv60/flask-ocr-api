from flask import Flask, request, jsonify
from PIL import Image
import io
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['en'])  # load once

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        image = Image.open(image_file.stream).convert("RGB")
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        result = reader.readtext(image_bytes)
        extracted_text = " ".join([text[1] for text in result])

        return jsonify({'text': extracted_text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
