"use client";

import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";

type Props = {
  onRegisterSuccess: () => void;
  onGoToLogin: () => void;
};

export default function RegisterForm({
  onRegisterSuccess,
  onGoToLogin,
}: Props) {
  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
  e.preventDefault();

  if (!fullName || !username || !email || !password || !confirm) {
    setError("Please fill in all fields.");
    return;
  }

  if (password !== confirm) {
    setError("Passwords do not match.");
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: fullName,
        username: username,
        email: email,
        password: password,
      }),
    });

    if (!res.ok) {
      const data = await res.json();
      setError(data.detail || "Registration failed");
      return;
    }

    onRegisterSuccess();
  } catch (err) {
    setError("Server unreachable");
  }
}

  return (
    <div className="login-right">
      <h2>Register</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
        />

        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>

        <div className="password-wrapper">
          <input
            type={showConfirm ? "text" : "password"}
            placeholder="Confirm Password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />
          <button
            type="button"
            className="password-toggle"
            onClick={() => setShowConfirm(!showConfirm)}
          >
            {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>

        {error && <p className="form-error">{error}</p>}

        <button type="submit">Register</button>
      </form>

      <p className="auth-switch">
        Already have an account?{" "}
        <span onClick={onGoToLogin}>Log in</span>
      </p>
    </div>
  );
}
