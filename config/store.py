import json
import os

CONFIG_FILE = "snapbase_config.json"

DEFAULT_CONFIG = {
    "api_key": None,
    "db_profiles": []
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
