import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

def is_dev_mode():
    return Path(".git").exists() or Path("venv").exists()

def parse_version(v_str):
    clean_str = v_str.lstrip("vV")
    parts = []
    for p in clean_str.split("."):
        if p.isdigit():
            parts.append(int(p))
    return parts

def check_for_updates():
    if is_dev_mode():
        print("[Update] ⛔ Mode Développement détecté : Vérification des MAJ désactivée.")
        return {"update_available": False}

    repo_url = "https://api.github.com/repos/Diamond-Technologies-Corp/Lunar/releases"
    config_path = "config.json"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        current_version = config.get("version", "1.0")

        req = urllib.request.Request(repo_url, headers={"User-Agent": "Lunar-App"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

            if isinstance(data, list) and len(data) > 0:
                latest_release = data[0]
                latest_tag = latest_release.get("tag_name", "")
                latest_version = latest_tag.lstrip("vV")

                if parse_version(latest_version) > parse_version(current_version):
                    return {
                        "update_available": True,
                        "latest_version": latest_version,
                        "current_version": current_version,
                        "download_url": latest_release.get("zipball_url"),
                    }
    except Exception:
        pass

    return {"update_available": False}

def launch():
    if is_dev_mode():
        print("[Launch] ⛔ Mode Développement détecté : Téléchargement bloqué pour protéger le code source.")
        return None

    repo_url = "https://api.github.com/repos/Diamond-Technologies-Corp/Lunar/releases"

    try:
        req = urllib.request.Request(repo_url, headers={"User-Agent": "Lunar-App"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            if isinstance(data, list) and len(data) > 0:
                latest_release = data[0]
                zip_url = latest_release.get("zipball_url")

                if zip_url:
                    temp_dir = os.environ.get("TEMP", "/tmp")
                    temp_zip = os.path.join(temp_dir, "lunar_update.zip")
                    urllib.request.urlretrieve(zip_url, temp_zip)
                    return temp_zip
    except Exception:
        pass

    return None

def apply_update(zip_path):
    if is_dev_mode():
        print("[Update] Development mode detected: update installation aborted.")
        return False

    app_dir = os.getcwd()
    temp_extract_dir = os.path.join(os.environ.get("TEMP", "/tmp"), "lunar_extracted")

    try:
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_extract_dir)

        extracted_contents = os.listdir(temp_extract_dir)
        if not extracted_contents:
            return False

        source_dir = os.path.join(temp_extract_dir, extracted_contents[0])

        new_version = None
        temp_config_path = os.path.join(source_dir, "config.json")
        if os.path.exists(temp_config_path):
            try:
                with open(temp_config_path, "r", encoding="utf-8") as f_temp:
                    new_version = json.load(f_temp).get("version")
            except Exception:
                pass

        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(app_dir, item)

            if item == "config.json" and os.path.exists(d):
                continue

            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                file_name = os.path.basename(s)
                if file_name != "update.py":
                    shutil.copy2(s, d)

        local_config_path = os.path.join(app_dir, "config.json")
        if os.path.exists(local_config_path) and new_version:
            try:
                with open(local_config_path, "r", encoding="utf-8") as f:
                    local_data = json.load(f)
                local_data["version"] = new_version
                with open(local_config_path, "w", encoding="utf-8") as f:
                    json.dump(local_data, f, indent=4)
            except Exception:
                pass

        main_script = os.path.join(app_dir, "root.py")
        subprocess.Popen([sys.executable, main_script])
        sys.exit(0)

    except Exception:
        return False