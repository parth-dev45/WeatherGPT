import React from "react";
import { 
  CloudSun, ShieldAlert, Sparkles, Navigation, Globe, UserCheck, 
  Search, Radio, Sprout, Plane, Waves, AlertTriangle, TrendingUp, LayoutGrid 
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
  activeAlertCount,
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
            🚨 <span className="font-bold text-red-300">[RED ALERT]</span> Cyclone 'VAAYU' approaching Odisha-WB Coast (120 kmph) • ⚠️ <span className="font-bold text-orange-300">[ORANGE ALERT]</span> Severe Heatwave across Vidarbha & West Rajasthan • ⚡ <span className="font-bold text-yellow-300">[DAMINI]</span> Cloud-to-ground lightning warnings active in Gangetic plains.
          </div>
        </div>
        <button 
          onClick={() => setActiveTab("alerts")} 
          className="flex-shrink-0 text-[10px] font-bold bg-red-600/80 hover:bg-red-500 text-white px-2 py-0.5 rounded-full transition shadow-sm"
        >
          {activeAlertCount} Warnings Active →
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
                Weather<span className="text-sky-400">GPT</span>
              </span>
              <span className="text-[9px] uppercase font-extrabold tracking-widest px-2 py-0.5 rounded-full bg-gradient-to-r from-sky-500/20 to-blue-500/20 text-sky-300 border border-sky-500/30">
                MoES • IMD
              </span>
            </div>
            <p className="text-[11px] text-gray-400 font-medium">Conversational AI & Early Warning Hub</p>
          </div>
        </div>

        {/* Global Search Location Bar */}
        <form onSubmit={onSearchSubmit} className="flex-1 max-w-sm min-w-[240px]">
          <div className="relative flex items-center">
            <Search size={14} className="absolute left-3 text-gray-400 pointer-events-none" />
            <input
              type="text"
              value={searchLocation}
              onChange={(e) => setSearchLocation(e.target.value)}
              placeholder="Search City, Agri District, Airport or Mandi..."
              className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-sky-500 focus:bg-slate-950 rounded-xl py-1.5 pl-8 pr-16 text-xs text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-sky-500/30 transition shadow-inner"
            />
            <div className="absolute right-1 flex items-center gap-1">
              <button
                type="button"
                onClick={onDetectLocation}
                title="Detect GPS Location"
                className="p-1 rounded-lg text-gray-400 hover:text-sky-400 hover:bg-slate-800 transition"
              >
                <Navigation size={13} />
              </button>
              <button
                type="submit"
                className="bg-sky-600 hover:bg-sky-500 text-white text-[10px] font-bold px-2 py-1 rounded-lg transition shadow-sm"
              >
                Go
              </button>
            </div>
          </div>
        </form>

        {/* Language Selector */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 bg-slate-900/90 border border-slate-700/80 rounded-xl px-2.5 py-1 text-xs">
            <Globe size={13} className="text-sky-400" />
            <select
              value={currentLanguage}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-[11px] font-medium text-gray-200 focus:outline-none cursor-pointer pr-1"
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code} className="bg-slate-900 text-gray-100">
                  {l.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Sub-bar: Persona Pills & Tab Navigators */}
      <div className="border-t border-slate-800/80 bg-slate-950/60 px-4 py-1.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between overflow-x-auto gap-3 no-scrollbar">
          {/* Persona Mode Pills */}
          <div className="flex items-center gap-1 flex-shrink-0">
            <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider mr-1">
              Persona:
            </span>
            {PERSONAS.map((p) => {
              const active = currentPersona === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => setPersona(p.id)}
                  className={`flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-lg font-semibold transition-all ${
                    active
                      ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-sm shadow-sky-500/20"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent"
                  }`}
                >
                  <span>{p.icon}</span>
                  <span>{p.label}</span>
                </button>
              );
            })}
          </div>

          {/* Tab Navigation Buttons */}
          <div className="flex items-center gap-1 bg-slate-900/90 p-0.5 rounded-xl border border-slate-800 flex-shrink-0">
            <button
              onClick={() => setActiveTab("chat")}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
                activeTab === "chat" 
                  ? "bg-gradient-to-r from-sky-600 to-blue-600 text-white shadow-md shadow-sky-600/30" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>💬</span> AI Chat & Voice
            </button>
            <button
              onClick={() => setActiveTab("map")}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
                activeTab === "map" 
                  ? "bg-gradient-to-r from-sky-600 to-blue-600 text-white shadow-md shadow-sky-600/30" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>🗺️</span> GIS Radar Map
            </button>
            <button
              onClick={() => setActiveTab("dashboard")}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
                activeTab === "dashboard" 
                  ? "bg-gradient-to-r from-sky-600 to-blue-600 text-white shadow-md shadow-sky-600/30" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>📊</span> Forecast Matrix
            </button>
            <button
              onClick={() => setActiveTab("agri")}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
                activeTab === "agri" 
                  ? "bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>🌾</span> Agromet
            </button>
            <button
              onClick={() => setActiveTab("alerts")}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
                activeTab === "alerts" 
                  ? "bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-md shadow-red-600/30" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>🚨</span> Warnings ({activeAlertCount})
            </button>
            <button
              onClick={() => setActiveTab("climate")}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
                activeTab === "climate" 
                  ? "bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-600/30" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>📈</span> Climate Trends
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
