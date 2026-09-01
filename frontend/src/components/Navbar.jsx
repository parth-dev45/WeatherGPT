import React from "react";
import { 
  CloudSun, ShieldAlert, Sparkles, Navigation, Globe, UserCheck, 
  Search, Radio, Sprout, Plane, Waves, AlertTriangle, TrendingUp, LayoutGrid, Scale 
} from "lucide-react";

const PERSONAS = [
  { id: "general", label: "Public", icon: "🌐", desc: "Daily Forecasts & Alerts" },
  { id: "farmer", label: "Farmers (Agromet)", icon: "🌾", desc: "Crop Advisories & Pests" },
  { id: "disaster_manager", label: "Disaster Cell", icon: "🚨", desc: "CAP Warnings & Cyclones" },
  { id: "aviation", label: "Aviation", icon: "✈️", desc: "METAR / TAF Reports" },
  { id: "marine", label: "Marine / Port", icon: "⚓", desc: "Ocean State & Waves" },
];

const LANGUAGES = [
  { code: "auto", name: "🌐 Auto Detect (स्वचालित)" },
  { code: "en", name: "English" },
  { code: "hi", name: "हिन्दी (Hindi)" },
  { code: "mr", name: "मराठी (Marathi)" },
  { code: "ta", name: "தமிழ் (Tamil)" },
  { code: "te", name: "తెలుగు (Telugu)" },
  { code: "bn", name: "বাংলা (Bengali)" },
  { code: "gu", name: "ગુજરાતી (Gujarati)" },
  { code: "pa", name: "ਪੰਜਾਬੀ (Punjabi)" },
  { code: "kn", name: "ಕನ್ನಡ (Kannada)" }
];

