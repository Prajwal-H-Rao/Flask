from flask import Flask, request, jsonify
import whisper
import os
import gc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the Whisper model once when the app starts
app.model = whisper.load_model("small")  # Change to "tiny" for less memory usage

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    # Save the uploaded file temporarily
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    try:
        # Perform transcription on the saved file
        result = app.model.transcribe(file_path, language=None)

        # Clean up: Delete file and clear memory
        os.remove(file_path)
        text = result["text"]
        language = result["language"]

        del result  # Explicitly delete result to free memory
        gc.collect()  # Force garbage collection

        return jsonify({
            "transcription": text,
            "language": language
        })

    except MemoryError:
        gc.collect()
        return jsonify({"error": "Memory limit exceeded"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')  # Set debug=False for better memory usage
