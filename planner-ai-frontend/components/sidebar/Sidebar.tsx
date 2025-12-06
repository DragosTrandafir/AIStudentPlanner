"use client";

import { useState } from "react";
import MiniMonthView from "@/components/calendar/MiniMonthView";
import { useTheme } from "@/components/context/ThemeContext";
import FeedbackModal from "@/components/modals/FeedbackModal"; 
import "@/styles/sidebar.css";

interface SidebarProps {
  currentMonth: Date;
  selectedDate: Date | null;
  onSelectDate: (date: Date) => void;


  
  onGeneratePlan?: () => void;     // AI generate handler
  onRegeneratePlan?: (feedback: string) => void;
  canRegenerate?: boolean;
}

export default function Sidebar({
  currentMonth,
  selectedDate,
  onSelectDate,
  onGeneratePlan,
  onRegeneratePlan,
  //canRegenerate = false,
}: SidebarProps) {
  const { theme, setTheme } = useTheme();

  const [showFeedback, setShowFeedback] = useState(false);

  


  return (
    <div className="sidebar">

      {/* THEME SWITCHER ICONS */}
      <div className="theme-switcher">

        {/* Light */}
        <button
          className={`theme-icon-btn ${theme === "light" ? "active" : ""}`}
          onClick={() => setTheme("light")}
          aria-label="Light Theme"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="4" />
            <line x1="12" y1="2" x2="12" y2="6" />
            <line x1="12" y1="18" x2="12" y2="22" />
            <line x1="4.93" y1="4.93" x2="7.76" y2="7.76" />
            <line x1="16.24" y1="16.24" x2="19.07" y2="19.07" />
            <line x1="2" y1="12" x2="6" y2="12" />
            <line x1="18" y1="12" x2="22" y2="12" />
            <line x1="4.93" y1="19.07" x2="7.76" y2="16.24" />
            <line x1="16.24" y1="7.76" x2="19.07" y2="4.93" />
          </svg>
        </button>

        {/* Dark */}
        <button
          className={`theme-icon-btn ${theme === "dark" ? "active" : ""}`}
          onClick={() => setTheme("dark")}
          aria-label="Dark Theme"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        </button>

        {/* Pink */}
        <button
          className={`theme-icon-btn ${theme === "pink" ? "active" : ""}`}
          onClick={() => setTheme("pink")}
          aria-label="Pink Theme"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3z" />
            <path d="M5 14l.8 2.2L8 17l-2.2.8L5 20l-.8-2.2L2 17l2.2-.8L5 14z" />
            <path d="M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8L19 14z" />
          </svg>
        </button>

      </div>

       {/* AI BUTTONS */}
      <div className="ai-buttons">
        <button
          className="ai-generate-btn"
          onClick={onGeneratePlan}
        >
          ⚡ Generate Plan
        </button>

      
      </div>

      {/* FEEDBACK BUTTON SECTION */}
      <div>

        <button
    className="feedback-sidebar-btn"
    onClick={() => setShowFeedback(true)}
  >
    Feedback
  </button>
      </div>

      {/* MINI CALENDAR */}
      <MiniMonthView
        selectedMonth={currentMonth}
        selectedDate={selectedDate}
        onSelect={(date) => onSelectDate(date)}
      />

      {/* FEEDBACK POPUP */}
       {showFeedback && (
        <FeedbackModal
  onClose={() => setShowFeedback(false)}
  onSubmit={(rating, message) => {
    setShowFeedback(false);

    if (onRegeneratePlan) {
      onRegeneratePlan(message);   // 🔥 Use feedback to regenerate the plan
    }
  }}
/>

      )}

    </div>
  );
}
