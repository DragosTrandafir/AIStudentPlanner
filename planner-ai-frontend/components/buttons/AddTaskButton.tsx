"use client";

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
        px-4 py-2
        bg-[#1D2939]
        text-white
        rounded-md
        font-medium
        hover:bg-[#111827]
        active:scale-[0.97]
        transition
        disabled:opacity-40 disabled:cursor-not-allowed
        ${className}
      `}
    >
      {children}
    </button>
  );
}
