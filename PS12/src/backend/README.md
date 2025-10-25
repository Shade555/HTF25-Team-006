# Backend (Flask) scaffold

This folder contains a small Flask scaffold for Phase 2 (file upload, text extraction and cleaning).

Quick start (PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
cd src\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the server (development):

```powershell
#$env:FLASK_APP = "app.py"
#$env:FLASK_ENV = "development"
python app.py
```

4. Test the health endpoint:

```powershell
curl http://127.0.0.1:5000/api/health
```

5. Test file upload (PowerShell example using curl):

```powershell
curl -X POST "http://127.0.0.1:5000/api/generate-podcast" -H "Authorization: Bearer testtoken" -F "file=@C:/path/to/your/file.pdf"
```

Notes
- The endpoint currently returns a `summary` field and `audio_url` is `null`. Replace the `summarize_text()` function with a call to your chosen AI summarizer and add a TTS/upload step to produce `audio_url`.
- `utils.py` uses PyMuPDF (fitz) to extract PDF text and a small cleaning heuristic. The heuristics are intentionally simple and should be improved for production.
