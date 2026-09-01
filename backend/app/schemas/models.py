from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class WeatherQueryRequest(BaseModel):
    query: str = Field(..., description="User natural language question in English, Hindi, Marathi, Tamil, etc.")
    language: Optional[str] = Field("auto", description="ISO language code or 'auto'")
    persona: Optional[str] = Field("general", description="User persona: 'general', 'farmer', 'aviation', 'marine', 'disaster_manager'")
    lat: Optional[float] = Field(None, description="Optional latitude for location grounding")
    lon: Optional[float] = Field(None, description="Optional longitude for location grounding")
    location_name: Optional[str] = Field(None, description="Explicit city/district name if known")

class WeatherMetric(BaseModel):
    label: str
    value: str
    unit: str
    icon: Optional[str] = None
    status: Optional[str] = None

class HourlyForecast(BaseModel):
    time: str
    temp: float
    rain_prob: int
    condition: str
    icon: str
    wind_speed: float

class DailyForecast(BaseModel):
    date: str
    day: str
    temp_max: float
    temp_min: float
    condition: str
    icon: str
    rain_sum: float
    wind_max: float

class WeatherData(BaseModel):
    location: str
    state: str
    country: str = "India"
    lat: float
    lon: float
    current_temp: float
    feels_like: float
    condition: str
    condition_code: int
    humidity: int
    wind_speed: float
    wind_direction: str
    precipitation: float
    pressure: float
    uv_index: float
    visibility: float
    aqi: int
    aqi_status: str
    sunrise: str
    sunset: str
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]
    nwp_model: str = "GFS-WRF Ensemble (0.125° Res)"

class CAPAlert(BaseModel):
    id: str
    headline: str
    event: str
    severity: str  # Red, Orange, Yellow, Green
    urgency: str   # Immediate, Expected, Future
    certainty: str # Observed, Likely, Possible
    area_desc: str
    district: str
    state: str
    lat: float
    lon: float
    effective: str
    expires: str
    instruction: str
    sender_name: str = "India Meteorological Department (MoES)"
    color: str

class AgriCropAdvisory(BaseModel):
    crop: str
    district: str
    state: str
    growth_stage: str
    weather_summary: str
    rainfall_risk: str
    irrigation_advice: str
    pesticide_advice: str
    harvest_recommendation: str
    damini_lightning_alert: bool = False
    suitability_score: int

class AviationBriefing(BaseModel):
    station_icao: str
    station_name: str
    metar_raw: str
    metar_decoded: Dict[str, Any]
    taf_raw: str
    flight_category: str  # VFR, MVFR, IFR, LIFR
    hazards: List[str]

class MarineAdvisory(BaseModel):
    coastal_zone: str
    wave_height_m: float
    sea_condition: str
    wind_speed_knots: float
    fisherman_warning: bool
    warning_message: str
    high_tide_time: str
    low_tide_time: str

class ChatResponse(BaseModel):
    query: str
    detected_language: str
    persona: str
    speech_text: str
    markdown_response: str
    structured_weather: Optional[WeatherData] = None
    alerts: Optional[List[CAPAlert]] = None
    agri_advisory: Optional[AgriCropAdvisory] = None
    aviation_briefing: Optional[AviationBriefing] = None
    marine_advisory: Optional[MarineAdvisory] = None
    quick_suggestions: List[str]
    suggested_actions: List[Dict[str, str]]
