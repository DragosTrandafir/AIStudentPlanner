"use client";

import { useState, useEffect } from "react";
import LoginForm from "./LoginForm";
import UserProfileModal from "./UserProfileModal";
import { saveUser, loadUser, clearUser, type StoredUser } from "@/utils/userStorage";

export default function UserAuthLayout() {
  const [currentUser, setCurrentUser] = useState<StoredUser | null>(null);
  const [showProfile, setShowProfile] = useState(false);
  const [showLogin, setShowLogin] = useState(true); // show login form initially

  // Load logged-in user from localStorage on mount
  useEffect(() => {
    const stored = loadUser();
    if (stored) {
      setCurrentUser(stored);
      setShowLogin(false);
    }
  }, []);

  // Called when login succeeds
  const handleLoginSuccess = (userData: any) => {
  console.log("DEBUG: Raw Backend Data ->", userData);

  // This mapping ensures we translate Python snake_case to your TypeScript camelCase
  const storedUser: StoredUser = {
    // Try full_name first, then name, then fall back to "Missing Name"
    fullName: userData.full_name || userData.name || "Missing Name",

    // Try username, then fall back to "Missing Username"
    username: userData.username || "Missing Username",

    // Try email, then fall back to "Missing Email"
    email: userData.email || "Missing Email",
  };

  console.log("DEBUG: Mapped Object for Storage ->", storedUser);

  saveUser(storedUser);
  setCurrentUser(storedUser);
  setShowLogin(false);
  setShowProfile(true);
};

  const handleSignOut = () => {
    clearUser();
    setCurrentUser(null);
    setShowProfile(false);
    setShowLogin(true);
  };

  return (
    <div>
      {/* Login form */}
      {showLogin && !currentUser && (
        <LoginForm onLogin={handleLoginSuccess}
        />
      )}

      {/* Profile modal */}
      {currentUser && showProfile && (
        <UserProfileModal
          user={currentUser}
          theme="light"
          onClose={() => setShowProfile(false)}
          onSignOut={handleSignOut}
        />
      )}

      {/* Optional button to view profile if logged in */}
      {currentUser && !showProfile && (
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          onClick={() => setShowProfile(true)}
        >
          View Profile
        </button>
      )}
    </div>
  );
}
