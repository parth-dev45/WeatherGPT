import re
import datetime
from typing import Dict, Any, Tuple, Optional, List
from .weather_service import geocode_location, fetch_weather_data, INDIAN_LOCATIONS
from .alert_service import get_active_alerts
from .agri_advisory import generate_crop_advisory
from .aviation_service import get_aviation_briefing
from .marine_service import get_marine_advisory
from .historical_service import get_climate_trend_data
from ..schemas.models import WeatherQueryRequest, ChatResponse, WeatherData

# Indic regional name transliteration mappings
INDIC_LOCATION_TRANSLITERATIONS = {
    "पुणे": "Pune",
    "मुंबई": "Mumbai",
    "बम्बई": "Mumbai",
    "दिल्ली": "Delhi",
    "नई दिल्ली": "New Delhi",
    "नागपूर": "Nagpur",
    "नागपुर": "Nagpur",
    "नाशिक": "Nashik",
    "नासिक": "Nashik",
    "सोलापूर": "Solapur",
    "सोलापुर": "Solapur",
    "कोल्हापूर": "Kolhapur",
    "छत्रपती संभाजीनगर": "Aurangabad",
    "संभाजीनगर": "Aurangabad",
    "औरंगाबाद": "Aurangabad",
    "जालना": "Jalna",
    "लातूर": "Latur",
    "लातुर": "Latur",
    "सांगली": "Sangli",
    "सातारा": "Satara",
    "बारामती": "Baramati",
    "बीड": "Beed",
    "अमरावती": "Amravati",
    "अकोला": "Akola",
    "जळगाव": "Jalgaon",
    "परभणी": "Parbhani",
    "नांदेड": "Nanded",
    "चंद्रपूर": "Chandrapur",
    "रत्नागिरी": "Ratnagiri",
    "सिंधुदुर्ग": "Sindhudurg",
    "अलिबाग": "Alibag",
    "ठाणे": "Thane",
    "चेन्नई": "Chennai",
    "कोलकाता": "Kolkata",
    "कलकत्ता": "Kolkata",
    "बेंगळुरू": "Bengaluru",
    "बैंगलोर": "Bengaluru",
    "बेंगलुरु": "Bengaluru",
    "हैदराबाद": "Hyderabad",
    "जयपूर": "Jaipur",
    "जयपुर": "Jaipur",
    "जोधपूर": "Jodhpur",
    "उदयपूर": "Udaipur",
    "अलवर": "Alwar",
    "लखनौ": "Lucknow",
    "लखनऊ": "Lucknow",
    "पाटणा": "Patna",
    "पटना": "Patna",
    "भोपाळ": "Bhopal",
    "भोपाल": "Bhopal",
    "इंदौर": "Indore",
    "ग्वालियर": "Gwalior",
    "जबलपूर": "Jabalpur",
    "उज्जैन": "Ujjain",
    "चंदीगड": "Chandigarh",
    "चंडीगढ़": "Chandigarh",
    "लुधियाना": "Ludhiana",
    "अमृतसर": "Amritsar",
    "वाराणसी": "Varanasi",
    "बनारस": "Varanasi",
    "कानपूर": "Kanpur",
    "कानपुर": "Kanpur",
    "झांसी": "Jhansi",
    "झांशी": "Jhansi",
    "प्रयागराज": "Prayagraj",
    "इलाहाबाद": "Prayagraj",
    "अयोध्या": "Ayodhya",
    "अहमदाबाद": "Ahmedabad",
    "सूरत": "Surat",
    "वडोदरा": "Vadodara",
    "राजकोट": "Rajkot",
    "गुवाहाटी": "Guwahati",
    "कोची": "Kochi",
    "कोचीन": "Kochi",
    "कोझिकोड": "Kozhikode",
    "तिरुवनंतपुरम": "Thiruvananthapuram",
    "वायनाड": "Wayanad",
    "विशाखापट्टनम": "Visakhapatnam",
    "वाइजाग": "Visakhapatnam",
    "विजयवाडा": "Vijayawada",
    "तिरुपती": "Tirupati",
    "वारंगल": "Warangal",
    "पुरी": "Puri",
    "भुवनेश्वर": "Bhubaneswar",
    "कटक": "Cuttack",
    "राउरकेला": "Rourkela",
    "संबलपूर": "Sambalpur",
    "श्रीनगर": "Srinagar",
    "जम्मू": "Jammu",
    "शिमला": "Shimla",
    "मनाली": "Manali",
    "धर्मशाला": "Dharamshala",
    "देहरादून": "Dehradun",
    "ऋषिकेश": "Rishikesh",
    "हरिद्वार": "Haridwar",
    "नैनीताल": "Nainital",
    "रांची": "Ranchi",
    "जमशेदपूर": "Jamshedpur",
    "धनबाद": "Dhanbad",
    "रायपूर": "Raipur",
    "बिलासपुर": "Bilaspur",
    "गोवा": "Panaji",
    "पणजी": "Panaji",
    "लेह": "Leh"
}