export default function Navbar({
  currentPersona,
  setPersona,
  currentLanguage,
  setLanguage,
  activeAlerts = [],
  activeAlertCount = 0,
  searchLocation,
  setSearchLocation,
  onSearchSubmit,
  onDetectLocation,
  activeTab,
  setActiveTab
}) {
  return (
    <header className="sticky top-0 z-50 glass-panel">
      {/* Top Emergency Marquee Ticker */}
      <div className="bg-gradient-to-r from-red-950/80 via-red-900/60 to-red-950/80 border-b border-red-800/40 text-red-200 text-xs py-1 px-4 flex items-center justify-between overflow-hidden">
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
          </span>
          <span className="font-bold uppercase tracking-wider text-[10px] text-red-300 flex items-center gap-1">
            <Radio size={11} className="text-red-400" /> WMO WIS2.0 / IMD CAP Live
          </span>
        </div>
        <div className="overflow-hidden whitespace-nowrap mx-4 flex-1">
          <div className="animate-marquee inline-block font-medium text-[11px] text-red-100">
            {activeAlerts && activeAlerts.length > 0 ? (
              activeAlerts.map((alt, idx) => (
                <span key={alt.id || idx} className="inline-block mr-8">
                  {alt.severity === "Red" ? "🚨" : alt.severity === "Orange" ? "⚠️" : "⚡"}{" "}
                  <span className={`font-bold ${alt.severity === "Red" ? "text-red-300" : alt.severity === "Orange" ? "text-orange-300" : "text-yellow-300"}`}>
                    [{alt.severity.toUpperCase()} ALERT]
                  </span>{" "}
                  {alt.headline}
                </span>
              ))
            ) : (
              <span>
                📡 <span className="font-bold text-emerald-300">[LIVE TELEMETRY]</span> Real-time hazard monitoring active across all Indian meteorological observation stations • GFS/WRF model ensemble operational.
              </span>
            )}
          </div>
        </div>
        <button 
          onClick={() => setActiveTab("alerts")} 
          className="flex-shrink-0 text-[10px] font-bold bg-red-600/80 hover:bg-red-500 text-white px-2.5 py-0.5 rounded-full transition shadow-sm"
        >
          {activeAlertCount} {activeAlertCount === 1 ? "Warning" : "Warnings"} Active →
        </button>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-3">
        {/* Brand Identity */}
        <div 
          className="flex items-center gap-3 cursor-pointer group" 
          onClick={() => setActiveTab("chat")}
        >
          <div className="relative flex items-center justify-center w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-500 via-blue-600 to-indigo-600 shadow-lg shadow-sky-500/25 text-white font-bold group-hover:scale-105 transition-transform duration-300">
            <CloudSun size={22} className="text-white animate-pulse" />
            <div className="absolute inset-0 rounded-2xl bg-sky-400/20 blur-sm"></div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-black tracking-tight text-white flex items-center font-heading">
                Weather<span className="gradient-text-sky">GPT</span>
              </span>
              <span className="text-[10px] uppercase font-bold tracking-widest px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">
                MoES • IMD
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-medium">Conversational AI & Early Warning Hub</p>
          </div>
        </div>

        {/* Global Search Bar */}
        <form onSubmit={onSearchSubmit} className="flex-1 max-w-md mx-2 min-w-[240px]">
          <div className="relative flex items-center">
            <Search size={15} className="absolute left-3 text-slate-400" />
            <input
              type="text"
              value={searchLocation}
              onChange={(e) => setSearchLocation(e.target.value)}
              placeholder="Search 250+ Indian cities, districts or tehsils..."
              className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20 rounded-xl py-1.5 pl-9 pr-20 text-xs text-slate-100 placeholder-slate-500 focus:outline-none transition shadow-inner"
            />
            <div className="absolute right-1 flex items-center gap-1">
              <button
                type="button"
                onClick={onDetectLocation}
                title="Auto-detect GPS Location"
                className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-sky-400 transition"
              >
                <Navigation size={13} />
              </button>
              <button
                type="submit"
                className="bg-sky-600 hover:bg-sky-500 text-white text-[10px] font-bold px-2 py-1 rounded-lg transition"
              >
                Go
              </button>
            </div>
          </div>
        </form>

        {/* Language & Action Controls */}
        <div className="flex items-center gap-2">
          <div className="relative flex items-center">
            <select
              value={currentLanguage}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-slate-900/90 border border-slate-700/80 text-slate-200 text-xs rounded-xl px-2.5 py-1.5 focus:outline-none focus:border-sky-500 font-medium cursor-pointer shadow-sm"
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code} className="bg-slate-900 text-slate-200">
                  {lang.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Secondary Persona & Navigation Bar */}
      <div className="border-t border-slate-800/80 bg-slate-950/60 backdrop-blur-md px-4 py-1.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4 overflow-x-auto no-scrollbar">
          {/* Persona Switcher Pills */}
          <div className="flex items-center gap-1.5 flex-shrink-0">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mr-1 hidden sm:inline">
              Persona:
            </span>
            {PERSONAS.map((p) => {
              const isActive = currentPersona === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => setPersona(p.id)}
                  title={p.desc}
                  className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                    isActive
                      ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-850"
                  }`}
                >
                  <span>{p.icon}</span>
                  <span className="text-[11px]">{p.label}</span>
                </button>
              );
            })}
          </div>

          {/* Module Tab Switcher */}
          <div className="flex items-center gap-1.5 border-l border-slate-800 pl-3 flex-shrink-0">
            <button
              onClick={() => setActiveTab("chat")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "chat"
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Sparkles size={13} className={activeTab === "chat" ? "text-sky-400" : "text-slate-400"} />
              <span>AI Chat & Voice</span>
            </button>

            <button
              onClick={() => setActiveTab("map")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "map"
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <span>🗺️</span>
              <span>GIS Radar Map</span>
            </button>

            <button
              onClick={() => setActiveTab("dashboard")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "dashboard"
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <span>📊</span>
              <span>Forecast Matrix</span>
            </button>

            <button
              onClick={() => setActiveTab("agri")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "agri"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Sprout size={13} className={activeTab === "agri" ? "text-emerald-400" : "text-slate-400"} />
              <span>Agromet</span>
            </button>

            <button
              onClick={() => setActiveTab("alerts")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "alerts"
                  ? "bg-red-500/20 text-red-300 border border-red-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <ShieldAlert size={13} className={activeTab === "alerts" ? "text-red-400" : "text-slate-400"} />
              <span>Warnings ({activeAlertCount})</span>
            </button>

            <button
              onClick={() => setActiveTab("compare")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "compare"
                  ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Scale size={13} className={activeTab === "compare" ? "text-indigo-400" : "text-slate-400"} />
              <span>Compare & AQI</span>
            </button>

            <button
              onClick={() => setActiveTab("climate")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition cursor-pointer ${
                activeTab === "climate"
                  ? "bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <TrendingUp size={13} className={activeTab === "climate" ? "text-purple-400" : "text-slate-400"} />
              <span>Climate</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
