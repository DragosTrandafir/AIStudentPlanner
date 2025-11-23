"use client";

import React, { useMemo } from "react";
import { Task } from "@/types/Task";

interface WeekViewProps {
  selectedDate: Date;
  tasks: Task[];
  onSelectTask: (task: Task) => void;
}

export default function WeekView({ selectedDate, tasks, onSelectTask }: WeekViewProps) {
  const weekStart = new Date(selectedDate);
  weekStart.setDate(selectedDate.getDate() - ((selectedDate.getDay() + 6) % 7));

  const weekDays = [...Array(7)].map((_, i) => {
    const d = new Date(weekStart);
    d.setDate(weekStart.getDate() + i);
    return d;
  });

  const hours = [...Array(24)].map((_, i) => i);

  const tasksByDay = useMemo(() => {
    const map = new Map<string, Task[]>();

    for (const t of tasks) {
      const d = new Date(t.startDate);
      const key = `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;

      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(t);
    }

    return map;
  }, [tasks]);

  return (
    <div className="week-view-container">
      <div className="week-header">
        <div className="hour-col-header"></div>
        {weekDays.map((day, idx) => (
          <div key={idx} className="week-day-header">
            {day.toLocaleString("default", { weekday: "short" })} {day.getDate()}
          </div>
        ))}
      </div>

      <div className="week-grid">
        <div className="hour-column">
          {hours.map((h) => (
            <div key={h} className="hour-cell">{h}:00</div>
          ))}
        </div>

        {weekDays.map((day, index) => {
          const key = `${day.getFullYear()}-${day.getMonth()}-${day.getDate()}`;
          const events = tasksByDay.get(key) ?? [];

          return (
            <div key={index} className="week-day-column">
              {hours.map((h) => (
                <div key={h} className="week-hour-cell"></div>
              ))}

              {events.map((ev) => {
                const start = new Date(ev.startDate);
                const hour = start.getHours();

                return (
                  <div
                    key={ev.id}
                    className="week-task"
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
          );
        })}
      </div>
    </div>
  );
}
