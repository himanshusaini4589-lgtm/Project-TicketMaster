import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = PROJECT_ROOT / "backend" / "prompts"
AGENT_NAME = "Ticketmaster Event Assistant"

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

MAX_MODEL_CALLS_PER_RUN = int(os.getenv("MAX_MODEL_CALLS_PER_RUN", "10"))

def hitl_enabled() -> bool:
    return os.getenv("HITL_ENABLED", "true").lower() in {"1", "true", "yes"}