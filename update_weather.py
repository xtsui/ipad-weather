from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


PARAMETERS = {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "current": ",".join([
        "temperature_2m",
        "apparent_temperature",
        "weather_code",
        "wind_speed_10m",
        "is_day",
    ]),
    "daily": ",".join([
        "weather_code",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_probability_max",
    ]),
    "temperature_unit": "celsius",
    "wind_speed_unit": "kmh",
    "timezone": "Europe/Paris",
    "forecast_days": 5,
}

API_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    + urlencode(PARAMETERS)
)

request = Request(
    API_URL,
    headers={
        "User-Agent": "ipad-weather-dashboard/1.0"
    },
)

with urlopen(request, timeout=30) as response:
    weather_data = json.load(response)

weather_data["generated_at_utc"] = (
    datetime.now(timezone.utc)
    .replace(microsecond=0)
    .isoformat()
    .replace("+00:00", "Z")
)

javascript = (
    "window.WEATHER_DATA = "
    + json.dumps(
        weather_data,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    + ";\n"
)

Path("weather-data.js").write_text(
    javascript,
    encoding="utf-8",
)

print("weather-data.js updated")
