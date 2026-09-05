from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="AI Content Studio API", version="1.0.0")

# Frontend is opened directly from the filesystem (or a dev server on a
# different port), so without CORS the browser blocks every request and
# the UI always falls back to "Backend is not running".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScriptRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    language: str = "English"
    duration: int = Field(default=60, ge=15, le=600)

    @field_validator("topic")
    @classmethod
    def topic_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Topic is required")
        return value


@app.get("/")
def root():
    return {"message": "AI Content Studio API is running"}


@app.post("/generate-script")
def generate_script(req: ScriptRequest):
    topic = req.topic

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
