# AI Content Studio

AI-powered content creation starter project.

## Features
- Generate video scripts from a topic (currently template-based; no AI provider is wired in yet)
- FastAPI backend with CORS enabled for local frontend use
- Simple web frontend (vanilla HTML/CSS/JS)
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
Copy `.env.example` to `.env` and add your API credentials when connecting an AI provider. Note: `main.py` doesn't read `.env` yet — this is a placeholder for the next step (wiring in an actual LLM call).
