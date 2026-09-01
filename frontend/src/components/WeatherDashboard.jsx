import React from "react";
import { 
  Sun, CloudSun, CloudRain, Wind, Droplets, Compass, Gauge, 
  Sunrise, Sunset, Eye, AlertTriangle, ShieldCheck, MapPin, Sparkles, ArrowUpRight
} from "lucide-react";

export default function WeatherDashboard({ weatherData, isLoading, onAskAI }) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh] space-y-3">
        <div className="w-12 h-12 rounded-full border-4 border-sky-500 border-t-transparent animate-spin"></div>
        <p className="text-xs text-slate-400 font-medium">Fetching real-time NWP observations and satellite feeds...</p>
      </div>
    );
  }

  if (!weatherData) {
    return (
      <div className="text-center py-16 text-slate-400 text-sm">
        No weather telemetry available. Please search a location or click auto-detect.
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-2 sm:px-4 py-3 space-y-5 animate-fadeIn">
      {/* Primary Hero Weather Card */}
      <div className="glass-card p-6 border border-slate-700/80 relative overflow-hidden bg-gradient-to-br from-slate-900/90 via-slate-900/80 to-sky-950/40">
        <div className="relative z-10 flex flex-wrap items-center justify-between gap-6">
          {/* Location & Temp Details */}
          <div>
            <div className="flex items-center gap-2 text-sky-400 text-xs font-bold uppercase tracking-wider mb-1">
              <MapPin size={14} />
              <span>{weatherData.location}, {weatherData.state}</span>
              <span className="text-[10px] bg-sky-500/20 text-sky-300 px-2.5 py-0.5 rounded-full border border-sky-500/30 font-mono">
                {weatherData.nwp_model}
              </span>
            </div>
            <div className="flex items-baseline gap-4 mt-2">
              <span className="text-6xl sm:text-7xl font-black tracking-tight text-white font-heading">
                {weatherData.current_temp}°
                <span className="text-3xl text-slate-400 font-normal">C</span>
              </span>
              <div>
                <div className="text-xl font-bold text-slate-100">{weatherData.condition}</div>
                <div className="text-xs text-slate-400 font-medium mt-0.5">
                  Feels like <span className="text-slate-200 font-semibold">{weatherData.feels_like}°C</span> • High: <span className="text-white font-bold">{weatherData.daily[0]?.temp_max}°C</span> / Low: <span className="text-slate-400 font-medium">{weatherData.daily[0]?.temp_min}°C</span>
                </div>
              </div>
            </div>
          </div>

          {/* AQI Indicator & Ask AI button */}
          <div className="flex flex-col items-end gap-3">
            <div className="flex items-center gap-3 bg-slate-950/70 p-2.5 rounded-2xl border border-slate-800">
              <div className="text-right">
                <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Air Quality (AQI)</div>
                <div className="text-xs font-bold text-white">
                  <span className="text-emerald-400 font-extrabold">{weatherData.aqi_status}</span>
                </div>
              </div>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/15 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-extrabold text-sm font-mono shadow-sm">
                {weatherData.aqi}
              </div>
            </div>

            <button
              onClick={() => onAskAI(`Provide a comprehensive weather and disaster outlook for ${weatherData.location} for this week.`)}
              className="btn-primary text-xs py-2 px-3.5"
            >
              <Sparkles size={14} /> Ask WeatherGPT Insights
            </button>
          </div>
        </div>

        {/* 4-Metric Grid Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-slate-800/80">
          <div className="flex items-center gap-3 bg-slate-950/60 p-3 rounded-2xl border border-slate-800/90 shadow-sm">
            <div className="p-2.5 rounded-xl bg-sky-500/15 text-sky-400 border border-sky-500/20">
              <Droplets size={20} />
            </div>
            <div>
              <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Humidity</div>
              <div className="text-base font-extrabold text-white">{weatherData.humidity}%</div>
            </div>
          </div>

          <div className="flex items-center gap-3 bg-slate-950/60 p-3 rounded-2xl border border-slate-800/90 shadow-sm">
            <div className="p-2.5 rounded-xl bg-teal-500/15 text-teal-400 border border-teal-500/20">
              <Wind size={20} />
            </div>
            <div>
              <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Wind Velocity</div>
              <div className="text-base font-extrabold text-white">
                {weatherData.wind_speed} <span className="text-xs font-normal text-slate-400">km/h {weatherData.wind_direction}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 bg-slate-950/60 p-3 rounded-2xl border border-slate-800/90 shadow-sm">
            <div className="p-2.5 rounded-xl bg-amber-500/15 text-amber-400 border border-amber-500/20">
              <Sun size={20} />
            </div>
            <div>
              <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">UV Index</div>
              <div className="text-base font-extrabold text-white">
                {weatherData.uv_index} <span className="text-[10px] font-semibold text-amber-300">({weatherData.uv_index > 7 ? 'High' : 'Moderate'})</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 bg-slate-950/60 p-3 rounded-2xl border border-slate-800/90 shadow-sm">
            <div className="p-2.5 rounded-xl bg-indigo-500/15 text-indigo-400 border border-indigo-500/20">
              <Gauge size={20} />
            </div>
            <div>
              <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Surface Pressure</div>
              <div className="text-base font-extrabold text-white">{weatherData.pressure} <span className="text-xs font-normal text-slate-400">hPa</span></div>
            </div>
          </div>
        </div>
      </div>

      {/* Hourly Forecast Timeline */}
      <div className="glass-card p-5 border border-slate-800">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <span>⏱️ 12-Hour High-Resolution Ensemble Timeline</span>
          </h3>
          <span className="text-[10px] text-sky-400 font-mono">0.125° GFS Grid</span>
        </div>
        <div className="flex gap-3 overflow-x-auto pb-2 no-scrollbar">
          {weatherData.hourly.map((hr, idx) => (
            <div
              key={idx}
              className="flex-shrink-0 flex flex-col items-center justify-between p-3 min-w-[95px] rounded-2xl bg-slate-950/70 border border-slate-800/90 hover:border-sky-500/50 hover:bg-slate-900 transition duration-200"
            >
              <span className="text-xs text-slate-400 font-mono font-medium">{hr.time}</span>
              <div className="my-2.5 text-sky-400">
                <CloudSun size={24} />
              </div>
              <span className="text-sm font-extrabold text-white">{hr.temp}°</span>
              <span className="text-[10px] text-sky-300 mt-1 font-bold flex items-center gap-0.5 bg-sky-950/50 px-2 py-0.5 rounded-full border border-sky-800/40">
                💧 {hr.rain_prob}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 7-Day Matrix & Astronomical Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="lg:col-span-2 glass-card p-5 border border-slate-800">
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider mb-4">
            📅 7-Day Synoptic Weather Outlook
          </h3>
          <div className="space-y-2.5">
            {weatherData.daily.map((day, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3 rounded-xl bg-slate-950/50 border border-slate-800/80 hover:bg-slate-900 transition"
              >
                <div className="w-20 font-bold text-xs text-slate-200">{day.day}</div>
                <div className="flex items-center gap-2 text-xs text-slate-400 flex-1">
                  <CloudRain size={16} className="text-sky-400" />
                  <span className="font-medium text-slate-300">{day.condition}</span>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono">
                  <span className="text-slate-400 text-[11px]">💧 {day.rain_sum} mm</span>
                  <div className="flex items-center gap-2">
                    <span className="text-white font-extrabold">{day.temp_max}°</span>
                    <span className="text-slate-500 font-medium">{day.temp_min}°</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Solar & Astro Details */}
        <div className="glass-card p-5 border border-slate-800 space-y-4">
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            ☀️ Solar Cycle & Visibility
          </h3>

          <div className="space-y-2.5">
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center gap-2 text-amber-400">
                <Sunrise size={18} />
                <span className="text-xs text-slate-300 font-semibold">Sunrise</span>
              </div>
              <span className="text-xs font-bold text-white font-mono">{weatherData.sunrise} IST</span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center gap-2 text-orange-400">
                <Sunset size={18} />
                <span className="text-xs text-slate-300 font-semibold">Sunset</span>
              </div>
              <span className="text-xs font-bold text-white font-mono">{weatherData.sunset} IST</span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center gap-2 text-sky-400">
                <Eye size={18} />
                <span className="text-xs text-slate-300 font-semibold">Optical Visibility</span>
              </div>
              <span className="text-xs font-bold text-white">{weatherData.visibility} km</span>
            </div>
          </div>

          <div className="p-3 bg-sky-950/40 border border-sky-900/60 rounded-xl text-xs text-sky-200 leading-relaxed">
            💡 <strong>IMD Agromet Advisory:</strong> Good daytime solar radiation for agricultural drying. Check pesticide spray timing before evening humidity climb.
          </div>
        </div>
      </div>
    </div>
  );
}