LANGUAGE_MAP = {
    "hi": ["मौसम", "बारिश", "तापमान", "हवा", "गर्मी", "फसल", "धान", "गेहूं", "अलर्ट", "बिजली", "आज", "कल", "होगा", "बताओ", "क्या"],
    "mr": ["हवामान", "पाऊस", "तापमान", "शेतकरी", "पीक", "कापूस", "सोयाबीन", "ऊन", "सांगा", "कसे", "आहे"],
    "ta": ["வானிலை", "மழை", "வெப்பநிலை", "விவசாயம்", "காற்று", "புயல்", "இன்று", "நாளை"],
    "te": ["వాతావరణం", "వర్షం", "ఉష్ణోగ్రత", "పంట", "రైతు", "గాలి", "హెచ్చరిక"],
    "bn": ["আবহাওয়া", "বৃষ্টি", "তাপমাত্রা", "ঘূর্ণিঝড়", "আজ", "কাল", "কেমন"],
    "gu": ["હવામાન", "વરસાદ", "તાપમાન", "ખેડૂત", "પાક", "આગાહી"],
    "pa": ["ਮੌਸਮ", "ਮੀਂਹ", "ਤਾਪਮਾਨ", "ਕਣਕ", "ਝੋਨਾ", "ਕੱਲ੍ਹ"],
    "kn": ["ಹವಾಮಾನ", "ಮಳೆ", "ತಾಪಮಾನ", "ಬೆಳೆ", "ರೈತ"]
}

def detect_language(text: str) -> str:
    """Detects Indian regional language or English."""
    for lang, keywords in LANGUAGE_MAP.items():
        for kw in keywords:
            if kw in text:
                return lang
    for char in text:
        code = ord(char)
        if 0x0900 <= code <= 0x097F:
            return "hi"
        elif 0x0B80 <= code <= 0x0BFF:
            return "ta"
        elif 0x0C00 <= code <= 0x0C7F:
            return "te"
        elif 0x0980 <= code <= 0x09FF:
            return "bn"
        elif 0x0A80 <= code <= 0x0AFF:
            return "gu"
        elif 0x0A00 <= code <= 0x0A7F:
            return "pa"
        elif 0x0C80 <= code <= 0x0CFF:
            return "kn"
    return "en"

STOPWORDS = {
    "what", "is", "the", "weather", "forecast", "temperature", "rain", "rainfall", 
    "heavy", "how", "hot", "cold", "now", "right", "today", "tomorrow", "tonight", 
    "this", "week", "will", "it", "in", "at", "near", "for", "around", "over", "of", 
    "and", "to", "tell", "me", "show", "give", "update", "condition", "status", 
    "kaisa", "hai", "hoga", "kya", "padega", "aaj", "kal", "ka", "ki", "ke", "liye",
    "crop", "agri", "farming", "cotton", "paddy", "wheat", "sugarcane", "pesticide",
    "please", "can", "you", "check", "current", "live", "about", "details", "info"
}

def extract_location_from_query(text: str, fallback_loc: Optional[str] = None) -> str:
    """Extracts location with multi-stage entity resolution."""
    lowered = text.lower()
    
    # 1. Match against known 250+ Indian cities and districts
    sorted_cities = sorted(INDIAN_LOCATIONS.keys(), key=len, reverse=True)
    for city_key in sorted_cities:
        pattern = r'\b' + re.escape(city_key) + r'\b'
        if re.search(pattern, lowered):
            return city_key.title()

    # 2. Check Indic Devanagari / Regional words
    for indic_name, eng_city in INDIC_LOCATION_TRANSLITERATIONS.items():
        if indic_name in text:
            return eng_city

    # 3. Regex extraction: 'in <City>', 'at <City>', 'near <City>', 'for <City>'
    match = re.search(r'\b(?:in|at|near|for|around|over|of)\s+([A-Za-z]+)', text, re.IGNORECASE)
    if match:
        cand = match.group(1).strip()
        if cand.lower() not in STOPWORDS and len(cand) >= 3:
            return cand.title()

    # 4. Tokenize and test isolated candidate words
    clean_tokens = re.findall(r'\b[A-Za-z]{3,}\b', text)
    candidate_tokens = [w for w in clean_tokens if w.lower() not in STOPWORDS]
    if candidate_tokens:
        return candidate_tokens[0].title()

    # 5. Fallback context
    if fallback_loc and fallback_loc.strip() and fallback_loc.lower() not in ["your location", "auto", ""]:
        return fallback_loc.strip().title()

    return "New Delhi"

