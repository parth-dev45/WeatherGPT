import asyncio
from typing import Optional, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from .schemas.models import (
    WeatherQueryRequest, ChatResponse, WeatherData, CAPAlert,
    AgriCropAdvisory, AviationBriefing, MarineAdvisory, CityComparisonData
)
from .services.weather_service import (
    geocode_location, fetch_weather_data, compare_locations, 
    search_locations_autocomplete, REGIONAL_TALUKA_EXPLORER
)
from .services.alert_service import get_active_alerts, get_cyclone_track_geojson
from .services.agri_advisory import generate_crop_advisory, CROP_DATABASE
from .services.aviation_service import get_aviation_briefing
from .services.marine_service import get_marine_advisory
from .services.historical_service import get_climate_trend_data
from .services.llm_engine import process_conversational_query

app = FastAPI(
    title="WeatherGPT API Backend",
    description="Conversational AI Platform for Weather Forecasting, Alerts, and Climate Information (MoES / IMD #26068)",
    version="1.0.0"
)

# Enable CORS for local React/Vite development and mobile PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active WebSocket connections for real-time WMO WIS2.0 / CAP disaster alerts
active_connections: List[WebSocket] = []

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "WeatherGPT Engine",
        "version": "1.0.0",
        "standards": ["ITU CAP v1.2", "WMO WIS2.0", "IMD GFS-WRF Ensemble"]
    }

@app.post("/api/chat/query", response_model=ChatResponse)
def handle_chat_query(req: WeatherQueryRequest):
    """Processes natural language weather queries in English & Indian languages."""
    return process_conversational_query(req)

@app.get("/api/locations/search")
def search_locations(
    q: str = Query(..., description="Query text for city, taluka, tehsil, or micro-locality"),
    limit: int = Query(8, description="Maximum number of suggestions")
):
    """Returns instant autocomplete suggestions across 450+ Indian talukas, districts, and towns."""
    return search_locations_autocomplete(q, limit)

@app.get("/api/locations/regional-explorer")
def get_regional_talukas(region: str = Query("pune", description="Region or city name")):
    """Returns list of popular sub-areas / talukas for the given metro/district."""
    reg = region.lower().strip()
    return REGIONAL_TALUKA_EXPLORER.get(reg, REGIONAL_TALUKA_EXPLORER.get("pune", []))

@app.get("/api/weather/current", response_model=WeatherData)
def get_current_weather(
    location: str = Query("Pune", description="City, taluka, or district name"),
    lat: Optional[float] = None,
    lon: Optional[float] = None
):
    """Retrieves real-time telemetry, 24-hour future hourly & 7-day NWP forecast."""
    if lat is None or lon is None:
        lat, lon, proper_name, state_name = geocode_location(location)
    else:
        proper_name = location
        state_name = "India"
    return fetch_weather_data(lat, lon, proper_name, state_name)

@app.get("/api/weather/compare", response_model=CityComparisonData)
def get_weather_comparison(
    city1: str = Query("Mumbai", description="First city for comparison"),
    city2: str = Query("Delhi", description="Second city for comparison")
):
    """Compares weather, AQI, travel route safety, and health personas between two cities."""
    return compare_locations(city1, city2)

@app.get("/api/alerts/active", response_model=List[CAPAlert])
def get_alerts(
    state: Optional[str] = None,
    district: Optional[str] = None,
    severity: Optional[str] = None
):
    """Retrieves active early warning CAP bulletins (cyclone, heatwave, floods)."""
    return get_active_alerts(state, district, severity)

@app.get("/api/alerts/cyclone-track")
def get_cyclone_track():
    """Returns active cyclone GeoJSON coordinate track and cone of uncertainty."""
    return get_cyclone_track_geojson()

@app.get("/api/advisory/crop", response_model=AgriCropAdvisory)
def get_crop_advisory(
    crop: str = Query("paddy", description="Crop name (paddy, cotton, wheat, sugarcane, etc.)"),
    district: str = Query("Nagpur", description="District name"),
    state: str = Query("Maharashtra", description="State name")
):
    """Generates localized Agromet farming advisory."""
    lat, lon, proper_name, state_name = geocode_location(district)
    weather = fetch_weather_data(lat, lon, proper_name, state_name)
    rain_prob = weather.hourly[0].rain_prob if weather.hourly else 20
    return generate_crop_advisory(crop, proper_name, state_name, weather.current_temp, rain_prob, weather.humidity)

@app.get("/api/advisory/crops-list")
def get_supported_crops():
    """Returns list of supported agricultural crops for advisories."""
    return list(CROP_DATABASE.keys())

@app.get("/api/aviation/briefing", response_model=AviationBriefing)
def get_aviation_weather(airport: str = Query("VIDP", description="Airport ICAO code or city name")):
    """Decodes METAR and TAF for aviation dispatchers and pilots."""
    return get_aviation_briefing(airport)

@app.get("/api/marine/advisory", response_model=MarineAdvisory)
def get_marine_weather(location: str = Query("Mumbai", description="Coastal city or port")):
    """Retrieves INCOIS ocean state forecasts and fisherman warnings."""
    return get_marine_advisory(location)

@app.get("/api/climate/trends")
def get_climate_trends(region: str = Query("All India", description="Region for climate trend analysis")):
    """Returns multi-decadal temperature anomaly and monsoon departure metrics."""
    return get_climate_trend_data(region)

@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    """WebSocket stream for broadcasting live WMO WIS2.0 / CAP disaster alerts."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep-alive heartbeat
            data = await websocket.receive_text()
            await websocket.send_json({
                "type": "heartbeat_ack",
                "active_alerts_count": len(get_active_alerts())
            })
    except WebSocketDisconnect:
        active_connections.remove(websocket)
