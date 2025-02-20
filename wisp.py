from flask import Flask, request, jsonify
import os
import gc
import io
from flask_cors import CORS
from faster_whisper import WhisperModel

app = Flask(__name__)
CORS(app)

# Load the Whisper model once when the app starts ("tiny" for lower memory usage)
model = WhisperModel("tiny", compute_type="int8")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read file into memory instead of saving to disk
        audio_data = io.BytesIO(file.read())

        # Perform transcription
        segments, info = model.transcribe(audio_data, language=None)
        text = " ".join(segment.text for segment in segments)
        
        return jsonify({
            "transcription": text,
            "language": info.language
        })

    except MemoryError:
        gc.collect()
        return jsonify({"error": "Memory limit exceeded"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
