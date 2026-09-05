# AI Content Studio

AI-powered content creation starter project.

## Features
- Generate video scripts from a topic
- Project-based content workflow
- FastAPI backend
- Simple web frontend
- Ready for future TTS, image generation, captions and FFmpeg pipelines

## Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
Open `frontend/index.html` in your browser.

## Environment
Copy `.env.example` to `.env` and add your API credentials when connecting an AI provider.
