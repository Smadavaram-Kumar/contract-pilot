"""
Configuration loader for ContractPilot.

Loads environment variables from .env file and validates that required
configuration is present.
"""

import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(dotenv_path: str = ".env") -> bool:
    """Load key-value pairs from a .env file into os.environ."""
    path = Path(dotenv_path)
    if not path.exists():
        return False

    with path.open() as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value

    return True


@dataclass
class Config:
    """Application configuration loaded from environment variables."""
    
    foundry_endpoint: str
    foundry_model: str
    log_level: str = "INFO"


def load_config() -> Config:
    """
    Load configuration from .env file and environment variables.
    
    Raises:
        ValueError: If required environment variables are missing.
    
    Returns:
        Config object with validated settings.
    """
    # Load .env file into os.environ
    load_dotenv()
    
    # Read required variables
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # Validate
    if not endpoint:
        raise ValueError(
            "FOUNDRY_PROJECT_ENDPOINT is not set. "
            "Add it to your .env file."
        )
    
    if not model:
        raise ValueError(
            "FOUNDRY_MODEL is not set. "
            "Add it to your .env file."
        )
    
    return Config(
        foundry_endpoint=endpoint,
        foundry_model=model,
        log_level=log_level,
    )