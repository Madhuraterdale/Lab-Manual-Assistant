## Setup

1. **Clone the repository**
   ```
   git clone <repo_url>
   cd Lab-Manual-Assistant
   ```
2. **Create a virtual environment**
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Copy `.env.example` to `.env` (if exists) or edit `.env` directly.
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=YOUR_KEY_HERE
     ```
   - For testing without consuming quota, set:
     ```
     SKIP_LLM=true
     ```

## Running the application

Use PowerShell (or Command Prompt) to start the app with the mock LLM:
```powershell
$env:SKIP_LLM = "true"   # optional, remove to use real Gemini
streamlit run main.py
```
Or double‑click the provided `run.ps1` script.

## Production deployment

When ready for production, disable `SKIP_LLM` and ensure a valid `GEMINI_API_KEY` is set. Deploy using Docker:
```bash
docker build -t lab‑assistant .
docker run -p 8501:8501 lab‑assistant
```

A Python-based AI assistant that processes laboratory manual PDFs, extracts experiment information, and helps students understand lab procedures efficiently.

Built using Python, LangChain, Streamlit, PyPDF2, and FAISS.
