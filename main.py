import json
import os
import subprocess
import sys

CONFIG_FILE = "config.json"


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
    subprocess.run([sys.executable, "setup.py"])
  else:
    subprocess.run([sys.executable, "root.py"])


if __name__ == "__main__":
  main()