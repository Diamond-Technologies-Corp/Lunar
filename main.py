import json
import os
import subprocess
import sys
from pathlib import Path
from root import build
from setup import setup

CONFIG_FILE = "config.json"

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

def load_or_create_config(config_path="config.json"):
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        print(f"✨ Fichier {config_path} créé avec la configuration par défaut !")
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture de {config_path}: {e}")
        return DEFAULT_CONFIG

def get_config_dir():
    if os.name == "nt":  # Windows
        base_dir = os.getenv("APPDATA")
    else:  # Linux / macOS
        base_dir = os.path.expanduser("~/.config")
    
    config_dir = Path(base_dir) / "Lunar"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def check_setup_status():
  if not os.path.exists(CONFIG_FILE):
    return False

  try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      return data.get("did_setup", False)
  except Exception:
    return False


def main():
  is_setup_done = check_setup_status()

  if not is_setup_done:
    setup()
  else:
        build()

if __name__ == "__main__":
  main()