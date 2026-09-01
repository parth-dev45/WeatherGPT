import re
import datetime
from typing import Dict, Any, Tuple, Optional, List
from .weather_service import geocode_location, fetch_weather_data, compare_locations, INDIAN_LOCATIONS
from .alert_service import get_active_alerts
from .agri_advisory import generate_crop_advisory
from .aviation_service import get_aviation_briefing
from .marine_service import get_marine_advisory
from .historical_service import get_climate_trend_data
from ..schemas.models import WeatherQueryRequest, ChatResponse, WeatherData, CityComparisonData

# Comprehensive Indic Multi-Script Transliteration mappings for all 8 Indian Languages
INDIC_LOCATION_TRANSLITERATIONS = {
    # 1. Hindi / Marathi / Sanskrit (Devanagari)
    "पुणे": "Pune", "मुंबई": "Mumbai", "बम्बई": "Mumbai", "दिल्ली": "Delhi", "नई दिल्ली": "New Delhi",
    "नागपूर": "Nagpur", "नागपुर": "Nagpur", "नाशिक": "Nashik", "नासिक": "Nashik", "सोलापूर": "Solapur",
    "सोलापुर": "Solapur", "कोल्हापूर": "Kolhapur", "छत्रपती संभाजीनगर": "Aurangabad", "संभाजीनगर": "Aurangabad",
    "औरंगाबाद": "Aurangabad", "जालना": "Jalna", "लातूर": "Latur", "लातुर": "Latur", "सांगली": "Sangli",
    "सातारा": "Satara", "बारामती": "Baramati", "बीड": "Beed", "अमरावती": "Amravati", "अकोला": "Akola",
    "जळगाव": "Jalgaon", "परभणी": "Parbhani", "नांदेड": "Nanded", "चंद्रपूर": "Chandrapur", "रत्नागिरी": "Ratnagiri",
    "सिंधुदुर्ग": "Sindhudurg", "अलिबाग": "Alibag", "ठाणे": "Thane", "चेन्नई": "Chennai", "कोलकाता": "Kolkata",
    "कलकत्ता": "Kolkata", "बेंगळुरू": "Bengaluru", "बैंगलोर": "Bengaluru", "बेंगलुरु": "Bengaluru",
    "हैदराबाद": "Hyderabad", "जयपूर": "Jaipur", "जयपुर": "Jaipur", "जोधपूर": "Jodhpur", "उदयपूर": "Udaipur",
    "अलवर": "Alwar", "लखनौ": "Lucknow", "लखनऊ": "Lucknow", "पाटणा": "Patna", "पटना": "Patna",
    "भोपाळ": "Bhopal", "भोपाल": "Bhopal", "इंदौर": "Indore", "ग्वालियर": "Gwalior", "जबलपूर": "Jabalpur",
    "उज्जैन": "Ujjain", "चंदीगड": "Chandigarh", "चंडीगढ़": "Chandigarh", "लुधियाना": "Ludhiana",
    "अमृतसर": "Amritsar", "वाराणसी": "Varanasi", "बनारस": "Varanasi", "कानपूर": "Kanpur", "कानपुर": "Kanpur",
    "झांसी": "Jhansi", "झांशी": "Jhansi", "प्रयागराज": "Prayagraj", "इलाहाबाद": "Prayagraj", "अयोध्या": "Ayodhya",
    "अहमदाबाद": "Ahmedabad", "सूरत": "Surat", "वडोदरा": "Vadodara", "राजकोट": "Rajkot", "गुवाहाटी": "Guwahati",
    "कोची": "Kochi", "कोचीन": "Kochi", "कोझिकोड": "Kozhikode", "तिरुवनंतपुरम": "Thiruvananthapuram",
    "वायनाड": "Wayanad", "विशाखापट्टनम": "Visakhapatnam", "वाइजाग": "Visakhapatnam", "विजयवाडा": "Vijayawada",
    "तिरुपती": "Tirupati", "वारंगल": "Warangal", "पुरी": "Puri", "भुवनेश्वर": "Bhubaneswar", "कटक": "Cuttack",
    "राउरकेला": "Rourkela", "संबलपूर": "Sambalpur", "श्रीनगर": "Srinagar", "जम्मू": "Jammu", "शिमला": "Shimla",
    "मनाली": "Manali", "धर्मशाला": "Dharamshala", "देहरादून": "Dehradun", "ऋषिकेश": "Rishikesh",
    "हरिद्वार": "Haridwar", "नैनीताल": "Nainital", "रांची": "Ranchi", "जमशेदपूर": "Jamshedpur",
    "धनबाद": "Dhanbad", "रायपूर": "Raipur", "बिलासपुर": "Bilaspur", "गोवा": "Panaji", "पणजी": "Panaji", "लेह": "Leh",

    # 2. Tamil (தமிழ்)
    "சென்னை": "Chennai", "சென்னையில்": "Chennai", "மதுரை": "Madurai", "கோயம்புத்தூர்": "Coimbatore", "கோவை": "Coimbatore",
    "திருச்சி": "Tiruchirappalli", "திருச்சிராப்பள்ளி": "Tiruchirappalli", "சேலம்": "Salem",
    "திருநெல்வேலி": "Tirunelveli", "ஈரோடு": "Erode", "வேலூர்": "Vellore", "கன்னியாகுமரி": "Kanyakumari",
    "தஞ்சாவூர்": "Thanjavur", "திண்டுக்கல்": "Dindigul", "தூத்துக்குடி": "Thoothukudi", "திருப்பூர்": "Tiruppur",
    "ராமேஸ்வரம்": "Rameshwaram", "புதுச்சேரி": "Puducherry", "காஞ்சிபுரம்": "Kanchipuram", "நாகர்கோவில்": "Nagercoil",

    # 3. Telugu (తెలుగు)
    "హైదరాబాద్": "Hyderabad", "హైదరాబాద్‌లో": "Hyderabad", "విశాఖపట్నం": "Visakhapatnam", "వైజాగ్": "Visakhapatnam", "విజయవాడ": "Vijayawada",
    "తిరుపతి": "Tirupati", "వరంగల్": "Warangal", "గుంటూరు": "Guntur", "నెల్లూరు": "Nellore", "కర్నూలు": "Kurnool",
    "రాజమండ్రి": "Rajahmundry", "కడప": "Kadapa", "కాకినాడ": "Kakinada", "నిజామాబాద్": "Nizamabad",
    "కరీంనగర్": "Karimnagar", "అనంతపురం": "Anantapur", "ఖమ్మం": "Khammam",

    # 4. Bengali (বাংলা)
    "কলকাতা": "Kolkata", "কলকাতায়": "Kolkata", "হাওড়া": "Howrah", "শিলিগুড়ি": "Siliguri", "দুর্গাপুর": "Durgapur",
    "আসানসোল": "Asansol", "বর্ধমান": "Bardhaman", "মেদিনীপুর": "Midnapore", "দার্জিলিং": "Darjeeling",
    "মালদা": "Malda", "জলপাইগুড়ি": "Jalpaiguri", "খড়গপুর": "Kharagpur",

    # 5. Gujarati (ગુજરાતી)
    "અમદાવાદ": "Ahmedabad", "અમદાવાદમાં": "Ahmedabad", "સુરત": "Surat", "વડોદરા": "Vadodara", "રાજકોટ": "Rajkot", "ભાવનગર": "Bhavnagar",
    "જામનગર": "Jamnagar", "જુનાગઢ": "Junagadh", "ગાંધીનગર": "Gandhinagar", "આણંદ": "Anand",
    "નવસારી": "Navsari", "ભરૂચ": "Bharuch", "પોરબંદર": "Porbandar", "મોરબી": "Morbi", "ભુજ": "Bhuj",

    # 6. Punjabi (ਪੰਜਾਬੀ)
    "ਅੰਮ੍ਰਿਤਸਰ": "Amritsar", "ਲੁਧਿਆਣਾ": "Ludhiana", "ਜਲੰਧਰ": "Jalandhar", "ਪਟਿਆਲਾ": "Patiala",
    "ਬਠਿੰਡਾ": "Bathinda", "ਮੋਹਾਲੀ": "Mohali", "ਚੰਡੀਗੜ੍ਹ": "Chandigarh", "ਹੁਸ਼ਿਆਰਪੁਰ": "Hoshiarpur",
    "ਪਠਾਨਕੋਟ": "Pathankot", "ਫ਼ਿਰੋਜ਼ਪੁਰ": "Firozpur",

    # 7. Kannada (ಕನ್ನಡ)
    "ಬೆಂಗಳೂರು": "Bengaluru", "ಬೆಂಗಳೂರಿನಲ್ಲಿ": "Bengaluru", "ಮೈಸೂರು": "Mysuru", "ಮಂಗಳೂರು": "Mangaluru", "ಹುಬ್ಬಳ್ಳಿ": "Hubli",
    "ಧಾರವಾಡ": "Dharwad", "ಬೆಳಗಾವಿ": "Belagavi", "ಕಲಬುರಗಿ": "Kalaburagi", "ಬಳ್ಳಾರಿ": "Ballari",
    "ದಾವಣಗೆರೆ": "Davangere", "ಶಿವಮೊಗ್ಗ": "Shivamogga", "ವಿಜಯಪುರ": "Vijayapura", "ಉಡುಪಿ": "Udupi",
    "ಬೀದರ್": "Bidar", "ಹಾಸನ": "Hassan", "ತುಮಕೂರು": "Tumakuru", "ಕೊಡಗು": "Coorg",

    # 8. Malayalam (മലയാളം)
    "തിരുവനന്തപുരം": "Thiruvananthapuram", "കൊച്ചി": "Kochi", "കോഴിക്കോട്": "Kozhikode",
    "തൃശ്ശൂർ": "Thrissur", "കൊല്ലം": "Kollam", "കണ്ണൂർ": "Kannur", "ആലപ്പുഴ": "Alappuzha",
    "പാലക്കാട്": "Palakkad", "കോട്ടയം": "Kottayam", "വയനാട്": "Wayanad", "മൂന്നാർ": "Munnar"
}

