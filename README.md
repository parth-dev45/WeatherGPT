# 🌦️ WeatherGPT: Conversational AI for Weather Forecasting, Alerts & Climate Information

> **Problem Statement ID**: 26068  
> **Organization**: Ministry of Earth Sciences (MoES) / India Meteorological Department (IMD)  
> **Theme**: Disaster Management  
> **Category**: Software  

---

## 🌟 Overview
**WeatherGPT** is a conversational AI and early warning decision-support platform designed to democratize complex meteorological datasets, numerical weather prediction (NWP) model outputs (GFS/WRF), disaster warnings, and agricultural advisories through natural language in **10+ Indian regional languages** with **voice interaction**.

---

## 🚀 Key Modules & Capabilities

1. **💬 Multimodal Conversational AI Engine**:
   - Natural language weather querying in Hindi, Marathi, Tamil, Telugu, Bengali, Gujarati, Punjabi, Kannada, and English.
   - Built-in Web Speech API microphone for Speech-to-Text (STT) and Indic Text-to-Speech (TTS) audio narration.
   - Intent classification and automated entity/location extraction across India.

2. **🗺️ Interactive GIS Doppler Radar & Cyclone Tracking Map**:
   - Leaflet-powered GIS engine with simulated IMD Doppler Weather Radar (DWR) precipitation circles.
   - Live Cyclone VAAYU track line and 48-hour cone of uncertainty.
   - Color-coded ITU CAP alert circles for Red, Orange, and Yellow warning zones.

3. **🌾 Agromet Advisory & Farmer Decision Support (Meghdoot Standard)**:
   - Tailored crop protection guidance for Paddy, Cotton, Wheat, Sugarcane, Soybean, and Mustard.
   - Actionable irrigation advice, pesticide spray timing, and harvest safety windows.
   - Integrated Damini Lightning Sensor risk indicator.

4. **🚨 ITU CAP v1.2 Early Warning Disaster Hub**:
   - Standardized Common Alerting Protocol (ITU-T X.1303) and WMO WIS2.0 subscriber architecture.
   - Official IMD disaster response instructions and audio emergency broadcast buzzer.

5. **✈️ Aviation & Marine Intelligence**:
   - Real-time METAR and 24-hour TAF decoder with flight category classifications (VFR, MVFR, IFR, LIFR).
   - INCOIS Ocean State Forecasts, significant wave heights, swell surge warnings, and fisherman advisories.

6. **📈 Multi-Decadal Historical Climate Analytics**:
   - 1970–2026 decadal temperature anomalies against the 1961–1990 IMD baseline normal.
   - Southwest Monsoon rainfall departure vs 880.6mm Long Period Average (LPA).

---

## 🛠️ Architecture & Tech Stack

```
[ Frontend (React 19 + Vite + Leaflet) ]  <--->  [ FastAPI Backend (Python 3.14) ]
   - Glassmorphic Dark UI                           - LLM Tool Calling & Routing Engine
   - Indic Web Speech STT/TTS                       - Open-Meteo & IMD Telemetry API
   - Persona Switcher                               - ITU CAP v1.2 Alert Generator
   - CartoDB DarkMatter GIS                         - Agromet & Aviation Decoders
```

---

## ⚡ How to Run Locally on macOS

### 1. Start the FastAPI Backend Server
```bash
cd backend
source ../venv/bin/activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be available at: `http://127.0.0.1:8000/docs`

### 2. Start the React Frontend Application
```bash
cd frontend
npm install
npm run dev
```
Open your browser at: **`http://localhost:5173`**

---

## 🌐 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/chat/query` | Process conversational natural language weather queries |
| `GET` | `/api/weather/current` | Real-time observations and 7-day hourly/daily forecast |
| `GET` | `/api/alerts/active` | Active ITU CAP severe weather early warning bulletins |
| `GET` | `/api/alerts/cyclone-track`| GeoJSON track coordinates for active cyclones |
| `GET` | `/api/advisory/crop` | Agromet crop-specific advisories for farmers |
| `GET` | `/api/aviation/briefing`| Decoded METAR/TAF aerodrome weather reports |
| `GET` | `/api/marine/advisory` | INCOIS ocean wave heights and fisherman warnings |
| `GET` | `/api/climate/trends` | 50-year temperature anomalies and monsoon departure |
