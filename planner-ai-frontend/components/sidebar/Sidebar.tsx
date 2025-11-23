"use client";

import MiniMonthView from "@/components/calendar/MiniMonthView";
import "@/styles/sidebar.css";

interface SidebarProps {
  currentMonth: Date;
  onSelect: (date: Date) => void;
}

export default function Sidebar({ currentMonth, onSelect }: SidebarProps) {
  return (
    <div className="sidebar">
      {/* === Task Legend === */}
      <div className="legend">
        <h2 className="legend-title">Task Legend</h2>

        <div className="legend-list">

          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: "#F4C2C2" }}></span>
            <span>Assignment</span>
          </div>

          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: "#F3E5AB" }}></span>
            <span>Project</span>
          </div>

          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: "#bde0fe" }}></span>
            <span>Written Exam</span>
          </div>

          <div className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: "#c8f7c5" }}></span>
            <span>Practical Exam</span>
          </div>

        </div>
      </div>

      {/* === Bottom Mini Calendar === */}
      <div className="sidebar-mini">
        <MiniMonthView selectedMonth={currentMonth} onSelect={onSelect} />
      </div>
    </div>
  );
}
