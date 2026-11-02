"""Zero-cost, keyless external API and dataset tools for the Cloud AI Agent."""

import json
import os
import urllib.parse
import pandas as pd
import requests

HEADERS = {"User-Agent": "FreeCloudAgentGuide/1.0 (educational-project)"}
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_resources.csv")


def get_live_weather(city: str) -> str:
    """Fetches current real-time temperature and wind speed for any city worldwide.

    Args:
        city: City name such as 'Seattle', 'Tokyo', or 'Reykjavik'.
    """
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "format": "json"},
            timeout=8,
        ).json()
        if not geo.get("results"):
            return json.dumps({"error": f"City '{city}' not found."})

        loc = geo["results"][0]
        wx = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "current": "temperature_2m,apparent_temperature,wind_speed_10m",
            },
            timeout=8,
        ).json().get("current", {})
        return json.dumps({
            "location": f"{loc['name']}, {loc.get('country', '')}",
            "temperature_c": wx.get("temperature_2m"),
            "feels_like_c": wx.get("apparent_temperature"),
            "wind_kmh": wx.get("wind_speed_10m"),
            "source": "https://open-meteo.com/",
        })
    except Exception as exc:
        return json.dumps({"error": f"Weather API unavailable: {exc}"})


def lookup_wikipedia_summary(topic: str) -> str:
    """Retrieves a factual encyclopedia summary and link for a concept, person, or place.

    Args:
        topic: Subject title such as 'Ada Lovelace' or 'Cloud computing'.
    """
    try:
        slug = urllib.parse.quote(topic.strip().replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}"
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code != 200:
            return json.dumps({"error": f"No summary found for '{topic}'."})
        data = resp.json()
        page = data.get("content_urls", {}).get("desktop", {}).get("page", url)
        return json.dumps({
            "title": data.get("title"),
            "summary": data.get("extract"),
            "url": page,
        })
    except Exception as exc:
        return json.dumps({"error": f"Wikipedia lookup failed: {exc}"})


def search_study_dataset(keyword: str) -> str:
    """Searches the curated free AI & cloud CSV dataset by topic, title, or difficulty level.

    Args:
        keyword: Term like 'python', 'agents', 'cloud', 'deep-learning', or 'Beginner'.
    """
    try:
        df = pd.read_csv(CSV_PATH)
        q = keyword.strip().lower()
        mask = (
            df["topic"].str.lower().str.contains(q, na=False)
            | df["title"].str.lower().str.contains(q, na=False)
            | df["level"].str.lower().str.contains(q, na=False)
        )
        rows = df[mask] if mask.any() else df
        return rows.to_json(orient="records")
    except Exception as exc:
        return json.dumps({"error": f"Dataset read error: {exc}"})
