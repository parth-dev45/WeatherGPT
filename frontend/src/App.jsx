import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import WeatherChat from "./components/WeatherChat";
import GISMap from "./components/GISMap";
import WeatherDashboard from "./components/WeatherDashboard";
import AgriAdvisor from "./components/AgriAdvisor";
import AviationMarine from "./components/AviationMarine";
import AlertCenter from "./components/AlertCenter";
import ClimateAnalytics from "./components/ClimateAnalytics";
import { sendChatQuery, fetchCurrentWeather, fetchActiveAlerts } from "./services/api";

export default function App() {
  const [currentPersona, setPersona] = useState("general");
  const [currentLanguage, setLanguage] = useState("auto");
  const [activeTab, setActiveTab] = useState("chat");
  const [searchLocation, setSearchLocation] = useState("Pune");
  const [weatherData, setWeatherData] = useState(null);
  const [activeAlertCount, setActiveAlertCount] = useState(4);
  const [isLoading, setIsLoading] = useState(false);

  // Initial Welcome Messages
  const [messages, setMessages] = useState([
    {
      id: "init-1",
      sender: "bot",
      text: "Namaste! 🙏 Welcome to **WeatherGPT** — the AI conversational intelligence platform built for the **Ministry of Earth Sciences (MoES)** and **India Meteorological Department (IMD)**.\n\nAsk me anything regarding real-time forecasts, GFS/WRF model outputs, **Agromet crop advisories (Meghdoot)**, **Damini lightning risks**, **aviation METAR/TAF**, **marine sea states**, or **ITU CAP disaster warnings** in 10+ Indian languages.",
      speech_text: "Namaste! Welcome to WeatherGPT. How can I assist you with weather forecasts or disaster alerts today?",
      suggested_actions: [
        { label: "View Doppler Radar Map", action: "open_map" },
        { label: "7-Day Forecast Matrix", action: "open_dashboard" },
        { label: "Farmers Agromet Advisory", action: "open_agri" },
        { label: "Active CAP Disaster Alerts", action: "open_alerts" }
      ]
    }
  ]);

  // Initial Weather Load for default location
  useEffect(() => {
    const initData = async () => {
      try {
        const data = await fetchCurrentWeather("Pune");
        setWeatherData(data);
        const alerts = await fetchActiveAlerts();
        setActiveAlertCount(alerts.length);
      } catch (e) {
        console.error("Initial data load error:", e);
      }
    };
    initData();
  }, []);

  // Handle User Message in Chat
  const handleSendMessage = async (text) => {
    const userMsg = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: text
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await sendChatQuery(text, currentPersona, currentLanguage, searchLocation);
      const botMsg = {
        id: `bot-${Date.now()}`,
        sender: "bot",
        text: response.markdown_response,
        speech_text: response.speech_text,
        weather: response.structured_weather,
        alerts: response.alerts,
        suggested_actions: response.suggested_actions
      };
      setMessages((prev) => [...prev, botMsg]);

      // If response contained weather telemetry, update dashboard state
      if (response.structured_weather) {
        setWeatherData(response.structured_weather);
        setSearchLocation(response.structured_weather.location);
      }
    } catch (err) {
      console.error("Chat error:", err);
      const errorMsg = {
        id: `bot-err-${Date.now()}`,
        sender: "bot",
        text: "⚠️ Unable to connect to WeatherGPT Backend. Please ensure the FastAPI server is running on `http://127.0.0.1:8000`.",
        speech_text: "Connection error with weather server."
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  // Location Search
  const handleSearchSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!searchLocation.trim()) return;
    setIsLoading(true);
    try {
      const data = await fetchCurrentWeather(searchLocation.trim());
      setWeatherData(data);
      // Auto query chat for the searched location
      handleSendMessage(`Current weather and 7-day outlook for ${searchLocation.trim()}`);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  // GPS Auto-detect
  const handleDetectLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          setIsLoading(true);
          try {
            const data = await fetchCurrentWeather("Your Location", latitude, longitude);
            setWeatherData(data);
            setSearchLocation(data.location);
            handleSendMessage(`Weather forecast for coordinates (${latitude.toFixed(2)}, ${longitude.toFixed(2)})`);
          } catch (e) {
            console.error(e);
          } finally {
            setIsLoading(false);
          }
        },
        () => {
          handleSearchSubmit();
        }
      );
    } else {
      handleSearchSubmit();
    }
  };

  const handleAskAI = (prompt) => {
    setActiveTab("chat");
    handleSendMessage(prompt);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-main)] text-[var(--text-main)]">
      {/* Top Navbar & Controls */}
      <Navbar
        currentPersona={currentPersona}
        setPersona={setPersona}
        currentLanguage={currentLanguage}
        setLanguage={setLanguage}
        activeAlertCount={activeAlertCount}
        searchLocation={searchLocation}
        setSearchLocation={setSearchLocation}
        onSearchSubmit={handleSearchSubmit}
        onDetectLocation={handleDetectLocation}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Main Content View Switcher */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-2 sm:p-4">
        {activeTab === "chat" && (
          <WeatherChat
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            currentLanguage={currentLanguage}
            currentPersona={currentPersona}
            onNavigateTab={(tab) => setActiveTab(tab)}
          />
        )}

        {activeTab === "map" && (
          <GISMap
            selectedLocation={searchLocation}
            onSelectLocation={(loc) => {
              setSearchLocation(loc);
              handleAskAI(`Detailed weather and hazard forecast for ${loc}`);
            }}
          />
        )}

        {activeTab === "dashboard" && (
          <WeatherDashboard
            weatherData={weatherData}
            isLoading={isLoading}
            onAskAI={handleAskAI}
          />
        )}

        {activeTab === "agri" && (
          <AgriAdvisor
            currentDistrict={weatherData ? weatherData.location : "Nagpur"}
            currentState={weatherData ? weatherData.state : "Maharashtra"}
            onAskAI={handleAskAI}
          />
        )}

        {activeTab === "alerts" && (
          <AlertCenter
            onAskAI={handleAskAI}
            onFocusMapZone={() => setActiveTab("map")}
          />
        )}

        {activeTab === "climate" && (
          <ClimateAnalytics
            onAskAI={handleAskAI}
          />
        )}

        {(currentPersona === "aviation" || currentPersona === "marine") && activeTab === "dashboard" && (
          <div className="mt-6">
            <AviationMarine onAskAI={handleAskAI} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800/80 py-3 text-center text-xs text-gray-500 glass-panel">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-2">
          <span>WeatherGPT Platform • Ministry of Earth Sciences (MoES) / IMD Innovation</span>
          <span className="font-mono text-[11px] text-gray-400">ITU CAP v1.2 • WMO WIS2.0 • GFS-WRF Ensemble 0.125°</span>
        </div>
      </footer>
    </div>
  );
}
