"use client";

import { useState, useEffect } from "react";
import { User, Sun, Moon, Sparkles } from "lucide-react";

import UserProfileModal from "@/components/authenticate/UserProfileModal";
import MiniMonthView from "@/components/calendar/MiniMonthView";
import { useTheme } from "@/components/context/ThemeContext";
import FeedbackModal from "@/components/modals/FeedbackModal";
import { loadUser, type StoredUser } from "@/utils/userStorage";
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

  const [currentUser, setCurrentUser] = useState<StoredUser | null>(null);

  // 3. Effect to load user data when Sidebar appears
  useEffect(() => {
    // Check if we are in the browser (client-side) to avoid server errors
    if (typeof window !== "undefined") {
      const loaded = loadUser();
      if (loaded) {
        setCurrentUser(loaded);
      }
    }
  }, []);

  // Default fallback if no user is found (e.g. fresh load before login)
  const displayUser = currentUser || {
    fullName: "Guest User",
    username: "guest",
    email: "Not signed in"
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
          user={displayUser}           // ✅ Passing real data

          onClose={() => setShowProfile(false)}
          onSignOut={() => {
            setShowProfile(false);
            window.location.reload();
          }}
        />
      )}

    </aside>
  );
}
