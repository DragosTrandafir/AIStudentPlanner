import React from "react";

interface Props {
  currentMonth: string;
  onPrev: () => void;
  onNext: () => void;
  onToday: () => void;
  onAddTask: () => void;
  view: "month" | "week" | "day";
  setView: (v: "month" | "week" | "day") => void;
}

export default function CalendarHeader({
  currentMonth,
  onPrev,
  onNext,
  onToday,
  onAddTask,
  view,
  setView,
}: Props) {
  return (
    <div className="flex items-center justify-between mb-6 header-controls">

      {/* LEFT — MONTH LABEL */}
      <h1 className="text-4xl font-bold month-title">
        {currentMonth}
      </h1>

      <div className="header-right">
      {/* CENTER — TOOLBAR */}
      <div className="toolbar">

        {/* GROUP 1 : ← Today → */}
        <div className="nav-group">
          <button className="nav-segment" onClick={onPrev}>←</button>
          <button className="nav-segment" onClick={onToday}>Today</button>
          <button className="nav-segment" onClick={onNext}>→</button>
        </div>

        {/* GROUP 2 : Month / Week / Day */}
        <div className="view-group">
          <button
            className={`nav-button ${view === "month" ? "active-view" : ""}`}
            onClick={() => setView("month")}
          >
            Month
          </button>

          <button
            className={`nav-button ${view === "week" ? "active-view" : ""}`}
            onClick={() => setView("week")}
          >
            Week
          </button>

          <button
            className={`nav-button ${view === "day" ? "active-view" : ""}`}
            onClick={() => setView("day")}
          >
            Day
          </button>
        </div>

      </div>

      {/* RIGHT — ADD TASK */}
      <button className="add-task-btn" onClick={onAddTask}>
        + Add Task
      </button>
      </div>
    </div>
  );
}
