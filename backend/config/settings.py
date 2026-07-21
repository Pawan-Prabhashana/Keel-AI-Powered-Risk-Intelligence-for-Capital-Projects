"""Configuration settings for Keel."""

import os

# Default model. Override with ANTHROPIC_MODEL in .env if desired.
DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def get_model_deployment_name():
    """Returns the model id used for all agents."""
    return os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)


def get_anthropic_api_key():
    """Returns the Anthropic API key."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("Missing required environment variable: ANTHROPIC_API_KEY")
    return key


def get_database_connection_string():
    """Returns the SQLite database path."""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.getenv("DB_PATH", os.path.join(here, "keel.db"))


# --- Backwards-compat shims so existing imports don't break ---
def initialize_ai_agent_settings():
    """Kept for import compatibility. Returns a simple settings dict."""
    return {
        "model": get_model_deployment_name(),
        "api_key": get_anthropic_api_key(),
    }


def get_project_client():
    """Not used; kept for import compatibility."""
    return None
