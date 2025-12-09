"use client";

import React, { useMemo } from "react";
import { Task } from "@/types/Task";

interface WeekViewProps {
  selectedDate: Date;
  tasks: Task[];
  onSelectTask: (task: Task) => void;
  typeColors: Record<string, string>;
}

type WeekEvent = Task & {
  start: Date;
  end: Date;
};

export default function WeekView({
  selectedDate,
  tasks,
  onSelectTask,
  typeColors,
}: WeekViewProps) {
  /* ---------------- WEEK START ---------------- */
  const weekStart = new Date(selectedDate);
  weekStart.setHours(0, 0, 0, 0);
  weekStart.setDate(selectedDate.getDate() - ((selectedDate.getDay() + 6) % 7));

  const weekDays = [...Array(7)].map((_, i) => {
    const d = new Date(weekStart);
    d.setDate(weekStart.getDate() + i);
    return d;
  });

  const hours = Array.from({ length: 24 }, (_, i) => i);

  /* ---------------- PREP EVENTS ---------------- */
  const weeklyEvents: WeekEvent[] = useMemo(() => {
    return tasks
      .map((t) => ({
        ...t,
        start: new Date(t.startDate),
        end: new Date(t.endDate),
      }))
      .filter((ev) => ev.end >= weekStart);
  }, [tasks, selectedDate]);

  /* ---------------- TRACKS (parallel columns) ---------------- */
  const arranged = useMemo(() => {
    const sorted = [...weeklyEvents].sort(
      (a, b) => a.start.getTime() - b.start.getTime()
    );

    const tracks: WeekEvent[][] = [];

    sorted.forEach((ev) => {
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

    return { events: sorted, tracks };
  }, [weeklyEvents]);

  /* ---------------- ALL DAY EVENTS ---------------- */
  const isAllDay = (ev: WeekEvent) => {
    return (
      ev.start.getHours() === 0 &&
      ev.start.getMinutes() === 0 &&
      ev.end.getHours() === 23 &&
      ev.end.getMinutes() === 59
    );
  };

  const allDayEvents = arranged.events.filter(isAllDay);
  const hourlyEvents = arranged.events.filter((ev) => !isAllDay(ev));

  /* =========================================================
       RENDER
  ========================================================== */
  return (
    <div className="week-view-container">
      {/* ---------------- HEADER ---------------- */}
      <div className="week-header">
        <div className="hour-col-header">All-Day</div>
        {weekDays.map((day, i) => (
          <div key={i} className="week-day-header">
            {day.toLocaleString("default", { weekday: "short" })}{" "}
            {day.getDate()}
          </div>
        ))}
      </div>

      {/* ---------------- ALL-DAY ROW ---------------- */}
      <div className="week-all-day-row">
        <div></div>

        {weekDays.map((day, ci) => {
          const dayStart = new Date(day);
          dayStart.setHours(0, 0, 0, 0);

          return (
            <div key={ci} className="week-all-day-cell">
              {allDayEvents.map((ev) => {
                const s = new Date(ev.start);
                s.setHours(0, 0, 0, 0);

                const e = new Date(ev.end);
                e.setHours(0, 0, 0, 0);

                if (dayStart < s || dayStart > e) return null;

                const weekday = (day.getDay() + 6) % 7;
                const isStartOfWeek = weekday === 0;
                const isEventStart = dayStart.getTime() === s.getTime();

                if (!isStartOfWeek && !isEventStart) return null;

                const daysLeftInWeek = 7 - weekday;
                const daysLeftInEvent =
                  Math.floor((e.getTime() - dayStart.getTime()) / 86400000) + 1;

                const span = Math.min(daysLeftInWeek, daysLeftInEvent);

                return (
                  <div
                    key={ev.id}
                    className="week-all-day-bar"
                    style={{
                      backgroundColor: typeColors[ev.type],
                      width: `calc(${span * 100}% - 6px)`,
                    }}
                    onClick={() => onSelectTask(ev)}
                  >
                    {ev.title}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>

      {/* ---------------- HOURLY GRID ---------------- */}
      <div className="week-grid">
        {/* HOURS COLUMN */}
        <div className="hour-column">
          {hours.map((h) => (
            <div key={h} className="hour-cell">
              {h}:00
            </div>
          ))}
        </div>

        {/* 7 COLUMNS */}
        {weekDays.map((day, colIndex) => {
          const dayStart = new Date(day);
          dayStart.setHours(0, 0, 0, 0);

          const dayEnd = new Date(day);
          dayEnd.setHours(23, 59, 59, 999);

          /* events inside this day */
          const todays = hourlyEvents.filter(
            (ev) => ev.end >= dayStart && ev.start <= dayEnd
          );

          return (
            <div key={colIndex} className="week-day-column">
              {hours.map((h) => (
                <div key={h} className="week-hour-cell"></div>
              ))}

              {todays.map((ev) => {
                /* ---- IDENTICAL TO DayView ---- */

                const startHour =
                  ev.start.toDateString() === day.toDateString()
                    ? ev.start.getHours() + ev.start.getMinutes() / 60
                    : 0;

                const endHour =
                  ev.end.toDateString() === day.toDateString()
                    ? ev.end.getHours() + ev.end.getMinutes() / 60
                    : 24;

                const duration = Math.max(0.3, endHour - startHour);

                const trackIndex = arranged.tracks.findIndex((t) =>
                  t.includes(ev)
                );
                const trackCount = arranged.tracks.length;
                const widthPercent = 100 / trackCount;

                return (
                  <div
                    key={ev.id + ":" + colIndex}
                    className="week-task"
                    style={{
                      top: `${startHour * 32}px`,       // EXACT CA DAY VIEW
                      height: `${duration * 32}px`,     // EXACT CA DAY VIEW
                      left: `${trackIndex * widthPercent}%`,
                      width: `${widthPercent - 2}%`,
                      backgroundColor: typeColors[ev.type],
                    }}
                    onClick={() => onSelectTask(ev)}
                  >
                    <strong>{ev.title}</strong>
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
