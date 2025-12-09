"use client";

import React, { useMemo } from "react";
import { Task } from "@/types/Task";

interface DayViewProps {
  selectedDate: Date;
  tasks: Task[];
  onSelectTask: (task: Task) => void;
  typeColors: Record<string, string>;
}

type ExtendedEvent = Task & { start: Date; end: Date };

export default function DayView({
  selectedDate,
  tasks,
  onSelectTask,
  typeColors,
}: DayViewProps) {
  const hours = Array.from({ length: 24 }, (_, i) => i);

  /* -------- FILTER EVENTS OF THIS DAY -------- */
  const todaysEvents = useMemo(() => {
    const dayStart = new Date(selectedDate);
    dayStart.setHours(0, 0, 0, 0);

    const dayEnd = new Date(selectedDate);
    dayEnd.setHours(23, 59, 59, 999);

    return tasks.filter((t) => {
      const start = new Date(t.startDate);
      const end = new Date(t.endDate);
      return end >= dayStart && start <= dayEnd;
    });
  }, [tasks, selectedDate]);

  /* ===============================================
        BUILD PARALLEL TRACKS (GOOGLE CALENDAR STYLE)
     =============================================== */

  const arrangedEvents = useMemo(() => {
    const evs: ExtendedEvent[] = todaysEvents
      .map((ev) => ({
        ...ev,
        start: new Date(ev.startDate),
        end: new Date(ev.endDate),
      }))
      .sort((a, b) => a.start.getTime() - b.start.getTime());

    const tracks: ExtendedEvent[][] = [];

    evs.forEach((ev) => {
      let placed = false;

      for (const track of tracks) {
        const last = track[track.length - 1];
        if (last.end <= ev.start) {
          track.push(ev);
          placed = true;
          break;
        }
      }

      if (!placed) tracks.push([ev]);
    });

    return { evs, tracks };
  }, [todaysEvents]);

  return (
    <div className="day-view-container">
      <div className="day-header">
        {selectedDate.toLocaleString("default", { weekday: "long" })},{" "}
        {selectedDate.getDate()}{" "}
        {selectedDate.toLocaleString("default", { month: "short" })}
      </div>

      <div className="day-grid">
        <div className="day-hour-column">
          {hours.map((h) => (
            <div key={h} className="hour-cell">
              {h}:00
            </div>
          ))}
        </div>

        <div className="day-events-column">
          {hours.map((h) => (
            <div key={h} className="day-hour-cell"></div>
          ))}

          {arrangedEvents.evs.map((ev) => {
            const start = ev.start;
            const end = ev.end;

            const startHour =
              start.toDateString() === selectedDate.toDateString()
                ? start.getHours() + start.getMinutes() / 60
                : 0;

            const endHour =
              end.toDateString() === selectedDate.toDateString()
                ? end.getHours() + end.getMinutes() / 60
                : 24;

            const duration = Math.max(0.5, endHour - startHour);

            const trackIndex = arrangedEvents.tracks.findIndex((track) =>
              track.includes(ev)
            );

            const columnCount = arrangedEvents.tracks.length;
            const widthPercent = 100 / columnCount;

            return (
              <div
                key={ev.id}
                className="day-task"
                style={{
                  top: `${startHour * 32}px`,
                  height: `${duration * 32}px`,
                  left: `${trackIndex * widthPercent}%`,
                  width: `${widthPercent - 2}%`,
                  backgroundColor: typeColors[ev.type],
                }}
                onClick={() => onSelectTask(ev)}
              >
                <strong>{ev.title}</strong>
                <div className="small">
                  {start.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