def format_human_weather_story(weather: WeatherData, proper_name: str, state_name: str) -> str:
    """Generates an articulate, executive intelligence summary for the user."""
    today = weather.daily[0] if weather.daily else None
    max_t = today.temp_max if today else weather.current_temp + 4
    min_t = today.temp_min if today else weather.current_temp - 4
    rain_p = weather.hourly[0].rain_prob if weather.hourly else 10
    
    # Rain description
    if weather.precipitation > 5.0 or rain_p > 60:
        rain_desc = f"**Heavy to moderate rainfall spells** are active with an elevated rain probability of **{rain_p}%**."
    elif weather.precipitation > 0.1 or rain_p > 30:
        rain_desc = f"Passing light showers are possible (**{rain_p}% probability**) with {weather.precipitation} mm precipitation."
    else:
        rain_desc = f"Dry conditions are expected to prevail (**{rain_p}% rain probability**) with negligible precipitation."

    # Comfort / Heat index description
    if weather.current_temp > 38.0:
        comfort = f"⚠️ **High thermal discomfort**: Ambient temperature is elevated at **{weather.current_temp}°C** (feels like **{weather.feels_like}°C**). Sun protection and hydration are recommended."
    elif weather.current_temp < 15.0:
        comfort = f"❄️ **Cool and pleasant weather**: Morning temperatures dip to **{min_t}°C**."
    else:
        comfort = f"Current conditions are **{weather.condition}** with a comfortable temperature of **{weather.current_temp}°C** (feels like **{weather.feels_like}°C**)."

    # Wind and AQI description
    wind_desc = f"Surface winds are blowing from the **{weather.wind_direction}** at **{weather.wind_speed} km/h**. Relative humidity is at **{weather.humidity}%** with atmospheric pressure of **{weather.pressure} hPa**."
    aqi_desc = f"Air Quality Index (AQI) is **{weather.aqi}**, categorized as **{weather.aqi_status}**."

    return (
        f"### 🌤️ Weather Intelligence: **{proper_name}, {state_name}**\n\n"
        f"{comfort}\n\n"
        f"**Key Forecast Highlights:**\n"
        f"- 🌡️ **Temperature Range:** Low of **{min_t}°C** to a High of **{max_t}°C**\n"
        f"- 🌧️ **Precipitation:** {rain_desc}\n"
        f"- 💨 **Wind & Atmosphere:** {wind_desc}\n"
        f"- 🍃 **Air Quality:** {aqi_desc}\n"
        f"- ☀️ **Solar UV:** UV Index is **{weather.uv_index}** ({'Very High' if weather.uv_index > 7 else 'Moderate'}) with Sunrise at **{weather.sunrise} IST** and Sunset at **{weather.sunset} IST**.\n"
    )

