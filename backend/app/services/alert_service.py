import datetime
from typing import List, Dict, Any, Optional
from ..schemas.models import CAPAlert

# Standard ITU CAP v1.2 Alerts for Disaster Management & WIS2.0 early warning
SAMPLE_CAP_ALERTS: List[CAPAlert] = [
    CAPAlert(
        id="IMD-CAP-2026-CY01",
        headline="RED ALERT: Severe Cyclonic Storm 'VAAYU' approaching Coastal Odisha & West Bengal",
        event="Tropical Cyclone",
        severity="Red",
        urgency="Immediate",
        certainty="Observed",
        area_desc="Coastal Districts of Puri, Jagatsinghpur, Kendrapara, Balasore & South 24 Parganas",
        district="Puri",
        state="Odisha",
        lat=19.8135,
        lon=85.8312,
        effective=datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST"),
        expires=(datetime.datetime.now() + datetime.timedelta(hours=36)).strftime("%Y-%m-%d %H:%M IST"),
        instruction="Total suspension of fishing operations. Mobilize NDRF/SDRF teams. Evacuation of low-lying coastal populations to cyclone shelters. Expected wind gusts 110-120 kmph.",
        sender_name="Cyclone Warning Division, IMD New Delhi",
        color="#EF4444"
    ),
    CAPAlert(
        id="IMD-CAP-2026-HW04",
        headline="ORANGE ALERT: Severe Heatwave Conditions over Vidarbha & West Rajasthan",
        event="Severe Heat Wave",
        severity="Orange",
        urgency="Expected",
        certainty="Likely",
        area_desc="Nagpur, Chandrapur, Akola, Bikaner, Jaisalmer and surrounding tehsils",
        district="Nagpur",
        state="Maharashtra",
        lat=21.1458,
        lon=79.0882,
        effective=datetime.datetime.now().strftime("%Y-%m-%d 08:00 IST"),
        expires=(datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d 20:00 IST"),
        instruction="Avoid direct sunlight exposure between 11:30 AM to 3:30 PM. High risk of heat stroke for outdoor workers and elderly. Maintain oral rehydration (ORS, buttermilk).",
        sender_name="Regional Meteorological Centre, Nagpur",
        color="#F97316"
    ),
    CAPAlert(
        id="IMD-CAP-2026-HR09",
        headline="ORANGE ALERT: Extremely Heavy Rainfall & Flash Flood Risk in Konkan & Ghats",
        event="Heavy Rain / Flash Flood",
        severity="Orange",
        urgency="Immediate",
        certainty="Likely",
        area_desc="Mumbai, Thane, Raigad, Ratnagiri and Pune Ghat sections",
        district="Mumbai",
        state="Maharashtra",
        lat=19.0760,
        lon=72.8777,
        effective=datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST"),
        expires=(datetime.datetime.now() + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M IST"),
        instruction="Isolated rainfall exceeding 180mm expected in 24 hours. Waterlogging in low-lying railway tracks and urban transit corridors. Avoid traveling to water bodies.",
        sender_name="Regional Meteorological Centre, Mumbai",
        color="#F97316"
    ),
    CAPAlert(
        id="IMD-CAP-2026-TS12",
        headline="YELLOW ALERT: Isolated Thunderstorm with Lightning & Hailstorm in Punjab & Haryana",
        event="Thunderstorm / Hailstorm",
        severity="Yellow",
        urgency="Expected",
        certainty="Possible",
        area_desc="Ludhiana, Patiala, Ambala, Karnal and adjoining agrarian belts",
        district="Ludhiana",
        state="Punjab",
        lat=30.9010,
        lon=75.8573,
        effective=datetime.datetime.now().strftime("%Y-%m-%d 14:00 IST"),
        expires=(datetime.datetime.now() + datetime.timedelta(hours=18)).strftime("%Y-%m-%d 06:00 IST"),
        instruction="Take shelter inside pucca structures. Do not stand under isolated trees or near high-tension electrical masts. Farmers advised to protect harvested grains in mandis.",
        sender_name="Meteorological Centre, Chandigarh",
        color="#EAB308"
    ),
    CAPAlert(
        id="IMD-CAP-2026-LN05",
        headline="DAMINI ALERT: Cloud-to-Ground Lightning Strikes detected within 25km radius",
        event="Severe Lightning Strike Risk",
        severity="Orange",
        urgency="Immediate",
        certainty="Observed",
        area_desc="Varanasi, Mirzapur, Sonbhadra, Patna Rural",
        district="Varanasi",
        state="Uttar Pradesh",
        lat=25.3176,
        lon=82.9739,
        effective=datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST"),
        expires=(datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M IST"),
        instruction="Immediate lightning alert from IITM Damini Lightning Sensor Network. Stay indoors. Avoid handling metal agricultural equipment in open fields.",
        sender_name="IITM Pune / IMD Lightning Detection Network",
        color="#F97316"
    )
]

def get_active_alerts(state: Optional[str] = None, district: Optional[str] = None, severity: Optional[str] = None) -> List[CAPAlert]:
    """Retrieves active early warning disaster alerts matching filters."""
    alerts = SAMPLE_CAP_ALERTS.copy()
    if state:
        alerts = [a for a in alerts if state.lower() in a.state.lower() or state.lower() in a.area_desc.lower()]
    if district:
        alerts = [a for a in alerts if district.lower() in a.district.lower() or district.lower() in a.area_desc.lower()]
    if severity:
        alerts = [a for a in alerts if a.severity.lower() == severity.lower()]
    return alerts if alerts else SAMPLE_CAP_ALERTS[:3]

def get_cyclone_track_geojson() -> Dict[str, Any]:
    """Returns simulated active cyclone track and cone of uncertainty in GeoJSON format."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [89.5, 14.2],
                        [88.2, 16.0],
                        [86.9, 17.8],
                        [85.8, 19.8], # Current
                        [84.9, 21.5], # 24h Forecast
                        [84.2, 23.0]  # 48h Forecast
                    ]
                },
                "properties": {
                    "name": "Cyclone VAAYU Track",
                    "intensity": "Very Severe Cyclonic Storm",
                    "max_winds_kmph": 120,
                    "landfall_point": "Near Puri, Odisha Coast"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [85.8312, 19.8135]
                },
                "properties": {
                    "name": "Current Center Position (19.8°N, 85.8°E)",
                    "pressure_hpa": 984,
                    "movement_speed": "16 km/h NNW"
                }
            }
        ]
    }
