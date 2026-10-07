import json
from datetime import datetime
from zoneinfo import ZoneInfo

from adhanpy.PrayerTimes import PrayerTimes
from adhanpy.calculation import CalculationParameters, CalculationMethod

CONFIG = "config.json"

def compute_prayers(cfg, tz_name="Europe/Zurich"):
    loc = cfg["location"]
    coords = (float(loc["latitude"]), float(loc["longitude"]))
    tz = ZoneInfo(tz_name)

    # UOIF = Fajr 12° / Isha 12°, pas de méthode prédéfinie => paramètres custom
    params = CalculationParameters(fajr_angle=12, isha_angle=12)

    pt = PrayerTimes(coords, datetime.now(tz), calculation_parameters=params, time_zone=tz)

    fmt = lambda d: d.strftime("%H:%M")
    return {
        "fajr": fmt(pt.fajr),
        "duhr": fmt(pt.dhuhr),
        "asr": fmt(pt.asr),
        "maghrib": fmt(pt.maghrib),
        "icha": fmt(pt.isha),
    }

with open(CONFIG, encoding="utf-8") as f:
    cfg = json.load(f)

cfg["Prayer"] = compute_prayers(cfg)

with open(CONFIG, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=4, ensure_ascii=False)