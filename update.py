import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.request
import webbrowser

from utils import log
from version import __version__

REPO = "Diamond-Technologies-Corp/Lunar"
RELEASES_URL = f"https://github.com/Diamond-Technologies-Corp/Lunar/releases"
ALLOWED_PREFIX = f"https://github.com/{REPO}/"
INSTALLER_PREFIX = "lunarsetup"  # LunarSetup.exe

API_TIMEOUT = 5
DOWNLOAD_TIMEOUT = 15
CHUNK_SIZE = 64 * 1024


def is_dev_mode():
   
    if os.getenv("LUNAR_FORCE_UPDATES") == "1":
        return False
    return not getattr(sys, "frozen", False)


def parse_version(v_str):
    match = re.match(r"\s*[vV]?(\d+(?:\.\d+)*)", str(v_str))
    if not match:
        return ()
    parts = [int(p) for p in match.group(1).split(".")]
    while parts and parts[-1] == 0:  # 1.4.0 == 1.4
        parts.pop()
    return tuple(parts)


def _get_json(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": "Lunar-App"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def find_installer_asset(release):
    for asset in release.get("assets", []):
        name = asset.get("name", "")
        url = asset.get("browser_download_url", "")
        if (
            name.lower().startswith(INSTALLER_PREFIX)
            and name.lower().endswith(".exe")
            and url.startswith(ALLOWED_PREFIX)
        ):
            return asset
    return None


def find_checksum_asset(release, installer_name):
    wanted = f"{installer_name}.sha256".lower()
    for asset in release.get("assets", []):
        if asset.get("name", "").lower() == wanted:
            if asset.get("browser_download_url", "").startswith(ALLOWED_PREFIX):
                return asset
    return None


def get_latest_release(timeout=API_TIMEOUT):
    data = _get_json(RELEASES_URL, timeout)

    if not isinstance(data, list):
        log(f"[Update] Unexpected GitHub response: {str(data)[:200]}")
        return None

    candidates = [
        r
        for r in data
        if isinstance(r, dict) and not r.get("draft") and find_installer_asset(r)
    ]
    if not candidates:
        return None

    return max(candidates, key=lambda r: parse_version(r.get("tag_name", "")))


def _describe_release(release):
    asset = find_installer_asset(release)
    checksum = find_checksum_asset(release, asset["name"]) if asset else None
    return {
        "latest_version": release.get("tag_name", "").lstrip("vV"),
        "download_url": release.get("html_url"),
        "asset_name": asset["name"] if asset else None,
        "asset_url": asset["browser_download_url"] if asset else None,
        "asset_size": asset.get("size") if asset else None,
        "checksum_url": checksum["browser_download_url"] if checksum else None,
    }


def check_for_updates():
    if is_dev_mode():
        print("[Update] Development mode detected: update check disabled.")
        return {"update_available": False}

    current_version = __version__

    try:
        release = get_latest_release()
        if release:
            info = _describe_release(release)
            latest_version = info["latest_version"]
            log(f"[Update] current={current_version} latest={latest_version}")

            if parse_version(latest_version) > parse_version(current_version):
                info["update_available"] = True
                info["current_version"] = current_version
                return info
        else:
            log("[Update] No usable release found.")
    except Exception as e:
        log(f"[Update] Check failed: {e}")

    return {"update_available": False}


def _fetch_expected_hash(url):
    if not url:
        return None
    req = urllib.request.Request(url, headers={"User-Agent": "Lunar-App"})
    with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
        text = response.read().decode("utf-8", errors="replace").strip()
    token = text.split()[0].lower() if text else ""
    if not re.fullmatch(r"[0-9a-f]{64}", token):
        raise ValueError("Invalid SHA256 file in release")
    return token


def _download_installer(info):
    name = os.path.basename(info["asset_name"])
    folder = os.path.join(tempfile.gettempdir(), "LunarUpdate")
    os.makedirs(folder, exist_ok=True)

    final_path = os.path.join(folder, name)
    part_path = final_path + ".part"

    expected_hash = _fetch_expected_hash(info.get("checksum_url"))
    sha = hashlib.sha256()
    received = 0

    req = urllib.request.Request(
        info["asset_url"], headers={"User-Agent": "Lunar-App"}
    )

    try:
        with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as response:
            expected_size = int(
                response.headers.get("Content-Length") or info.get("asset_size") or 0
            )
            with open(part_path, "wb") as out:
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    out.write(chunk)
                    sha.update(chunk)
                    received += len(chunk)

        if expected_size and received != expected_size:
            raise ValueError(
                f"Incomplete download ({received}/{expected_size} bytes)"
            )
        if expected_hash and sha.hexdigest() != expected_hash:
            raise ValueError("SHA256 mismatch: file rejected")

        os.replace(part_path, final_path)
    except Exception:
        try:
            os.remove(part_path)
        except OSError:
            pass
        raise

    log(f"[Update] Installer downloaded: {final_path} ({received} bytes)")
    return final_path


def launch(update_info=None):

    if is_dev_mode():
        print("[Launch] Development mode detected: download blocked.")
        return None

    try:
        if not update_info or not update_info.get("asset_url"):
            release = get_latest_release(timeout=10)
            if not release:
                return None
            update_info = _describe_release(release)

        return _download_installer(update_info)
    except Exception as e:
        log(f"[Update] Download failed: {e}")

        page = (update_info or {}).get("download_url")
        if page:
            webbrowser.open(page)

    return None


def apply_update(installer_path, on_exit=None):

    if is_dev_mode():
        print("[Update] Development mode detected: update installation aborted.")
        return False

    if (
        not installer_path
        or not os.path.isfile(installer_path)
        or os.path.getsize(installer_path) == 0
    ):
        log(f"[Update] Installer missing or empty: {installer_path}")
        return False

    if not hasattr(os, "startfile"):
        return False

    try:
        os.startfile(installer_path)  
    except Exception as e:
        log(f"[Update] Could not start installer: {e}")
        return False

    if on_exit is not None:
        on_exit()
        return True

    os._exit(0)