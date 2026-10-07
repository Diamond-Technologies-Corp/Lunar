import json
from datetime import date, datetime
from pathlib import Path

from adhanpy.PrayerTimes import PrayerTimes
from adhanpy.calculation import CalculationMethod

CONFIG_PATH = Path(__file__).parent / "config.json"

METHODS = {
    "Muslim World League (Fajr 18° / Isha 17°)": CalculationMethod.MUSLIM_WORLD_LEAGUE,
    "ISNA (15° / 15°)": CalculationMethod.NORTH_AMERICA,
    "Egyptian (19.5° / 17.5°)": CalculationMethod.EGYPTIAN,
    "Karachi (18° / 18°)": CalculationMethod.KARACHI,
    "Umm al-Qura (18.5° / 90 min after Maghrib)": CalculationMethod.UMM_AL_QURA,
    "UOIF (12° / 12°)": CalculationMethod.UOIF,
}


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def compute_prayer_times(config: dict, day: date | None = None) -> dict:
    loc = config["location"]
    day = day or date.today()

    method = METHODS.get(loc["method"])
    if method is None:
        raise ValueError(f"Méthode de calcul inconnue : {loc['method']}")

    tz = datetime.now().astimezone().tzinfo

    pt = PrayerTimes(
        (loc["latitude"], loc["longitude"]),
        day,
        calculation_method=method,
        time_zone=tz,
    )

    return {
        "fajr": pt.fajr.strftime("%H:%M"),
        "duhr": pt.dhuhr.strftime("%H:%M"),
        "asr": pt.asr.strftime("%H:%M"),
        "maghrib": pt.maghrib.strftime("%H:%M"),
        "icha": pt.isha.strftime("%H:%M"),
    }


def run_computation() -> dict:
    config = load_config()
    config["Prayer"] = compute_prayer_times(config)
    save_config(config)
    return config["Prayer"]


if __name__ == "__main__":
    prayers = run_computation()
    for name, hour in prayers.items():
        print(f"{name:8} {hour}")