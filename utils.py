import copy
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from version import __version__

DEFAULT_CONFIG = {
    "location": {
        "method": "UOIF (12° / 12°)",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    "language-content-llm": "French",
    "version": __version__,
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

MAX_LOG_SIZE = 200_000  # octets

_config_checked = False


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


def log(message):
    
    try:
        path = get_data_dir() / "lunar.log"
        if path.exists() and path.stat().st_size > MAX_LOG_SIZE:
            path.write_text("", encoding="utf-8")
        with path.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
    except Exception:
        pass


def _write_config(path, data):
    tmp_path = path.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    os.replace(tmp_path, path)


def _merge_defaults(defaults, current):

    changed = False
    for key, value in defaults.items():
        if key not in current:
            current[key] = copy.deepcopy(value)
            changed = True
        elif isinstance(value, dict) and isinstance(current[key], dict):
            if _merge_defaults(value, current[key]):
                changed = True
    return changed


def _migrate_config(path):

    try:
        with path.open("r", encoding="utf-8") as f:
            current = json.load(f)
        if not isinstance(current, dict):
            raise ValueError("config.json is not a JSON object")
    except (OSError, ValueError) as e:

        log(f"[Config] Unreadable config.json ({e}); resetting to defaults.")
        try:
            os.replace(path, path.with_suffix(".json.bak"))
        except OSError:
            pass
        _write_config(path, DEFAULT_CONFIG)
        return

    changed = _merge_defaults(DEFAULT_CONFIG, current)


    if current.get("version") != __version__:
        current["version"] = __version__
        changed = True

    if changed:
        _write_config(path, current)


def get_config_path():
    global _config_checked

    path = get_data_dir() / "config.json"

    if not path.exists():
        _write_config(path, DEFAULT_CONFIG)
        _config_checked = True
    elif not _config_checked:
        _migrate_config(path)
        _config_checked = True

    return path