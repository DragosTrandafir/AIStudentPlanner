"use client";

import React, { useMemo } from "react";
import { Task } from "@/types/Task";

interface DayViewProps {
  selectedDate: Date;
  tasks: Task[];
  onSelectTask: (task: Task) => void;
}

export default function DayView({ selectedDate, tasks, onSelectTask }: DayViewProps) {
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const todaysTasks = useMemo(() => {
    return tasks.filter((t) => {
      const d = new Date(t.startDate);

      return (
        d.getFullYear() === selectedDate.getFullYear() &&
        d.getMonth() === selectedDate.getMonth() &&
        d.getDate() === selectedDate.getDate()
      );
    });
  }, [tasks, selectedDate]);

  return (
    <div className="day-view-container">

      {/* Day header */}
      <div className="day-header">
        {selectedDate.toLocaleString("default", { weekday: "long" })},{" "}
        {selectedDate.getDate()}{" "}
        {selectedDate.toLocaleString("default", { month: "short" })}
      </div>

      {/* Grid */}
      <div className="day-grid">
        
        {/* Hour labels */}
        <div className="day-hour-column">
          {hours.map((h) => (
            <div key={h} className="hour-cell">{h}:00</div>
          ))}
        </div>

        {/* Event area */}
        <div className="day-events-column">
          {hours.map((h) => (
            <div key={h} className="day-hour-cell"></div>
          ))}

          {todaysTasks.map((ev) => {
            const start = new Date(ev.startDate);
            const hour = start.getHours();

            return (
              <div
                key={ev.id}
                className="day-task"
                style={{ top: `${hour * 60}px`, backgroundColor: ev.color }}
                onClick={() => onSelectTask(ev)}
              >
                <strong>{ev.title}</strong>
                <div className="small">
                  {start.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </div>
              </div>
            );
          })}

        </div>
      </div>
    </div>
  );
}
