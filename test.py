import json
from datetime import datetime
from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes
from adhanpy.calculation import CalculationParameters

with open("config.json", encoding="utf-8") as f:
    cfg = json.load(f)

lat = float(cfg["location"]["latitude"])
lon = float(cfg["location"]["longitude"])

tz = ZoneInfo("Europe/Paris")
params = CalculationParameters(fajr_angle=12, isha_angle=12)
pt = PrayerTimes((lat, lon), datetime.now(tz), calculation_parameters=params, time_zone=tz)

print(pt.fajr.strftime("%H:%M"), pt.dhuhr.strftime("%H:%M"), pt.asr.strftime("%H:%M"), pt.maghrib.strftime("%H:%M"), pt.isha.strftime("%H:%M"))