"use client";

import React from "react";

interface AddTaskButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export default function AddTaskButton({
  children,
  onClick,
  disabled = false,
  className = "",
}: AddTaskButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        px-5 py-2 
        bg-[#aa6c32] 
        text-white 
        text-lg 
        font-bold 
        rounded-2xl 
        shadow-md 
        hover:bg-[#b38b66] 
        active:translate-y-[3px] 
        active:shadow-inner 
        transition-all
        disabled:opacity-60 disabled:cursor-not-allowed
        ${className}
      `}
    >
      {children}
    </button>
  );
}
