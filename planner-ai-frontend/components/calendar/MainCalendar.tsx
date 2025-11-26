"use client";

import React, { useState, useMemo } from "react";
import Sidebar from "@/components/sidebar/Sidebar";

import AddTaskModal from "@/components/modals/AddTaskModal";
import TaskDetailsModal from "@/components/modals/TaskDetailsModal";

import WeekView from "@/components/calendar/WeekView";
import DayView from "@/components/calendar/DayView";

import { getMonthMatrix, isSameDay } from "@/utils/dateUtils";
import { Task } from "@/types/Task";

import "@/styles/calendar.css";

export default function MainCalendar() {
  const today = new Date();

  /* ---------------- STATE ---------------- */
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date>(today);
  const [currentMonth, setCurrentMonth] = useState<Date>(today);

  const [showAddModal, setShowAddModal] = useState(false);
  const [editTask, setEditTask] = useState<Task | null>(null);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  const [viewMode, setViewMode] = useState<"month" | "week" | "day">("month");

  const monthMatrix = useMemo(
    () => getMonthMatrix(currentMonth),
    [currentMonth]
  );

  /* ---------------- COLORS ---------------- */
  const typeColors = {
    Assignment: "#F4C2C2",
    Project: "#F3E5AB",
    "Written Exam": "#bde0fe",
    "Practical Exam": "#c8f7c5",
  };

  /* ---------------- MONTH EVENT MAP ---------------- */
  const monthEvents = useMemo(() => {
    const map = new Map<string, Task[]>();

    for (const t of tasks) {
      let d = new Date(t.startDate);
      const end = new Date(t.endDate);

      while (d <= end) {
        const key = `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
        if (!map.has(key)) map.set(key, []);
        map.get(key)!.push(t);
        d = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1);
      }
    }

    return map;
  }, [tasks]);

  /* ---------------- NAVIGATION ---------------- */
  const next = () => {
    if (viewMode === "month") {
      setCurrentMonth(
        new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 1)
      );
    } else if (viewMode === "week") {
      const d = new Date(selectedDate);
      d.setDate(d.getDate() + 7);
      setSelectedDate(d);
    } else {
      const d = new Date(selectedDate);
      d.setDate(d.getDate() + 1);
      setSelectedDate(d);
    }
  };

  const prev = () => {
    if (viewMode === "month") {
      setCurrentMonth(
        new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, 1)
      );
    } else if (viewMode === "week") {
      const d = new Date(selectedDate);
      d.setDate(d.getDate() - 7);
      setSelectedDate(d);
    } else {
      const d = new Date(selectedDate);
      d.setDate(d.getDate() - 1);
      setSelectedDate(d);
    }
  };

  const goToToday = () => {
    setSelectedDate(today);
    setCurrentMonth(new Date(today.getFullYear(), today.getMonth(), 1));
  };

  /* ---------------- SAVE TASK ---------------- */
  function handleSaveTask(task: Task) {
    setTasks((prev) => {
      const idx = prev.findIndex((t) => t.id === task.id);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = task;
        return copy;
      }
      return [...prev, task];
    });

    setEditTask(null);
    setShowAddModal(false);
  }

  /* ---------------- DELETE TASK ---------------- */
  function handleDelete(id: number) {
    setTasks((prev) => prev.filter((t) => t.id !== id));
    setSelectedTask(null);
  }

  const monthLabel = currentMonth.toLocaleString("default", {
    month: "long",
    year: "numeric",
  });

  /* =====================================================
     MAIN RENDER
  ===================================================== */
  return (
    <div className="flex h-screen overflow-hidden">

      {/* SIDEBAR */}
      <Sidebar
        currentMonth={currentMonth}
        selectedDate={selectedDate}
        onSelectDate={(d) => {
          setSelectedDate(d);
          setCurrentMonth(new Date(d.getFullYear(), d.getMonth(), 1));
        }}
      />

      {/* MAIN */}
      <main className="flex-1 px-10 py-6 bg-gradient-to-b from-[#ffe5e5] to-[#fff0d6] overflow-hidden">

        {/* HEADER */}
        <div className="flex items-start justify-between mb-6 header-controls">
          <div>
            <h1 className="text-4xl font-bold text-[#5d2a02]">{monthLabel}</h1>

            <button
              onClick={() => {
                setShowAddModal(true);
                setEditTask(null);
              }}
              className="add-task-btn"
            >
              + Add Task
            </button>
          </div>

          {/* NAV */}
          <div className="flex flex-col gap-3 items-end">
            <div className="flex gap-2 main-header-buttons">
              <button className="nav-button" onClick={prev}>‹</button>
              <button className="nav-button" onClick={goToToday}>Today</button>
              <button className="nav-button" onClick={next}>›</button>
            </div>

            <div className="flex gap-2 main-header-buttons">
              <button
                className={`nav-button ${viewMode === "month" ? "active-view" : ""}`}
                onClick={() => setViewMode("month")}
              >
                Month
              </button>

              <button
                className={`nav-button ${viewMode === "week" ? "active-view" : ""}`}
                onClick={() => setViewMode("week")}
              >
                Week
              </button>

              <button
                className={`nav-button ${viewMode === "day" ? "active-view" : ""}`}
                onClick={() => setViewMode("day")}
              >
                Day
              </button>
            </div>
          </div>
        </div>

        {/* ======================= MONTH VIEW ======================= */}
        {viewMode === "month" && (
          <div className="calendar-container">

            {/* WEEKDAY HEADERS */}
            <div className="calendar-weekdays">
              {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((d) => (
                <div key={d}>{d}</div>
              ))}
            </div>

            {/* GRID */}
            <div className="calendar-grid-days">
              {monthMatrix.map((week, wi) =>
                week.map((day, di) => {
                  const key = `${day.getFullYear()}-${day.getMonth()}-${day.getDate()}`;
                  const events = monthEvents.get(key) ?? [];

                  const inMonth = day.getMonth() === currentMonth.getMonth();
                  const selected = isSameDay(day, selectedDate);

                  return (
                    <div
                      key={`${wi}-${di}`}
                      className={`calendar-day-cell ${
                        inMonth ? "in-month" : "out-month"
                      } ${selected ? "selected" : ""}`}
                      onClick={() => setSelectedDate(day)}
                    >
                      <div className="day-number">{day.getDate()}</div>

                      {/* ================== FIXED MULTI-LANE MONTH BARS ================== */}
                      <div className="event-lane-container">
                        {(() => {
                          /** 1️⃣ Build LANE structure for THIS DAY */
                          const lanes: Task[][] = [];

                          for (const ev of events) {
                            const start = new Date(ev.startDate);
                            const end = new Date(ev.endDate);

                            start.setHours(0, 0, 0, 0);
                            end.setHours(0, 0, 0, 0);

                            const dayStart = new Date(day);
                            dayStart.setHours(0, 0, 0, 0);

                            if (dayStart < start || dayStart > end) continue;

                            let placed = false;

                            for (const lane of lanes) {
                              const last = lane[lane.length - 1];
                              if (!last) continue;

                              const lastStart = new Date(last.startDate);
                              const lastEnd = new Date(last.endDate);

                              lastStart.setHours(0, 0, 0, 0);
                              lastEnd.setHours(0, 0, 0, 0);

                              const overlaps =
                                !(dayStart > lastEnd || dayStart < lastStart);

                              if (overlaps) continue;

                              lane.push(ev);
                              placed = true;
                              break;
                            }

                            if (!placed) lanes.push([ev]);
                          }

                          /** 2️⃣ Render lanes */
                          return lanes.map((lane, laneIdx) =>
                            lane.map((ev) => {
                              const start = new Date(ev.startDate);
                              const end = new Date(ev.endDate);

                              start.setHours(0, 0, 0, 0);
                              end.setHours(0, 0, 0, 0);

                              const dayStart = new Date(day);
                              dayStart.setHours(0, 0, 0, 0);

                              const weekday = (day.getDay() + 6) % 7;
                              const isWeekStart = weekday === 0;
                              const isEventStart =
                                start.getTime() === dayStart.getTime();

                              if (!isWeekStart && !isEventStart) return null;

                              const daysLeftInWeek = 7 - weekday;
                              const daysLeftInEvent =
                                Math.floor(
                                  (end.getTime() - dayStart.getTime()) /
                                    86400000
                                ) + 1;

                              const span = Math.min(
                                daysLeftInWeek,
                                daysLeftInEvent
                              );

                              return (
                                <div
                                  key={ev.id + "-lane-" + laneIdx}
                                  className="event-bar-multi"
                                  style={{
                                    top: `${laneIdx * 22}px`,
                                    width: `calc(${span * 100}% + ${
                                      (span - 1) * 6
                                    }px)`,
                                    backgroundColor: typeColors[ev.type],
                                  }}
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setSelectedTask(ev);
                                  }}
                                >
                                  {ev.title}
                                </div>
                              );
                            })
                          );
                        })()}
                      </div>
                      {/* ================== END FIX ================== */}

                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {/* ======================== WEEK VIEW ======================== */}
        {viewMode === "week" && (
          <WeekView
            selectedDate={selectedDate}
            tasks={tasks}
            onSelectTask={setSelectedTask}
            typeColors={typeColors}
          />
        )}

        {/* ========================= DAY VIEW ========================= */}
        {viewMode === "day" && (
          <DayView
            selectedDate={selectedDate}
            tasks={tasks}
            onSelectTask={setSelectedTask}
            typeColors={typeColors}
          />
        )}
      </main>

      {/* MODALS */}
      {showAddModal && (
        <AddTaskModal
          existingTask={editTask}
          onClose={() => setShowAddModal(false)}
          onSave={handleSaveTask}
        />
      )}

      {selectedTask && (
        <TaskDetailsModal
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onEdit={(task) => {
            setEditTask(task);
            setShowAddModal(true);
          }}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}