def process_conversational_query(req: WeatherQueryRequest) -> ChatResponse:
    """Main LLM Tool Calling and Query Processing Engine."""
    query = req.query.strip()
    lang = req.language if req.language and req.language != "auto" else detect_language(query)
    persona = req.persona or "general"
    
    # Extract location
    loc_name = extract_location_from_query(query, req.location_name)
    lat, lon, proper_name, state_name = geocode_location(loc_name)
    
    # Fetch live weather telemetry and NWP grids
    weather = fetch_weather_data(lat, lon, proper_name, state_name)
    
    # Identify Intent
    q_low = query.lower()
    is_cyclone = any(k in q_low for k in ["cyclone", "storm", "vaayu", "flood", "warning", "alert", "danger", "disaster", "अलर्ट", "चेतावनी"])
    is_agri = persona == "farmer" or any(k in q_low for k in ["crop", "farmer", "paddy", "cotton", "wheat", "sugarcane", "irrigation", "spray", "pesticide", "harvest", "फसल", "धान", "गेहूं", "कापूस", "शेती"])
    is_aviation = persona == "aviation" or any(k in q_low for k in ["flight", "aviation", "metar", "taf", "airport", "pilot", "runway", "ifr", "vfr"])
    is_marine = persona == "marine" or any(k in q_low for k in ["sea", "marine", "ocean", "wave", "tide", "fisherman", "fishing", "coastal", "समुद्र", "लाटा"])
    is_climate = any(k in q_low for k in ["climate", "history", "trend", "monsoon average", "warming", "decade", "historical"])

    alerts = None
    agri_adv = None
    av_brief = None
    marine_adv = None
    
    # Tool execution based on routed intent
    if is_agri:
        crop = "paddy"
        for c in ["cotton", "wheat", "sugarcane", "soybean", "mustard"]:
            if c in q_low:
                crop = c
                break
        rain_prob = weather.hourly[0].rain_prob if weather.hourly else 20
        agri_adv = generate_crop_advisory(crop, proper_name, state_name, weather.current_temp, rain_prob, weather.humidity)

    if is_aviation:
        av_brief = get_aviation_briefing(proper_name)

    if is_marine:
        marine_adv = get_marine_advisory(proper_name)

    if is_cyclone or weather.current_temp > 42.0 or weather.precipitation > 25.0:
        alerts = get_active_alerts(state=state_name, district=proper_name)

    # Formulate localized response & speech audio text
    markdown_resp = ""
    speech_text = ""
    quick_suggestions = []
    
    if lang == "hi": # Hindi
        speech_text = f"{proper_name} में वर्तमान तापमान {weather.current_temp}°C है और मौसम {weather.condition} है। अधिकतम तापमान {weather.daily[0].temp_max if weather.daily else 32}°C रहने का अनुमान है।"
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} का मौसम पूर्वानुमान**\n\n"
            f"वर्तमान में {proper_name} में **{weather.condition}** मौसम है और तापमान **{weather.current_temp}°C** (महसूस: **{weather.feels_like}°C**) दर्ज किया गया है।\n\n"
            f"**प्रमुख मौसम बिंदु:**\n"
            f"- 🌡️ **तापमान सीमा:** न्यूनतम **{weather.daily[0].temp_min if weather.daily else 22}°C** से अधिकतम **{weather.daily[0].temp_max if weather.daily else 32}°C**\n"
            f"- 🌧️ **बारिश संभावना:** **{weather.hourly[0].rain_prob if weather.hourly else 10}%** संभावना (वर्षा: {weather.precipitation} mm)\n"
            f"- 💨 **हवा की गति:** **{weather.wind_speed} km/h {weather.wind_direction}**, आर्द्रता **{weather.humidity}%**\n"
            f"- 🍃 **वायु गुणवत्ता (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        if agri_adv:
            speech_text += f" किसान भाइयों के लिए सलाह: {agri_adv.irrigation_advice}"
            markdown_resp += (
                f"\n#### 🌾 **कृषि सलाह ({agri_adv.crop})**\n"
                f"- **सिंचाई सलाह:** {agri_adv.irrigation_advice}\n"
                f"- **कीटनाशक छिड़काव:** {agri_adv.pesticide_advice}\n"
                f"- **कटाई परामर्श:** {agri_adv.harvest_recommendation}\n"
            )
        if alerts:
            markdown_resp += f"\n⚠️ **मौसम चेतावनी (CAP Alert):** {alerts[0].headline}\n_{alerts[0].instruction}_\n"
        quick_suggestions = [f"कल {proper_name} में बारिश होगी क्या?", f"{proper_name} के लिए कृषि सलाह", f"{proper_name} का 7 दिनों का मौसम"]

    elif lang == "mr": # Marathi
        speech_text = f"{proper_name} मध्ये सध्याचे तापमान {weather.current_temp}°C असून हवामान {weather.condition} आहे."
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} हवामान अंदाज**\n\n"
            f"{proper_name} मध्ये सध्या **{weather.condition}** वातावरण असून तापमान **{weather.current_temp}°C** (अनुभव: **{weather.feels_like}°C**) आहे.\n\n"
            f"**महत्त्वाचे मुद्दे:**\n"
            f"- 🌡️ **तापमान:** किमान **{weather.daily[0].temp_min if weather.daily else 22}°C** ते कमाल **{weather.daily[0].temp_max if weather.daily else 32}°C**\n"
            f"- 🌧️ **पाऊस अंदाज:** **{weather.hourly[0].rain_prob if weather.hourly else 10}%** शक्यता\n"
            f"- 💨 **वारा व आर्द्रता:** वारा **{weather.wind_speed} km/h**, आर्द्रता **{weather.humidity}%**\n"
            f"- 🍃 **हवेचा दर्जा (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        if agri_adv:
            markdown_resp += (
                f"\n#### 🌾 **शेतकरी कृषी सल्ला ({agri_adv.crop})**\n"
                f"- **पाणी व्यवस्थापन:** {agri_adv.irrigation_advice}\n"
                f"- **फवारणी सल्ला:** {agri_adv.pesticide_advice}\n"
            )
        quick_suggestions = [f"{proper_name} मध्ये उद्या पाऊस पडेल का?", f"{proper_name} साठी कृषी सल्ला", f"{proper_name} 7 दिवसांचा अंदाज"]

    else: # English (Default)
        speech_text = f"In {proper_name}, it is currently {weather.current_temp} degrees Celsius with {weather.condition}. Wind speed is {weather.wind_speed} kilometers per hour."
        markdown_resp = format_human_weather_story(weather, proper_name, state_name)

        if agri_adv:
            speech_text += f" Agromet Advisory: {agri_adv.irrigation_advice}"
            markdown_resp += (
                f"\n#### 🌾 **Agromet Advisory ({agri_adv.crop})**\n"
                f"- **Irrigation Recommendation:** {agri_adv.irrigation_advice}\n"
                f"- **Pesticide & Spraying:** {agri_adv.pesticide_advice}\n"
                f"- **Harvesting Guidance:** {agri_adv.harvest_recommendation}\n"
                f"- **Damini Lightning Risk:** {'⚡ High Risk - Stay away from open fields' if agri_adv.damini_lightning_alert else '✅ Safe from electrical activity'}\n"
            )

        if av_brief:
            markdown_resp += (
                f"\n#### ✈️ **Aviation Weather Briefing ({av_brief.station_icao})**\n"
                f"- **Flight Category:** **{av_brief.flight_category}**\n"
                f"- **Raw METAR:** `{av_brief.metar_raw}`\n"
                f"- **Decoded Observations:** Wind: {av_brief.metar_decoded['wind']}, Visibility: {av_brief.metar_decoded['visibility']}, Clouds: {av_brief.metar_decoded['clouds']}\n"
                f"- **Hazards:** {', '.join(av_brief.hazards)}\n"
            )

        if marine_adv:
            markdown_resp += (
                f"\n#### ⚓ **INCOIS Ocean State & Marine Advisory**\n"
                f"- **Coastal Sector:** {marine_adv.coastal_zone}\n"
                f"- **Significant Wave Height:** **{marine_adv.wave_height_m} meters** ({marine_adv.sea_condition})\n"
                f"- **Fishermen Advisory:** **{'🚨 WARNING - DO NOT VENTURE INTO DEEP SEA' if marine_adv.fisherman_warning else '✅ Normal coastal fishing permitted'}**\n"
                f"- **Tidal Timings:** High Tide at **{marine_adv.high_tide_time}**, Low Tide at **{marine_adv.low_tide_time}**\n"
            )

        if alerts:
            markdown_resp += f"\n#### 🚨 **Active CAP Disaster Warnings**\n"
            for alt in alerts:
                markdown_resp += f"- **[{alt.severity.upper()} ALERT] {alt.headline}**\n  _{alt.instruction}_\n"

        quick_suggestions = [
            f"Will it rain heavily in {proper_name} tomorrow?",
            f"Agromet crop advisory for {proper_name}",
            f"Show active alerts for {state_name}",
            f"7-day hourly NWP forecast for {proper_name}"
        ]

    suggested_actions = [
        {"label": "View GIS Radar Map", "action": "open_map"},
        {"label": "Detailed 7-Day Forecast", "action": "open_dashboard"},
        {"label": "Farmer Agromet Advisories", "action": "open_agri"},
        {"label": "Disaster Alerts Feed", "action": "open_alerts"}
    ]

    return ChatResponse(
        query=query,
        detected_language=lang,
        persona=persona,
        speech_text=speech_text,
        markdown_response=markdown_resp,
        structured_weather=weather,
        alerts=alerts,
        agri_advisory=agri_adv,
        aviation_briefing=av_brief,
        marine_advisory=marine_adv,
        quick_suggestions=quick_suggestions,
        suggested_actions=suggested_actions
    )
