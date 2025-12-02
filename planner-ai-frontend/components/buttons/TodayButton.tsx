"use client";

interface TodayButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  className?: string;
}

export default function TodayButton({
  onClick,
  children,
  className = "",
}: TodayButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`
        px-4 py-1.5
        rounded-full
        bg-gradient-to-b from-[#fff3dd] to-[#ffe7c2]
        border border-[#d6b48c]
        text-[#5a3b17]
        shadow-sm
        hover:shadow-md
        hover:-translate-y-[1px]
        transition-all duration-150
        ${className}
      `}
    >
      {children}
    </button>
  );
}
