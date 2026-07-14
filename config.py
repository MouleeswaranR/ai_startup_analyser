"""
Configuration module for the AI Company system.
Loads environment variables and provides shared config.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Fix for LiteLLM and CrewAI Telemetry errors
os.environ["LITELLM_DROP_PARAMS"] = "True"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Fix for Groq complaining about 'cache_breakpoint' unsupported property
try:
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except ImportError:
    pass

# ── API Keys ──────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
API_KEY = os.getenv("API_KEY", "")

# ── Model Configuration ──────────────────────────────────
AVAILABLE_MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b",
    "openrouter/free",
    "groq/llama-3.1-70b-versatile"
]

MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b"
TEMPERATURE = 0.4
MAX_OUTPUT_TOKENS = 8192
AGENT_DELAY_SECONDS = 0  # No pause needed for Nvidia/Openrouter free routing

# ── Output Directory ─────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Validation ────────────────────────────────────────────
def validate_config(model_name: str = None):
    """Validate that all required configuration is present."""
    model_to_check = model_name or MODEL_NAME
    if model_to_check.startswith("openrouter/") and not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY not set. "
            "Create a .env file with OPENROUTER_API_KEY='your_key_here'"
        )
    elif model_to_check.startswith("groq/") and not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set. "
            "Create a .env file with GROQ_API_KEY='your_key_here'"
        )
    elif model_to_check.startswith("nvidia/") and not NVIDIA_API_KEY:
        raise ValueError(
            "NVIDIA_API_KEY not set. "
            "Create a .env file with NVIDIA_API_KEY='your_key_here'"
        )
    return True
