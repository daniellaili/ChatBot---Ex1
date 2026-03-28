"""Weather via Open-Meteo (no API key required)."""

from __future__ import annotations

import urllib.parse

import httpx

_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str) -> str:
    name = city.strip()
    if not name:
        return "Please specify a city."

    try:
        geo_params = urllib.parse.urlencode({"name": name, "count": 1, "language": "en", "format": "json"})
        with httpx.Client(timeout=15.0) as client:
            geo_resp = client.get(f"{_GEO_URL}?{geo_params}")
            geo_resp.raise_for_status()
            geo = geo_resp.json()
    except httpx.HTTPError as exc:
        return f"Geocoding service error: {exc}"
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
        with httpx.Client(timeout=15.0) as client:
            fc_resp = client.get(f"{_FORECAST_URL}?{fc_params}")
            fc_resp.raise_for_status()
            fc = fc_resp.json()
    except httpx.HTTPError as exc:
        return f"Weather service error: {exc}"
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