LANGUAGE_MAP = {
    "hi": ["मौसम", "बारिश", "तापमान", "हवा", "गर्मी", "फसल", "धान", "गेहूं", "अलर्ट", "बिजली", "आज", "कल", "होगा", "बताओ", "क्या"],
    "mr": ["हवामान", "पाऊस", "तापमान", "शेतकरी", "पीक", "कापूस", "सोयाबीन", "ऊन", "सांगा", "कसे", "आहे"],
    "ta": ["வானிலை", "மழை", "வெப்பநிலை", "விவசாயம்", "காற்று", "புயல்", "இன்று", "நாளை", "பெய்யுமா"],
    "te": ["వాతావరణం", "వర్షం", "ఉష్ణోగ్రత", "పంట", "రైతు", "గాలి", "హెచ్చరిక", "ఎలా"],
    "bn": ["আবহাওয়া", "বৃষ্টি", "তাপমাত্রা", "ঘূর্ণিঝড়", "আজ", "কাল", "কেমন", "হবে"],
    "gu": ["હવામાન", "વરસાદ", "તાપમાન", "ખેડૂત", "પાક", "આગાહી", "પડશે"],
    "pa": ["ਮੌਸਮ", "ਮੀਂਹ", "ਤਾਪਮਾਨ", "ਕਣਕ", "ਝੋਨਾ", "ਕੱਲ੍ਹ", "ਕਿਵੇਂ"],
    "kn": ["ಹವಾಮಾನ", "ಮಳೆ", "ತಾಪಮಾನ", "ಬೆಳೆ", "ರೈತ", "ಬರುತ್ತದೆಯೇ"]
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
        elif 0x0D00 <= code <= 0x0D7F:
            return "ml"
    return "en"

STOPWORDS = {
    "what", "is", "the", "weather", "forecast", "temperature", "rain", "rainfall", 
    "heavy", "how", "hot", "cold", "now", "right", "today", "tomorrow", "tonight", 
    "this", "week", "will", "it", "in", "at", "near", "for", "around", "over", "of", 
    "and", "to", "tell", "me", "show", "give", "update", "condition", "status", 
    "kaisa", "hai", "hoga", "kya", "padega", "aaj", "kal", "ka", "ki", "ke", "liye",
    "crop", "agri", "farming", "cotton", "paddy", "wheat", "sugarcane", "pesticide",
    "please", "can", "you", "check", "current", "live", "about", "details", "info",
    "மழை", "வானிலை", "பெய்யுமா", "இன்று", "நாளை",
    "వర్షం", "వాతావరణం", "ఎలా", "ఉంది", "రేపు",
    "বৃষ্টি", "আবহাওয়া", "হবে", "কি", "আজ", "কাল",
    "વરસાદ", "હવામાન", "પડશે", "આજે", "કાલે",
    "ਮੀਂਹ", "ਮੌਸਮ", "ਕਿਵੇਂ", "ਹੈ", "ਅੱਜ", "ਕੱਲ੍ਹ",
    "ಮಳೆ", "ಹವಾಮಾನ", "ಬರುತ್ತದೆಯೇ", "ಇಂದು", "ನಾಳೆ"
}

def extract_location_from_query(text: str, fallback_loc: Optional[str] = None) -> str:
    """Extracts location with multi-stage entity resolution across all Indian language scripts."""
    lowered = text.lower()
    
    # 1. Match against known 250+ Indian cities and districts (English)
    sorted_cities = sorted(INDIAN_LOCATIONS.keys(), key=len, reverse=True)
    for city_key in sorted_cities:
        pattern = r'\b' + re.escape(city_key) + r'\b'
        if re.search(pattern, lowered):
            return city_key.title()

    # 2. Check Indic Multi-Script Dictionary (Tamil, Telugu, Bengali, Gujarati, Punjabi, Kannada, Marathi, Hindi)
    sorted_indic = sorted(INDIC_LOCATION_TRANSLITERATIONS.keys(), key=len, reverse=True)
    for indic_name in sorted_indic:
        if indic_name in text:
            return INDIC_LOCATION_TRANSLITERATIONS[indic_name]

    # 3. Regex extraction: 'in <City>', 'at <City>', 'near <City>', 'for <City>'
    match = re.search(r'\b(?:in|at|near|for|around|over|of)\s+([A-Za-z]+)', text, re.IGNORECASE)
    if match:
        cand = match.group(1).strip()
        if cand.lower() not in STOPWORDS and len(cand) >= 3:
            return cand.title()

    # 4. Tokenize Unicode words (including all Indic regional scripts)
    unicode_tokens = re.findall(r'[\w\u0900-\u0DFF]{3,}', text)
    candidate_tokens = [w for w in unicode_tokens if w.lower() not in STOPWORDS]
    if candidate_tokens:
        # Check if first candidate token is a known regional city
        for tok in candidate_tokens:
            for indic_name in sorted_indic:
                if indic_name in tok:
                    return INDIC_LOCATION_TRANSLITERATIONS[indic_name]
        return candidate_tokens[0]

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
    
    if weather.precipitation > 5.0 or rain_p > 60:
        rain_desc = f"**Heavy to moderate rainfall spells** are active with an elevated rain probability of **{rain_p}%**."
    elif weather.precipitation > 0.1 or rain_p > 30:
        rain_desc = f"Passing light showers are possible (**{rain_p}% probability**) with {weather.precipitation} mm precipitation."
    else:
        rain_desc = f"Dry conditions are expected to prevail (**{rain_p}% rain probability**) with negligible precipitation."

    if weather.current_temp > 38.0:
        comfort = f"⚠️ **High thermal discomfort**: Ambient temperature is elevated at **{weather.current_temp}°C** (feels like **{weather.feels_like}°C**). Sun protection and hydration are recommended."
    elif weather.current_temp < 15.0:
        comfort = f"❄️ **Cool and pleasant weather**: Morning temperatures dip to **{min_t}°C**."
    else:
        comfort = f"Current conditions are **{weather.condition}** with a comfortable temperature of **{weather.current_temp}°C** (feels like **{weather.feels_like}°C**)."

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

def extract_two_locations(text: str) -> Tuple[str, str]:
    """Extracts two city names for comparison queries."""
    patterns = [
        r'(?:compare|between)\s+([A-Za-z]+)\s+(?:and|vs|with|to)\s+([A-Za-z]+)',
        r'([A-Za-z]+)\s+(?:vs|versus)\s+([A-Za-z]+)',
        r'([A-Za-z]+)\s+(?:or|and)\s+([A-Za-z]+)\s+weather',
        r'([A-Za-z]+)\s+(?:hotter|colder|better|warmer)\s+than\s+([A-Za-z]+)'
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            c1, c2 = m.group(1).strip().title(), m.group(2).strip().title()
            if c1.lower() not in STOPWORDS and c2.lower() not in STOPWORDS:
                return c1, c2
    return "Mumbai", "Delhi"

def process_conversational_query(req: WeatherQueryRequest) -> ChatResponse:
    """Main LLM Tool Calling and Query Processing Engine with Multilingual Generation."""
    query = req.query.strip()
    detected = detect_language(query)
    if detected != "en":
        lang = detected
    else:
        lang = req.language if req.language and req.language != "auto" else "en"
    persona = req.persona or "general"
    q_low = query.lower()

    # Comparison Intent
    is_compare = any(k in q_low for k in ["compare", " vs ", "versus", "hotter than", "colder than", "warmer than", "better than", "तुलना", "तुलना करा", "ஒப்பீடு", "పోలిక"])
    if is_compare:
        c1, c2 = extract_two_locations(query)
        comp_data = compare_locations(c1, c2)
        speech_text = f"Comparing {comp_data.city1.location} and {comp_data.city2.location}. {comp_data.temp_warmer_city} is warmer by {abs(comp_data.temp_diff)} degrees Celsius. Travel safety score is {comp_data.travel_safety_score} out of 100."
        markdown_resp = (
            f"### ⚖️ **Comparative Weather Intelligence: {comp_data.city1.location} vs {comp_data.city2.location}**\n\n"
            f"| Metric | 📍 **{comp_data.city1.location}** ({comp_data.city1.state}) | 📍 **{comp_data.city2.location}** ({comp_data.city2.state}) | 📊 **Variance / Advantage** |\n"
            f"| :--- | :--- | :--- | :--- |\n"
            f"| 🌡️ **Current Temp** | **{comp_data.city1.current_temp}°C** (Feels {comp_data.city1.feels_like}°C) | **{comp_data.city2.current_temp}°C** (Feels {comp_data.city2.feels_like}°C) | **{comp_data.temp_warmer_city}** is +{abs(comp_data.temp_diff)}°C warmer |\n"
            f"| 💧 **Humidity** | **{comp_data.city1.humidity}%** | **{comp_data.city2.humidity}%** | $\\Delta$ {abs(comp_data.humidity_diff)}% |\n"
            f"| 💨 **Wind Speed** | **{comp_data.city1.wind_speed} km/h** ({comp_data.city1.wind_direction}) | **{comp_data.city2.wind_speed} km/h** ({comp_data.city2.wind_direction}) | — |\n"
            f"| 🍃 **Air Quality (AQI)** | **{comp_data.city1.aqi}** ({comp_data.city1.aqi_status}) | **{comp_data.city2.aqi}** ({comp_data.city2.aqi_status}) | 🌿 **{comp_data.aqi_better_city}** has cleaner air |\n"
            f"| 🌧️ **Precipitation** | **{comp_data.city1.precipitation} mm** ({comp_data.city1.condition}) | **{comp_data.city2.precipitation} mm** ({comp_data.city2.condition}) | 🌧️ Higher rain risk in **{comp_data.rain_risk_city}** |\n\n"
            f"#### 🚗 **Highway & Transit Route Safety (Score: {comp_data.travel_safety_score}/100)**\n"
            f"{comp_data.travel_advisory}\n\n"
            f"#### 🏃 **Health & Vulnerability Personas**\n"
            f"- 🏃 **Athletes & Runners:** {comp_data.health_advisory.athletes}\n"
            f"- 🫁 **Asthma & Respiratory:** {comp_data.health_advisory.asthma_patients}\n"
            f"- 👶 **Children & Schools:** {comp_data.health_advisory.children_schools}\n"
            f"- 👴 **Senior Citizens:** {comp_data.health_advisory.elderly}\n"
        )
        quick_suggestions = [
            "Compare Pune vs Goa",
            "Compare Bengaluru vs Hyderabad",
            "Compare Shimla vs Manali",
            f"7-day forecast for {comp_data.city1.location}"
        ]
        suggested_actions = [
            {"label": "Open Comparison Matrix", "action": "open_compare"},
            {"label": "View Doppler Radar Map", "action": "open_map"},
            {"label": "Active CAP Warnings", "action": "open_alerts"}
        ]
        return ChatResponse(
            query=query,
            detected_language=lang,
            persona=persona,
            speech_text=speech_text,
            markdown_response=markdown_resp,
            structured_weather=comp_data.city1,
            comparison_data=comp_data,
            alerts=None,
            agri_advisory=None,
            aviation_briefing=None,
            marine_advisory=None,
            quick_suggestions=quick_suggestions,
            suggested_actions=suggested_actions
        )
    
    # Extract location
    loc_name = extract_location_from_query(query, req.location_name)
    lat, lon, proper_name, state_name = geocode_location(loc_name)
    
    # Fetch live weather telemetry and NWP grids
    weather = fetch_weather_data(lat, lon, proper_name, state_name)
    
    # Identify Intent
    is_cyclone = any(k in q_low for k in ["cyclone", "storm", "vaayu", "flood", "warning", "alert", "danger", "disaster", "अलर्ट", "चेतावनी"])
    is_agri = persona == "farmer" or any(k in q_low for k in ["crop", "farmer", "paddy", "cotton", "wheat", "sugarcane", "irrigation", "spray", "pesticide", "harvest", "फसल", "धान", "गेहूं", "कापूस", "शेती"])
    is_aviation = persona == "aviation" or any(k in q_low for k in ["flight", "aviation", "metar", "taf", "airport", "pilot", "runway", "ifr", "vfr"])
    is_marine = persona == "marine" or any(k in q_low for k in ["sea", "marine", "ocean", "wave", "tide", "fisherman", "fishing", "coastal", "समुद्र", "लाटा"])

    alerts = None
    agri_adv = None
    av_brief = None
    marine_adv = None
    
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

    today = weather.daily[0] if weather.daily else None
    min_t = today.temp_min if today else weather.current_temp - 3
    max_t = today.temp_max if today else weather.current_temp + 4
    rain_p = weather.hourly[0].rain_prob if weather.hourly else 10

    # 1. HINDI (hi)
    if lang == "hi":
        speech_text = f"{proper_name} में वर्तमान तापमान {weather.current_temp}°C है और मौसम {weather.condition} है। अधिकतम तापमान {max_t}°C रहने का अनुमान है।"
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} का मौसम पूर्वानुमान**\n\n"
            f"वर्तमान में {proper_name} में **{weather.condition}** मौसम है और तापमान **{weather.current_temp}°C** (महसूस: **{weather.feels_like}°C**) दर्ज किया गया है।\n\n"
            f"**प्रमुख मौसम बिंदु:**\n"
            f"- 🌡️ **तापमान सीमा:** न्यूनतम **{min_t}°C** से अधिकतम **{max_t}°C**\n"
            f"- 🌧️ **बारिश संभावना:** **{rain_p}%** संभावना (वर्षा: {weather.precipitation} mm)\n"
            f"- 💨 **हवा की गति:** **{weather.wind_speed} km/h {weather.wind_direction}**, आर्द्रता **{weather.humidity}%**\n"
            f"- 🍃 **वायु गुणवत्ता (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        if agri_adv:
            speech_text += f" किसान भाइयों के लिए सलाह: {agri_adv.irrigation_advice}"
            markdown_resp += f"\n#### 🌾 **कृषि सलाह ({agri_adv.crop})**\n- **सिंचाई:** {agri_adv.irrigation_advice}\n- **कीटनाशक छिड़काव:** {agri_adv.pesticide_advice}\n"
        quick_suggestions = [f"कल {proper_name} में बारिश होगी क्या?", f"{proper_name} के लिए कृषि सलाह", f"{proper_name} 7 दिनों का मौसम"]

    # 2. MARATHI (mr)
    elif lang == "mr":
        speech_text = f"{proper_name} मध्ये सध्याचे तापमान {weather.current_temp}°C असून हवामान {weather.condition} आहे."
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} हवामान अंदाज**\n\n"
            f"{proper_name} मध्ये सध्या **{weather.condition}** वातावरण असून तापमान **{weather.current_temp}°C** (अनुभव: **{weather.feels_like}°C**) आहे.\n\n"
            f"**महत्त्वाचे मुद्दे:**\n"
            f"- 🌡️ **तापमान:** किमान **{min_t}°C** ते कमाल **{max_t}°C**\n"
            f"- 🌧️ **पाऊस अंदाज:** **{rain_p}%** शक्यता (पाऊस: {weather.precipitation} mm)\n"
            f"- 💨 **वारा व आर्द्रता:** वारा **{weather.wind_speed} km/h**, आर्द्रता **{weather.humidity}%**\n"
            f"- 🍃 **हवेचा दर्जा (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        if agri_adv:
            markdown_resp += f"\n#### 🌾 **शेतकरी कृषी सल्ला ({agri_adv.crop})**\n- **पाणी व्यवस्थापन:** {agri_adv.irrigation_advice}\n- **फवारणी:** {agri_adv.pesticide_advice}\n"
        quick_suggestions = [f"{proper_name} मध्ये उद्या पाऊस पडेल का?", f"{proper_name} साठी कृषी सल्ला", f"{proper_name} 7 दिवसांचा अंदाज"]

    # 3. TAMIL (ta)
    elif lang == "ta":
        speech_text = f"{proper_name} இல் தற்போதைய வெப்பநிலை {weather.current_temp}°C. வானிலை {weather.condition} ஆக உள்ளது."
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} வானிலை நிலவரம்**\n\n"
            f"தற்போது {proper_name} இல் வானிலை **{weather.condition}** ஆக உள்ளது. வெப்பநிலை **{weather.current_temp}°C** (உணர்வது: **{weather.feels_like}°C**).\n\n"
            f"**முக்கிய வானிலை விவரங்கள்:**\n"
            f"- 🌡️ **வெப்பநிலை அளவு:** குறைந்தபட்சம் **{min_t}°C** முதல் அதிகபட்சம் **{max_t}°C** வரை\n"
            f"- 🌧️ **மழை வாய்ப்பு:** **{rain_p}%** வாய்ப்பு (மழைப்பொழிவு: {weather.precipitation} mm)\n"
            f"- 💨 **காற்று & ஈரப்பதம்:** காற்று வேகம் **{weather.wind_speed} km/h**, ஈரப்பதம் **{weather.humidity}%**\n"
            f"- 🍃 **காற்று தரம் (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        quick_suggestions = [f"நாளை {proper_name} மழை பெய்யுமா?", f"{proper_name} விவசாய ஆலோசனை", f"{proper_name} 7 நாள் வானிலை"]

    # 4. TELUGU (te)
    elif lang == "te":
        speech_text = f"{proper_name} లో ప్రస్తుత ఉష్ణోగ్రత {weather.current_temp}°C. వాతావరణం {weather.condition} గా ఉంది."
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} వాతావరణ సమాచారం**\n\n"
            f"ప్రస్తుతం {proper_name} లో వాతావరణం **{weather.condition}** గా ఉంది. ఉష్ణోగ్రత **{weather.current_temp}°C** (అనిపించేది: **{weather.feels_like}°C**).\n\n"
            f"**ముఖ్య వాతావరణ వివరాలు:**\n"
            f"- 🌡️ **ఉష్ణోగ్రత శ్రేణి:** కనిష్ట ఉష్ణోగ్రత **{min_t}°C** నుండి గరిష్ట ఉష్ణోగ్రత **{max_t}°C**\n"
            f"- 🌧️ **వర్ష సూచన:** **{rain_p}%** అవకాశం (వర్షపాతం: {weather.precipitation} mm)\n"
            f"- 💨 **గాలి వేగం & తేమ:** గాలి వేగం **{weather.wind_speed} km/h**, గాలిలో తేమ **{weather.humidity}%**\n"
            f"- 🍃 **గాలి నాణ్యత (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        quick_suggestions = [f"రేపు {proper_name} లో వర్షం పడుతుందా?", f"{proper_name} రైతు సలహాలు", f"{proper_name} 7 రోజుల వాతావరణం"]

    # 5. BENGALI (bn)
    elif lang == "bn":
        speech_text = f"{proper_name} এ বর্তমান তাপমাত্রা {weather.current_temp}°C এবং আবহাওয়া {weather.condition}।"
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} আবহাওয়ার পূর্বাভাস**\n\n"
            f"বর্তমানে {proper_name} এ আবহাওয়া **{weather.condition}** এবং তাপমাত্রা **{weather.current_temp}°C** (অনুভূত: **{weather.feels_like}°C**)।\n\n"
            f"**প্রধান আবহাওয়া তথ্য:**\n"
            f"- 🌡️ **তাপমাত্রার বিস্তার:** সর্বনিম্ন **{min_t}°C** থেকে সর্বোচ্চ **{max_t}°C**\n"
            f"- 🌧️ **বৃষ্টিপাতের সম্ভাবনা:** **{rain_p}%** সম্ভাবনা (বৃষ্টিপাত: {weather.precipitation} mm)\n"
            f"- 💨 **বাতাসের গতিবেগ ও আর্দ্রতা:** বাতাসের গতি **{weather.wind_speed} km/h**, আর্দ্রতা **{weather.humidity}%**\n"
            f"- 🍃 **বায়ুর গুণমান সূচক (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        quick_suggestions = [f"কাল {proper_name} এ বৃষ্টি হবে কি?", f"{proper_name} এর কৃষি পরামর্শ", f"{proper_name} ৭ দিনের পূর্বাভাস"]

    # 6. GUJARATI (gu)
    elif lang == "gu":
        speech_text = f"{proper_name} માં હાલનું તાપમાન {weather.current_temp}°C છે અને હવામાન {weather.condition} છે."
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} હવામાન આગાહી**\n\n"
            f"હાલમાં {proper_name} માં **{weather.condition}** વાતાવરણ છે અને તાપમાન **{weather.current_temp}°C** (અનુભવ: **{weather.feels_like}°C**) છે.\n\n"
            f"**મુખ્ય હવામાન મુદ્દા:**\n"
            f"- 🌡️ **તાપમાન શ્રેણી:** લઘુત્તમ **{min_t}°C** થી મહત્તમ **{max_t}°C**\n"
            f"- 🌧️ **વરસાદની શક્યતા:** **{rain_p}%** સંભાવના (વરસાદ: {weather.precipitation} mm)\n"
            f"- 💨 **પવનની ગતિ અને ભેજ:** પવનની ગતિ **{weather.wind_speed} km/h**, ભેજ **{weather.humidity}%**\n"
            f"- 🍃 **હવાની ગુણવત્તા (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        quick_suggestions = [f"કાલે {proper_name} માં વરસાદ પડશે?", f"{proper_name} માટે કૃષિ સલાહ", f"{proper_name} 7 દિવસનું હવામાન"]

    # 7. PUNJABI (pa)
    elif lang == "pa":
        speech_text = f"{proper_name} ਵਿੱਚ ਮੌਜੂਦਾ ਤਾਪਮਾਨ {weather.current_temp}°C ਹੈ ਅਤੇ ਮੌਸਮ {weather.condition} ਹੈ।"
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ**\n\n"
            f"ਇਸ ਸਮੇਂ {proper_name} ਵਿੱਚ **{weather.condition}** ਮੌਸਮ ਹੈ ਅਤੇ ਤਾਪਮਾਨ **{weather.current_temp}°C** (ਮਹਿਸੂਸ: **{weather.feels_like}°C**) ਹੈ।\n\n"
            f"**ਮੁੱਖ ਮੌਸਮ ਜਾਣਕਾਰੀ:**\n"
            f"- 🌡️ **ਤਾਪਮਾਨ ਸੀਮਾ:** ਘੱਟੋ-ਘੱਟ **{min_t}°C** ਤੋਂ ਵੱਧ ਤੋਂ ਵੱਧ **{max_t}°C**\n"
            f"- 🌧️ **ਮੀਂਹ ਦੀ ਸੰਭਾਵਨਾ:** **{rain_p}%** ਸੰਭਾਵਨਾ (ਵਰਖਾ: {weather.precipitation} mm)\n"
            f"- 💨 **ਹਵਾ ਦੀ ਰਫ਼ਤਾਰ:** **{weather.wind_speed} km/h**, ਨਮੀ **{weather.humidity}%**\n"
            f"- 🍃 **ਹਵਾ ਦੀ ਗੁਣਵੱਤਾ (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        quick_suggestions = [f"ਕੱਲ੍ਹ {proper_name} ਵਿੱਚ ਮੀਂਹ ਪਵੇਗਾ?", f"{proper_name} ਲਈ ਖੇਤੀ ਸਲਾਹ", f"{proper_name} 7 ਦਿਨਾਂ ਦਾ ਮੌਸਮ"]

    # 8. KANNADA (kn)
    elif lang == "kn":
        speech_text = f"{proper_name} ನಲ್ಲಿ ಪ್ರಸ್ತುತ ತಾಪಮಾನ {weather.current_temp}°C ಮತ್ತು ಹವಾಮಾನ {weather.condition} ಆಗಿದೆ."
        markdown_resp = (
            f"### 🌤️ **{proper_name}, {state_name} ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ**\n\n"
            f"ಪ್ರಸ್ತುತ {proper_name} ನಲ್ಲಿ **{weather.condition}** ವಾತಾವರಣವಿದ್ದು, ತಾಪಮಾನ **{weather.current_temp}°C** (ಅನುಭವ: **{weather.feels_like}°C**) ಆಗಿದೆ.\n\n"
            f"**ಪ್ರಮುಖ ಹವಾಮಾನ ವಿವರಗಳು:**\n"
            f"- 🌡️ **ತಾಪಮಾನ ಶ್ರೇಣಿ:** ಕನಿಷ್ಠ **{min_t}°C** ರಿಂದ ಗರಿಷ್ಠ **{max_t}°C** ವರೆಗೆ\n"
            f"- 🌧️ **ಮಳೆಯ ಸಾಧ್ಯತೆ:** **{rain_p}%** ಸಂಭವನೀಯತೆ (ಮಳೆ: {weather.precipitation} mm)\n"
            f"- 💨 **ಗಾಳಿಯ ವೇಗ ಮತ್ತು ತೇವಾಂಶ:** ಗಾಳಿಯ ವೇಗ **{weather.wind_speed} km/h**, ತೇವಾಂಶ **{weather.humidity}%**\n"
            f"- 🍃 **ವಾಯು ಗುಣಮಟ್ಟ (AQI):** **{weather.aqi}** ({weather.aqi_status})\n"
        )
        quick_suggestions = [f"ನಾಳೆ {proper_name} ನಲ್ಲಿ ಮಳೆ ಬರುತ್ತದೆಯೇ?", f"{proper_name} ಕೃಷಿ ಸಲಹೆ", f"{proper_name} 7 ದಿನಗಳ ಹವಾಮಾನ"]

    # 9. ENGLISH (en - Default)
    else:
        speech_text = f"In {proper_name}, it is currently {weather.current_temp} degrees Celsius with {weather.condition}. Wind speed is {weather.wind_speed} kilometers per hour."
        markdown_resp = format_human_weather_story(weather, proper_name, state_name)

        if agri_adv:
            speech_text += f" Agromet Advisory: {agri_adv.irrigation_advice}"
            markdown_resp += (
                f"\n#### 🌾 **Agromet Advisory ({agri_adv.crop})**\n"
                f"- **Irrigation Recommendation:** {agri_adv.irrigation_advice}\n"
                f"- **Pesticide & Spraying:** {agri_adv.pesticide_advice}\n"
                f"- **Harvesting Guidance:** {agri_adv.harvest_recommendation}\n"
            )

        if av_brief:
            markdown_resp += f"\n#### ✈️ **Aviation Briefing ({av_brief.station_icao})**: {av_brief.flight_category} - {av_brief.metar_raw}\n"

        if marine_adv:
            markdown_resp += f"\n#### ⚓ **INCOIS Marine Advisory**: Waves {marine_adv.wave_height_m}m ({marine_adv.sea_condition}). {marine_adv.warning_message}\n"

        if alerts:
            markdown_resp += f"\n#### 🚨 **Active CAP Warnings**\n"
            for alt in alerts:
                markdown_resp += f"- **[{alt.severity.upper()} ALERT] {alt.headline}**\n"

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
