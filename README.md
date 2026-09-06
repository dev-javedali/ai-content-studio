# AI Content Studio

AI-powered content creation starter project.

## Features
- Generate video scripts from a topic using OpenAI (falls back to a local template if no API key is set or the call fails)
- FastAPI backend with CORS enabled for local frontend use
- Simple web frontend (vanilla HTML/CSS/JS) with a copy-to-clipboard button and a badge showing whether the script came from AI or the template
- Ready for future TTS, image generation, captions and FFmpeg pipelines

## Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API runs at `http://127.0.0.1:8000`.

### Frontend
Open `frontend/index.html` directly in your browser (or serve it with any static server). It talks to the backend at `http://127.0.0.1:8000` by default — update `API_URL` in `index.html` if you run the backend elsewhere.

## Environment
Copy `.env.example` to `.env` and set `OPENAI_API_KEY` to enable real AI-generated scripts:
```bash
cp .env.example .env
# then edit .env and add your key
```
Without a key, `/generate-script` still works and returns a template-based script (response includes `"source": "template"` so the frontend can tell the difference).
