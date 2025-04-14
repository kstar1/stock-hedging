import os
import shutil
import json

CONFIG_JSON = "config/config_filters.json"
CONFIG_PY = "config/config_filters.py"
INIT_FILE = "config/__init__.py"
FILTER_VARS = {
    "FILTER_CONFIG": {
        "moneyness_range": [0.95, 1.05],
        "min_volume": 100
    }
}

def ensure_package_structure():
    if not os.path.exists("config"):
        os.makedirs("config")
    if not os.path.exists("cache"):
        os.makedirs("cache")
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(INIT_FILE, "w") as f:
        f.write("# Makes 'config' a Python package\n")

def convert_json_to_py():
    if os.path.exists(CONFIG_JSON):
        try:
            with open(CONFIG_JSON, "r") as f:
                config_data = json.load(f)
            with open(CONFIG_PY, "w") as f:
                f.write(f"FILTER_CONFIG = {json.dumps(config_data, indent=4)}\n")
            os.remove(CONFIG_JSON)
            print("✅ Converted config_filters.json to config_filters.py")
        except Exception as e:
            print(f"❌ Failed to convert JSON: {e}")
    elif not os.path.exists(CONFIG_PY):
        with open(CONFIG_PY, "w") as f:
            f.write(f"FILTER_CONFIG = {json.dumps(FILTER_VARS['FILTER_CONFIG'], indent=4)}\n")
        print("✅ Created default config_filters.py")

if __name__ == "__main__":
    print("🔧 Running setup for stock-hedging project...")
    ensure_package_structure()
    convert_json_to_py()
    print("✅ Setup complete. You can now run: PYTHONPATH=. python src/main.py")
