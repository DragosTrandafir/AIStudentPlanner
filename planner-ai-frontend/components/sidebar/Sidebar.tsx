"use client";

import MiniMonthView from "@/components/calendar/MiniMonthView";

interface SidebarProps {
  currentMonth: Date;
  selectedDate: Date | null;
  onSelectDate: (date: Date) => void;
}

export default function Sidebar({
  currentMonth,
  selectedDate,
  onSelectDate,
}: SidebarProps) {
  return (
    <div
      className="w-64 bg-[#f6ecd9] h-full p-6 flex flex-col justify-between"
      style={{ borderRight: "1px solid #e0d4c2" }}
    >
      {/* TASK LEGEND */}
      <div>
        <h2 className="text-2xl font-bold mb-6 text-[#5a3e2b]">Task Legend</h2>

        <div className="flex flex-col gap-4 text-[#5a3e2b]">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#F4C2C2" }}></span>
            Assignment
          </div>

          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#F3E5AB" }}></span>
            Project
          </div>

          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#bde0fe" }}></span>
            Written Exam
          </div>

          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#c8f7c5" }}></span>
            Practical Exam
          </div>
        </div>
      </div>

      {/* MINI CALENDAR */}
      <MiniMonthView
        selectedMonth={currentMonth}
        selectedDate={selectedDate}
        onSelect={(date) => onSelectDate(date)}  // ✔ numele corect
      />
    </div>
  );
}
