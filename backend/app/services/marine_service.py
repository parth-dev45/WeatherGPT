from typing import Dict, Any
from ..schemas.models import MarineAdvisory

COASTAL_ZONES: Dict[str, Dict[str, Any]] = {
    "odisha": {
        "zone": "North Odisha & West Bengal Coast (Bay of Bengal)",
        "wave_height": 4.8,
        "sea_cond": "Rough to Very Rough",
        "wind_knots": 35.0,
        "warning": True,
        "msg": "RED WARNING: Fishermen are strictly advised not to venture into deep sea along and off Odisha-West Bengal coasts due to approaching cyclonic storm.",
        "high_tide": "14:25 IST (3.4m)",
        "low_tide": "20:40 IST (0.8m)"
    },
    "mumbai": {
        "zone": "Konkan & Mumbai Coast (Arabian Sea)",
        "wave_height": 3.2,
        "sea_cond": "Moderate to Rough",
        "wind_knots": 22.0,
        "warning": True,
        "msg": "ORANGE ADVISORY: High swell waves of 3.0 to 3.5 meters expected during high tide. Small boat fishermen advised to remain near harbor limits.",
        "high_tide": "12:50 IST (4.2m)",
        "low_tide": "19:15 IST (1.1m)"
    },
    "kerala": {
        "zone": "Malabar & South Kerala Coast",
        "wave_height": 2.5,
        "sea_cond": "Moderate",
        "wind_knots": 18.0,
        "warning": False,
        "msg": "YELLOW ALERT: Kallakkadal (Swell Surge) alert for coastal stretches. Maintain vigilance near beach fronts.",
        "high_tide": "11:10 IST (1.2m)",
        "low_tide": "17:30 IST (0.4m)"
    },
    "chennai": {
        "zone": "Coromandel Coast (Tamil Nadu)",
        "wave_height": 1.6,
        "sea_cond": "Slight to Moderate",
        "wind_knots": 12.0,
        "warning": False,
        "msg": "Normal fishing operations permitted. Sea surface temp 29.5°C.",
        "high_tide": "10:45 IST (1.1m)",
        "low_tide": "16:50 IST (0.3m)"
    }
}

def get_marine_advisory(location_str: str) -> MarineAdvisory:
    """Generates ocean state forecast and fisherman warnings."""
    clean = location_str.lower()
    sel = COASTAL_ZONES["mumbai"]
    
    if "odisha" in clean or "puri" in clean or "bengal" in clean or "kolkata" in clean or "vizag" in clean:
        sel = COASTAL_ZONES["odisha"]
    elif "kerala" in clean or "kochi" in clean or "trivandrum" in clean:
        sel = COASTAL_ZONES["kerala"]
    elif "chennai" in clean or "tamil" in clean or "puducherry" in clean:
        sel = COASTAL_ZONES["chennai"]

    return MarineAdvisory(
        coastal_zone=sel["zone"],
        wave_height_m=sel["wave_height"],
        sea_condition=sel["sea_cond"],
        wind_speed_knots=sel["wind_knots"],
        fisherman_warning=sel["warning"],
        warning_message=sel["msg"],
        high_tide_time=sel["high_tide"],
        low_tide_time=sel["low_tide"]
    )
