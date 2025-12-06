"use client";

import React, { useState } from "react";
import "@/styles/feedback.css";

interface Props {
  onClose: () => void;
  onSubmit: (rating: number, message: string) => void;
}

export default function FeedbackModal({ onClose, onSubmit }: Props) {
  const [rating, setRating] = useState(0);
  const [hovered, setHovered] = useState(0);
  const [message, setMessage] = useState("");

  function handleSend() {
    if (rating === 0) {
      alert("Please choose a rating");
      return;
    }
    onSubmit(rating, message);
  }

  return (
    <div className="feedback-backdrop" onClick={onClose}>
      <div className="feedback-card" onClick={(e) => e.stopPropagation()}>
        
        {/* CLOSE BUTTON */}
        <button className="feedback-card-close" onClick={onClose}>✕</button>

        {/* ICON */}
        <div className="feedback-icon">
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="90"
    height="90"
    viewBox="0 0 64 64"
  >
    <rect x="6" y="10" width="52" height="46" rx="8" fill="#d3d3d3" />
    <rect x="6" y="8" width="52" height="46" rx="8" fill="#f4f4f4" />
    <rect x="6" y="8" width="52" height="14" fill="#e65145" />
    <rect x="16" y="2" width="8" height="20" rx="4" fill="#c6c6c6" />
    <rect x="40" y="2" width="8" height="20" rx="4" fill="#c6c6c6" />
    <rect x="16" y="4" width="8" height="12" rx="4" fill="#787878" />
    <rect x="40" y="4" width="8" height="12" rx="4" fill="#787878" />
    <g fill="#c1c1c1">
      <rect x="14" y="26" width="8" height="8" rx="2" />
      <rect x="24" y="26" width="8" height="8" rx="2" />
      <rect x="34" y="26" width="8" height="8" rx="2" />
      <rect x="44" y="26" width="8" height="8" rx="2" />
      <rect x="14" y="36" width="8" height="8" rx="2" />
      <rect x="24" y="36" width="8" height="8" rx="2" />
      <rect x="34" y="36" width="8" height="8" rx="2" />
      <rect x="44" y="36" width="8" height="8" rx="2" />
      <rect x="14" y="46" width="8" height="8" rx="2" />
      <rect x="24" y="46" width="8" height="8" rx="2" />
      <rect x="34" y="46" width="8" height="8" rx="2" />
      <rect x="44" y="46" width="8" height="8" rx="2" />
    </g>
  </svg>
</div>


        {/* TITLE */}
        <h2 className="feedback-card-title">Submit Your Feedback</h2>

        {/* STARS */}
        <div className="feedback-stars-group">
          {[1, 2, 3, 4, 5].map((star) => (
            <span
              key={star}
              className={`feedback-star-card ${
                star <= (hovered || rating) ? "active" : ""
              }`}
              onMouseEnter={() => setHovered(star)}
              onMouseLeave={() => setHovered(0)}
              onClick={() => setRating(star)}
            >
              ★
            </span>
          ))}
        </div>

        {/* TEXTAREA */}
        <textarea
          className="feedback-card-textarea"
          placeholder="Your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        {/* SEND BUTTON */}
        <button className="feedback-card-send" onClick={handleSend}>
            ♻️ Regenerate Plan          </button>
      </div>
    </div>
  );
}
