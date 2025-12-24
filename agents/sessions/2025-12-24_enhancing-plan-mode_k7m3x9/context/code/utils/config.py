from pathlib import Path

# Global configuration that can be imported by other notebooks
CONFIG = {
    "DEBUG": False,
    "MODEL_NAME": "gemini-2.5-pro-preview-05-20",
    "TEMPERATURE": 0.5,
    "THINKING_BUDGET": 8192,
    "INPUT_DIR": "../inputs",
    "OUTPUT_DIR": "outputs",
    "PROMPTS_DIR": "./prompts",
    "INTERIM_DATA_DIR": Path("interim_data"),
}

# Create interim data directory
CONFIG["INTERIM_DATA_DIR"].mkdir(exist_ok=True)


def get_config():
    """Get the global configuration."""
    return CONFIG


def update_config(**kwargs):
    """Update configuration values."""
    CONFIG.update(kwargs)
    return CONFIG
