import json

from root import build
from setup import setup
from utils import get_config_path


def check_setup_status():
    try:
        with open(get_config_path(), "r", encoding="utf-8") as f:
            return json.load(f).get("did_setup", False)
    except Exception:
        return False


def main():
    if not check_setup_status():
        setup()

    if check_setup_status():
        build()


if __name__ == "__main__":
    main()