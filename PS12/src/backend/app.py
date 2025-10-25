from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from utils import extract_text_from_file, clean_text, summarize_text

ALLOWED_EXTENSIONS = {"pdf", "txt"}

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    # Simple CORS for local development. Replace with flask-cors or stricter rules in production.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def allowed_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/generate-podcast", methods=["POST", "OPTIONS"])
def generate_podcast():
    # Respond to preflight
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
    """
    Expected multipart/form-data with a single file field named 'file'.
    This endpoint performs:
      - basic auth placeholder (Authorization header optional for now)
      - text extraction (pdf/txt)
      - cleaning of extracted text
      - summarization stub (replace with AI call later)

    Returns JSON with { success, summary, audio_url }
    Note: TTS and cloud storage are not implemented in this scaffold.
    """
    # Basic auth placeholder (replace with real auth in prod)
    auth = request.headers.get("Authorization")
    if not auth:
        # allow for local testing but note in the response
        auth_notice = "no-authorization-provided"
    else:
        auth_notice = "authorization-present"

    if "file" not in request.files:
        return jsonify({"success": False, "error": "missing file in request"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename or "")

    if filename == "" or not allowed_filename(filename):
        return jsonify({"success": False, "error": "invalid or missing filename (allowed: .pdf, .txt)"}), 400

    # Save to a temporary file for processing
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = os.path.join(tmpdir, filename)
        file.save(tmp_path)

        # Extract text
        raw_text = extract_text_from_file(tmp_path)
        if not raw_text or raw_text.strip() == "":
            return jsonify({"success": False, "error": "no text extracted from file"}), 400

        # Clean the text
        cleaned = clean_text(raw_text)

        # Summarize (stub) - replace this with an AI provider call later
        summary = summarize_text(cleaned)

    # No TTS or storage implemented here. Provide a placeholder audio_url field.
    result = {
        "success": True,
        "auth": auth_notice,
        "summary": summary,
        "audio_url": None,
        "note": "TTS and cloud storage not implemented in scaffold. Replace summarize_text() or extend this endpoint to POST to TTS and upload the returned audio to cloud storage (S3/GCS/Firebase).",
    }

    return jsonify(result)


if __name__ == "__main__":
    # For local dev only. In production, use a WSGI server.
    app.run(host="127.0.0.1", port=5000, debug=True)
