import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "settings.json"


def load_settings():

    if not SETTINGS_FILE.exists():
        return {}

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(data):

    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
