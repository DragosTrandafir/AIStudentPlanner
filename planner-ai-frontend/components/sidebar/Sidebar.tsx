"use client";

import { useState } from "react";
import { User, Sun, Moon, Sparkles } from "lucide-react";

import UserProfileModal from "@/components/authenticate/user/UserProfileModal";
import MiniMonthView from "@/components/calendar/MiniMonthView";
import { useTheme } from "@/components/context/ThemeContext";
import FeedbackModal from "@/components/modals/FeedbackModal";
import "@/styles/sidebar.css";

interface SidebarProps {
  currentMonth: Date;
  selectedDate: Date | null;
  onSelectDate: (date: Date) => void;
  onGeneratePlan?: () => void;
  onRegeneratePlan?: (feedback: string) => void;
  canRegenerate?: boolean;
  isGenerating?: boolean;
}

export default function Sidebar({
  currentMonth,
  selectedDate,
  onSelectDate,
  onGeneratePlan,
  onRegeneratePlan,
  //canRegenerate = false,
  isGenerating = false,
}: SidebarProps) {
  const { theme, setTheme } = useTheme();

  const [showFeedback, setShowFeedback] = useState(false);
  const [showProfile, setShowProfile] = useState(false);

  /* ✅ YOUR REAL DATA (replace with your actual values) */
  const user = {
    fullName: "name",
    username: "username",
    email: "email",
  };

  return (
    <aside className="sidebar">

      {/* USER AVATAR */}
      <button
        className={`user-avatar ${theme}`}
        aria-label="User profile"
        onClick={() => setShowProfile(true)}
      >
        <User size={26} />
      </button>

      {/* THEME SWITCHER */}
      <div className="theme-switcher">
        <button
          className={`theme-icon-btn ${theme === "light" ? "active" : ""}`}
          onClick={() => setTheme("light")}
        >
          <Sun size={18} />
        </button>

        <button
          className={`theme-icon-btn ${theme === "dark" ? "active" : ""}`}
          onClick={() => setTheme("dark")}
        >
          <Moon size={18} />
        </button>

        <button
          className={`theme-icon-btn ${theme === "pink" ? "active" : ""}`}
          onClick={() => setTheme("pink")}
        >
          <Sparkles size={18} />
        </button>
      </div>

      {/* AI BUTTON */}
      <div className="ai-buttons">
        <button
          className="ai-generate-btn"
          onClick={onGeneratePlan}
          disabled={isGenerating}
        >
          {isGenerating ? "⏳ Generating..." : "⚡ Generate Plan"}
        </button>
      </div>

      {/* FEEDBACK */}
      <button
        className="feedback-sidebar-btn"
        onClick={() => setShowFeedback(true)}
      >
        Feedback
      </button>

      {/* MINI CALENDAR */}
      <MiniMonthView
        selectedMonth={currentMonth}
        selectedDate={selectedDate}
        onSelect={onSelectDate}
      />

      {/* FEEDBACK MODAL */}
      {showFeedback && (
        <FeedbackModal
          onClose={() => setShowFeedback(false)}
          onSubmit={(rating, message) => {
            setShowFeedback(false);
            onRegeneratePlan?.(message);
          }}
        />
      )}

      {/* USER PROFILE MODAL */}
      {showProfile && (
        <UserProfileModal
          user={user}
          onClose={() => setShowProfile(false)}
          onSignOut={() => {
            setShowProfile(false);
            window.location.reload(); // back to login
          }}
        />
      )}

    </aside>
  );
}
