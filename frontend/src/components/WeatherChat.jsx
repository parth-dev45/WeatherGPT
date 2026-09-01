import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { 
  Send, Mic, MicOff, Volume2, VolumeX, Sparkles, 
  MapPin, CheckCircle2, ChevronRight, User, Bot, Radio
} from "lucide-react";
import { speechEngine } from "../services/voice";
import ModernWeatherCard from "./ModernWeatherCard";

const PROMPT_CHIPS = [
  { text: "🌧️ Will it rain heavily in Mumbai tomorrow?", category: "Forecast" },
  { text: "🌾 Cotton crop spray advisory for Nagpur district", category: "Agromet" },
  { text: "🚨 Active cyclone track & landfall forecast for Odisha", category: "Disaster" },
  { text: "✈️ METAR & TAF weather briefing for Delhi VIDP", category: "Aviation" },
  { text: "⚓ Ocean wave height & fisherman warning for Kochi", category: "Marine" },
  { text: "📈 Compare this year's monsoon vs 30-year IMD average", category: "Climate" }
];

export default function WeatherChat({
  messages,
  onSendMessage,
  isLoading,
  currentLanguage,
  currentPersona,
  onNavigateTab
}) {
  const [inputText, setInputText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [activeSpeechId, setActiveSpeechId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText.trim());
    setInputText("");
  };

  const handleToggleVoice = () => {
    if (isRecording) {
      speechEngine.stopListening();
      setIsRecording(false);
    } else {
      speechEngine.startListening(
        currentLanguage,
        (transcript, isFinal) => {
          setInputText(transcript);
          if (isFinal) {
            setIsRecording(false);
          }
        },
        () => setIsRecording(false),
        (err) => {
          console.warn("Speech error:", err);
          setIsRecording(false);
        }
      );
      setIsRecording(true);
    }
  };

  const handleSpeak = (msgId, text) => {
    if (activeSpeechId === msgId) {
      speechEngine.stopSpeaking();
      setActiveSpeechId(null);
    } else {
      speechEngine.speak(text, currentLanguage, () => {
        setActiveSpeechId(null);
      });
      setActiveSpeechId(msgId);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] max-w-5xl mx-auto px-2 sm:px-4 py-2">
      {/* Messages Stream Container */}
      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {messages.map((msg, index) => {
          const isUser = msg.sender === "user";
          return (
            <div
              key={msg.id || index}
              className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} animate-fadeIn`}
            >
              {/* Avatar Icon */}
              <div className={`flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shadow-md ${
                isUser 
                  ? "bg-gradient-to-tr from-sky-600 to-blue-500 text-white shadow-sky-500/20" 
                  : "bg-gradient-to-tr from-indigo-600 via-sky-600 to-teal-500 text-white shadow-indigo-500/20"
              }`}>
                {isUser ? <User size={15} /> : <Bot size={15} />}
              </div>

              {/* Chat Bubble */}
              <div
                className={`max-w-[88%] rounded-2xl p-4 transition-all ${
                  isUser
                    ? "bg-gradient-to-r from-sky-600 via-blue-600 to-blue-700 text-white rounded-tr-none shadow-lg shadow-sky-600/20 border border-sky-400/30"
                    : "glass-card text-slate-100 rounded-tl-none border border-slate-700/80 bg-slate-900/80 shadow-xl"
                }`}
              >
                {/* Header with Title & Audio button */}
                <div className="flex items-center justify-between gap-4 mb-2 pb-1.5 border-b border-white/10 text-xs">
                  <div className="flex items-center gap-1.5 font-bold">
                    {isUser ? (
                      <span className="text-sky-100">You</span>
                    ) : (
                      <span className="flex items-center gap-1.5 gradient-text-sky font-extrabold tracking-wide">
                        <Sparkles size={13} className="text-sky-400" /> WeatherGPT Intelligence
                      </span>
                    )}
                  </div>
                  {!isUser && msg.speech_text && (
                    <button
                      onClick={() => handleSpeak(msg.id || index, msg.speech_text)}
                      title="Listen with Indic Voice Synthesizer"
                      className={`p-1.5 rounded-lg text-xs flex items-center gap-1 transition ${
                        activeSpeechId === (msg.id || index)
                          ? "bg-sky-500 text-white animate-pulse"
                          : "text-slate-400 hover:text-sky-300 hover:bg-white/10"
                      }`}
                    >
                      {activeSpeechId === (msg.id || index) ? <VolumeX size={14} /> : <Volume2 size={14} />}
                      <span className="text-[10px] hidden sm:inline">{activeSpeechId === (msg.id || index) ? "Mute" : "Listen"}</span>
                    </button>
                  )}
                </div>

                {/* Rich Formatted Markdown Content */}
                <div className="text-xs sm:text-sm leading-relaxed text-slate-200 prose prose-invert max-w-none prose-p:my-1 prose-headings:my-2 prose-ul:my-1">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>

                {/* Modern Weather Card (Matching the Reference UI) */}
                {msg.weather && (
                  <div className="mt-4">
                    <ModernWeatherCard weather={msg.weather} />
                  </div>
                )}

                {/* Suggested Action Buttons */}
                {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                  <div className="mt-3.5 pt-2 border-t border-white/10 flex flex-wrap gap-1.5">
                    {msg.suggested_actions.map((act, i) => (
                      <button
                        key={i}
                        onClick={() => onNavigateTab(act.action.replace("open_", ""))}
                        className="text-xs font-semibold bg-sky-500/10 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 px-2.5 py-1 rounded-lg flex items-center gap-1 transition shadow-sm"
                      >
                        <span>{act.label}</span>
                        <ChevronRight size={11} />
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Pulse */}
        {isLoading && (
          <div className="flex items-center gap-2 text-sky-400 text-xs font-semibold py-2.5 px-4 glass-card max-w-fit rounded-xl animate-pulse">
            <Sparkles size={15} className="animate-spin" />
            <span>Formulating weather intelligence from IMD NWP ensemble...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div className="py-2 overflow-x-auto no-scrollbar flex gap-2">
        {PROMPT_CHIPS.map((chip, i) => (
          <button
            key={i}
            onClick={() => onSendMessage(chip.text)}
            className="flex-shrink-0 text-xs font-medium bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/80 hover:border-sky-500/50 px-3 py-1.5 rounded-full transition shadow-sm hover:shadow-sky-500/10"
          >
            {chip.text}
          </button>
        ))}
      </div>

      {/* Modern Input Bar with Voice Mic */}
      <form onSubmit={handleSubmit} className="relative flex items-center gap-2 mt-1">
        <div className="relative flex-1 flex items-center">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={
              isRecording
                ? "🎙️ Listening in Indic voice mode... Speak clearly now"
                : "Ask weather forecasts, crop advisories, or disaster alerts in Hindi, Marathi, Tamil, English..."
            }
            className={`w-full bg-slate-900/95 border ${
              isRecording 
                ? "border-red-500 ring-4 ring-red-500/20 text-white" 
                : "border-slate-700/80 focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30"
            } rounded-2xl py-3 pl-4 pr-12 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none transition shadow-2xl`}
          />
          <button
            type="button"
            onClick={handleToggleVoice}
            title={isRecording ? "Stop Recording" : "Voice Input (Bhashini / Web Speech)"}
            className={`absolute right-2.5 p-2 rounded-xl transition ${
              isRecording
                ? "mic-active"
                : "bg-slate-800/90 text-slate-400 hover:text-sky-400 hover:bg-slate-700"
            }`}
          >
            {isRecording ? <MicOff size={18} /> : <Mic size={18} />}
          </button>
        </div>

        <button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          className="btn-primary p-3 rounded-2xl flex items-center justify-center disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
