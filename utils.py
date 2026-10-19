import json
import os
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "location": {
        "method": "UOIF (12° / 12°)",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    "language-content-llm": "French",
    "version": "1.3",
    "Prayer": {
        "fajr": "07:05",
        "duhr": "13:36",
        "asr": "16:24",
        "maghrib": "18:57",
        "icha": "20:06"
    },
    "did_setup": False,
    "image-bg": "True"
}


def resource_path(relative_path):

    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


def get_data_dir():

    if os.name == "nt":  # Windows
        base = os.getenv("APPDATA")
    else:  # Linux / macOS
        base = os.path.expanduser("~/.config")

    folder = Path(base) / "Lunar"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_config_path():

    path = get_data_dir() / "config.json"

    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)

    return path