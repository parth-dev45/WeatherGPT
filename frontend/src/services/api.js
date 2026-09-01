const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function sendChatQuery(query, persona = "general", language = "auto", locationName = "") {
  const res = await fetch(`${API_BASE_URL}/chat/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      persona,
      language,
      location_name: locationName
    })
  });
  if (!res.ok) throw new Error("Failed to query WeatherGPT engine");
  return await res.json();
}

export async function fetchCurrentWeather(location = "New Delhi", lat = null, lon = null) {
  let url = `${API_BASE_URL}/weather/current?location=${encodeURIComponent(location)}`;
  if (lat !== null && lon !== null) {
    url += `&lat=${lat}&lon=${lon}`;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch current weather");
  return await res.json();
}

export async function fetchActiveAlerts(severity = null) {
  let url = `${API_BASE_URL}/alerts/active`;
  if (severity) url += `?severity=${severity}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch active alerts");
  return await res.json();
}

export async function fetchCycloneTrack() {
  const res = await fetch(`${API_BASE_URL}/alerts/cyclone-track`);
  if (!res.ok) throw new Error("Failed to fetch cyclone track");
  return await res.json();
}

export async function fetchCropAdvisory(crop = "paddy", district = "Nagpur", state = "Maharashtra") {
  const res = await fetch(`${API_BASE_URL}/advisory/crop?crop=${encodeURIComponent(crop)}&district=${encodeURIComponent(district)}&state=${encodeURIComponent(state)}`);
  if (!res.ok) throw new Error("Failed to fetch crop advisory");
  return await res.json();
}

export async function fetchAviationBriefing(airport = "VIDP") {
  const res = await fetch(`${API_BASE_URL}/aviation/briefing?airport=${encodeURIComponent(airport)}`);
  if (!res.ok) throw new Error("Failed to fetch aviation briefing");
  return await res.json();
}

export async function fetchMarineAdvisory(location = "Mumbai") {
  const res = await fetch(`${API_BASE_URL}/marine/advisory?location=${encodeURIComponent(location)}`);
  if (!res.ok) throw new Error("Failed to fetch marine advisory");
  return await res.json();
}

export async function fetchClimateTrends(region = "All India") {
  const res = await fetch(`${API_BASE_URL}/climate/trends?region=${encodeURIComponent(region)}`);
  if (!res.ok) throw new Error("Failed to fetch climate trends");
  return await res.json();
}
