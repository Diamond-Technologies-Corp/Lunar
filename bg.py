import json
from pathlib import Path
from PIL import Image, ImageFilter
import requests 

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
IMG_ROOT = BASE_DIR / "assets" / "img" / "root-bg.jpg"
IMG_BLUR = BASE_DIR / "assets" / "img" / "root-blur.jpg"


def disabled():
    with Image.open(IMG_ROOT) as img:
        img.filter(ImageFilter.GaussianBlur(radius=15)).save(IMG_BLUR)


def fetch_img():
    print("Hi")
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": "TON_API_KEY"}
    params = {"query": "nature landscape", "orientation": "landscape", "per_page": 5}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()


def check_responses_user():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    return data.get("image-bg", False)


def main():
    if check_responses_user():
        fetch_img()
    else:
        disabled()


if __name__ == "__main__":
    main()