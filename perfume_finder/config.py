import os
from pathlib import Path


from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Config:
    # Always set SECRET_KEY in production; the default is only for local development.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() in ("1", "true", "yes")

    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

    PERFUME_DATABASE_PATH = os.environ.get(
        "PERFUME_DATABASE_PATH", str(PROJECT_ROOT / "data" / "perfumes.json")
    )
