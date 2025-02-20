from flask import Flask, request, jsonify
import whisper
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load the Whisper model once when the app starts
app.model = whisper.load_model("small")  # Use "turbo", "small", "medium", or "large" as needed

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
        result = app.model.transcribe(file_path, language=None)  # Auto-detect language

        # Delete the uploaded file after transcription
        os.remove(file_path)

        # Return JSON response with transcription and detected language
        return jsonify({
            "transcription": result["text"],
            "language": result["language"]
        })

    except Exception as e:
        # Handle exceptions gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')