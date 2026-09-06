import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

load_dotenv()

app = FastAPI(title="AI Content Studio API", version="1.1.0")

# Frontend is opened directly from the filesystem (or a dev server on a
# different port), so without CORS the browser blocks every request and
# the UI always falls back to "Backend is not running".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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


def build_template_script(topic: str, language: str, duration: int) -> str:
    """Deterministic fallback used when no OpenAI key is configured, or
    when the OpenAI call fails for any reason."""
    return (
        f"HOOK: Did you know this about {topic}?\n\n"
        f"BODY: In this {duration}-second {language} video, "
        f"we explain the most important facts about {topic} in a simple and engaging way.\n\n"
        "CTA: Follow for more useful content."
    )


def build_ai_script(topic: str, language: str, duration: int) -> Optional[str]:
    """Try to generate a script with OpenAI. Returns None on any failure
    (missing key, network error, bad response) so the caller can fall
    back to the template generator instead of crashing the request."""
    if not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        # A flat token budget cut long scripts off mid-sentence: 400 tokens
        # is fine for a 60s script (~150 words) but nowhere near enough for
        # a 600s one (~1500 words). Scale roughly with requested duration,
        # capped so a single request can't run away in cost/latency.
        estimated_tokens = int(duration * 4)  # ~150 wpm, ~1.3 tokens/word
        max_tokens = max(200, min(estimated_tokens, 2000))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You write short, punchy scripts for short-form video "
                        "(Shorts/Reels/TikTok). Structure every response as "
                        "HOOK, BODY, and CTA on separate lines, matching the "
                        "requested duration and language. Reply in plain text "
                        "only — no markdown, no asterisks, no headings, no "
                        "code fences."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Write a {duration}-second video script in {language} "
                        f"about: {topic}"
                    ),
                },
            ],
            max_tokens=max_tokens,
            timeout=15,
        )
        content = response.choices[0].message.content
        if not content:
            return None

        # Safety net for models that wrap output in a code fence anyway.
        cleaned = content.strip().strip("`").strip()
        return cleaned or None
    except Exception as exc:  # any failure should fall back, never crash the request
        print(f"[generate-script] OpenAI generation failed, using template: {exc}")
        return None


@app.get("/")
def root():
    return {"message": "AI Content Studio API is running"}


@app.post("/generate-script")
def generate_script(req: ScriptRequest):
    topic = req.topic

    ai_script = build_ai_script(topic, req.language, req.duration)
    script = ai_script or build_template_script(topic, req.language, req.duration)

    return {
        "topic": topic,
        "language": req.language,
        "duration": req.duration,
        "script": script,
        "source": "ai" if ai_script else "template",
    }
