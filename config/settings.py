import json
import os

CONFIG_DIR = os.path.dirname(__file__)
FILTER_CONFIG_PATH = os.path.join(CONFIG_DIR, 'config_filters.json')

def load_filter_config():
    try:
        with open(FILTER_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Filter config file not found at {FILTER_CONFIG_PATH}")
        # Return default values if file is missing
        return {
            "min_volume": 50,
            "moneyness_range": [0.90, 1.10] # Example defaults
        }

# Load once on import
FILTER_CONFIG = load_filter_config()

# Other settings
DEFAULT_TICKER = "TSLA"
# Add functions to load API keys from .env later if needed