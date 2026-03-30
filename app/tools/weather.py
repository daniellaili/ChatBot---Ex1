"""Weather via Open-Meteo (no API key required)."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str) -> str:
    name = city.strip()
    if not name:
        return "Please specify a city."

    try:
        geo_params = urllib.parse.urlencode({"name": name, "count": 1, "language": "en", "format": "json"})
        with urllib.request.urlopen("{0}?{1}".format(_GEO_URL, geo_params), timeout=15) as response:
            geo = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return "Geocoding service error: {0}".format(exc)
    except urllib.error.URLError as exc:
        return "Geocoding service unavailable: {0}".format(exc.reason)
    except ValueError:
        return "Geocoding service returned invalid data."

    results = geo.get("results")
    if not results:
        return f"Could not find a location named '{name}'."

    first = results[0]
    lat = first.get("latitude")
    lon = first.get("longitude")
    label = first.get("name", name)
    country = first.get("country", "")
    admin = first.get("admin1", "")
    if lat is None or lon is None:
        return "Geocoding response missing coordinates."

    try:
        fc_params = urllib.parse.urlencode(
            {
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "timezone": "auto",
            }
        )
        with urllib.request.urlopen("{0}?{1}".format(_FORECAST_URL, fc_params), timeout=15) as response:
            fc = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return "Weather service error: {0}".format(exc)
    except urllib.error.URLError as exc:
        return "Weather service unavailable: {0}".format(exc.reason)
    except ValueError:
        return "Weather service returned invalid data."

    current = fc.get("current_weather") or {}
    temp = current.get("temperature")
    wind = current.get("windspeed")
    code = current.get("weathercode")
    time_utc = current.get("time", "")

    place = label
    if admin:
        place = f"{label}, {admin}"
    if country:
        place = f"{place}, {country}"

    if temp is None:
        return f"Could not read current weather for {place}."

    parts = [f"Current weather in {place}: {temp} degrees C"]
    if wind is not None:
        parts.append(f"wind {wind} km/h")
    if code is not None:
        parts.append(f"condition code {code}")
    if time_utc:
        parts.append(f"(observation {time_utc})")
    return ". ".join(parts) + "."
