from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Content Studio API", version="1.0.0")

class ScriptRequest(BaseModel):
    topic: str
    language: str = "English"
    duration: int = 60

@app.get("/")
def root():
    return {"message": "AI Content Studio API is running"}

@app.post("/generate-script")
def generate_script(req: ScriptRequest):
    topic = req.topic.strip()
    if not topic:
        return {"error": "Topic is required"}

    script = (
        f"HOOK: Did you know this about {topic}?\n\n"
        f"BODY: In this {req.duration}-second {req.language} video, "
        f"we explain the most important facts about {topic} in a simple and engaging way.\n\n"
        "CTA: Follow for more useful content."
    )
    return {
        "topic": topic,
        "language": req.language,
        "duration": req.duration,
        "script": script
    }
