"use client";

import { useState, FormEvent } from "react";
import { Eye, EyeOff } from "lucide-react";
// 1. Add this import!
import { saveUser } from "@/utils/userStorage";

type Props = {
  onLogin: (userData: any) => void;
};

export default function LoginForm({ onLogin }: Props) {
  const [usernameOrEmail, setUsernameOrEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!usernameOrEmail.trim() || !password.trim()) {
      setError("Please fill in all fields.");
      return;
    }

    setError("");

    try {
      const response = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username_or_email: usernameOrEmail.trim(),
          password: password,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || "Login failed");
        return;
      }

      const userData = await response.json();

      localStorage.setItem("authToken", userData.access_token);

      const backendUser = userData.user;

      const formattedUser = {
        id: backendUser.id,
        fullName: backendUser.name ||  "No Name",
        username: backendUser.username,
        email: backendUser.email
      };

      saveUser(formattedUser);

      // Now we can tell the parent component to redirect
      onLogin(formattedUser);

    } catch (err) {
      console.error(err);
      setError("Server unreachable");
    }
  };

  return (
    <div className="login-right">
      <h2>Sign In</h2>
      {/* ... rest of your JSX remains exactly the same ... */}
       <form onSubmit={handleSubmit} className="login-form">
        <input
          type="text"
          placeholder="Username or email"
          value={usernameOrEmail}
          onChange={(e) => setUsernameOrEmail(e.target.value)}
        />

        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="button"
            className="password-toggle"
            onClick={() => setShowPassword((prev) => !prev)}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>

        {error && <p className="form-error">{error}</p>}

        <button type="submit" className="login-btn">
          Login
        </button>
      </form>
    </div>
  );
}