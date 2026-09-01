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
  const [activeAlerts, setActiveAlerts] = useState([]);
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
        setActiveAlerts(alerts);
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
      const resp = await sendChatQuery(text, currentPersona, currentLanguage, searchLocation);
      
      const botMsg = {
        id: `bot-${Date.now()}`,
        sender: "bot",
        text: resp.markdown_response,
        speech_text: resp.speech_text,
        weather: resp.structured_weather,
        alerts: resp.alerts,
        agri_advisory: resp.agri_advisory,
        aviation_briefing: resp.aviation_briefing,
        marine_advisory: resp.marine_advisory,
        suggested_actions: resp.suggested_actions,
        quick_suggestions: resp.quick_suggestions
      };

      setMessages((prev) => [...prev, botMsg]);

      // If response contained structured weather, sync to active search state
      if (resp.structured_weather) {
        setWeatherData(resp.structured_weather);
        setSearchLocation(resp.structured_weather.location);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          sender: "bot",
          text: "⚠️ **Communication Anomaly**: Could not connect to the WeatherGPT forecasting cluster. Please ensure the backend server is running and try again.",
          speech_text: "Could not connect to the weather forecasting cluster. Please try again."
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Search Submit
  const handleSearchSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!searchLocation.trim()) return;

    setIsLoading(true);
    try {
      const data = await fetchCurrentWeather(searchLocation.trim());
      setWeatherData(data);
      handleSendMessage(`Give me a complete weather intelligence and hazard summary for ${searchLocation.trim()}`);
    } catch (err) {
      console.error(err);
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
        activeAlerts={activeAlerts}
        activeAlertCount={activeAlerts.length}
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
            location={searchLocation}
            onAskAI={handleAskAI}
          />
        )}

        {activeTab === "aviation_marine" && (
          <AviationMarine
            location={searchLocation}
            onAskAI={handleAskAI}
          />
        )}

        {activeTab === "alerts" && (
          <AlertCenter
            onSelectAlertLocation={(loc) => {
              setSearchLocation(loc);
              handleAskAI(`Disaster advisory and mitigation instructions for active alert in ${loc}`);
            }}
          />
        )}

        {activeTab === "climate" && (
          <ClimateAnalytics />
        )}
      </main>

      {/* Modern Status Footer */}
      <footer className="glass-panel border-t border-slate-800/80 py-2.5 px-4 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-200">WeatherGPT Platform</span>
            <span>•</span>
            <span>Ministry of Earth Sciences (MoES) / IMD Innovation</span>
          </div>
          <div className="flex items-center gap-3 text-[11px] font-mono text-slate-300">
            <span>ITU CAP v1.2</span>
            <span>•</span>
            <span>WMO WIS2.0</span>
            <span>•</span>
            <span>GFS-WRF Ensemble 0.125°</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
