"use client";

export interface ArrowCalendarButtonProps {
  direction: "left" | "right";
  onClick: () => void;
}

export default function ArrowCalendarButton({ direction, onClick }: ArrowCalendarButtonProps) {
  return (
    <button
      onClick={onClick}
      className="
        w-9 h-9
        rounded-full
        bg-gradient-to-b from-[#fff3dd] to-[#ffe7c2]
        border border-[#d6b48c]
        shadow-sm
        text-[#5a3b17]
        hover:shadow-md
        hover:-translate-y-[1px]
        transition-all duration-150
        flex items-center justify-center
        font-bold
      "
    >
      {direction === "left" ? "‹" : "›"}
    </button>
  );
}
