import json

import requests
from PIL import Image, ImageFilter

from utils import get_config_path, get_data_dir, resource_path


IMG_ROOT = resource_path("assets/img/root-bg.jpg")


IMG_BLUR = get_data_dir() / "root-blur.jpg"


def disabled():
    with Image.open(IMG_ROOT) as img:
        img.filter(ImageFilter.GaussianBlur(radius=15)).save(IMG_BLUR)


def fetch_img():
    print("Hi")
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": "TON_API_KEY"}
    params = {"query": "nature landscape", "orientation": "landscape", "per_page": 5}

    try:

        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"[bg] Impossible de récupérer l'image : {e}")
        return None


def check_responses_user():
    try:
        with open(get_config_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    return str(data.get("image-bg", False)).lower() == "true"


def main():
    if check_responses_user():
        fetch_img()
    else:
        disabled()


if __name__ == "__main__":
    main()