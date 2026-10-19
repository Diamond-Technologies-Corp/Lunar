import json
import os
import sys
import tempfile
import urllib.request
import webbrowser

from utils import DEFAULT_CONFIG

RELEASES_URL = "https://api.github.com/repos/Diamond-Technologies-Corp/Lunar/releases"


def is_dev_mode():

    return not getattr(sys, "frozen", False)


def parse_version(v_str):
    clean_str = v_str.lstrip("vV")
    parts = []
    for p in clean_str.split("."):
        if p.isdigit():
            parts.append(int(p))
    return parts


def get_latest_release(timeout=5):
    req = urllib.request.Request(RELEASES_URL, headers={"User-Agent": "Lunar-App"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = json.loads(response.read().decode())

    if isinstance(data, list) and len(data) > 0:
        return data[0]
    return None


def check_for_updates():
    if is_dev_mode():
        print("[Update] ⛔ Mode Développement détecté : Vérification des MAJ désactivée.")
        return {"update_available": False}


    current_version = DEFAULT_CONFIG["version"]

    try:
        release = get_latest_release()
        if release:
            latest_version = release.get("tag_name", "").lstrip("vV")

            if parse_version(latest_version) > parse_version(current_version):
                return {
                    "update_available": True,
                    "latest_version": latest_version,
                    "current_version": current_version,
                    "download_url": release.get("html_url"),
                }
    except Exception:
        pass

    return {"update_available": False}


def launch():

    if is_dev_mode():
        print("[Launch] ⛔ Mode Développement détecté : Téléchargement bloqué.")
        return None

    try:
        release = get_latest_release(timeout=10)
        if not release:
            return None

        for asset in release.get("assets", []):
            name = asset.get("name", "")
            if name.lower().endswith(".exe"):
                temp_path = os.path.join(tempfile.gettempdir(), name)
                urllib.request.urlretrieve(asset["browser_download_url"], temp_path)
                return temp_path

       
        page = release.get("html_url")
        if page:
            webbrowser.open(page)
    except Exception:
        pass

    return None


def apply_update(installer_path):

    if is_dev_mode():
        print("[Update] Development mode detected: update installation aborted.")
        return False

    try:
        os.startfile(installer_path) 
    except Exception:
        return False

    sys.exit(0)