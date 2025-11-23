"use client";

import React, { useState, useMemo } from "react";
import Sidebar from "@/components/sidebar/Sidebar";
import AddTaskModal from "@/components/modals/AddTaskModal";
import TaskDetailsModal from "@/components/modals/TaskDetailsModal";
import CalendarLegend from "./CalendarLegend";
import { getMonthMatrix } from "@/utils/dateUtils";

/* -------------------------
   Task types
   ------------------------- */
export type TaskStatus = "Pending" | "In Progress" | "Completed";
export type TaskType = "Assignment" | "Project" | "Practical Exam" | "Written Exam";

export interface Task {
  id: number;
  title: string;
  subject?: string;
  type: TaskType;
  difficulty?: number;
  description?: string;
  status?: TaskStatus;
  startDate: Date;
  endDate: Date;
  color?: string;
}

/* -----------------------------------
   SAFETY: convert to real Date objects
   ----------------------------------- */
function normalizeTaskDates(t: Task): Task {
  return {
    ...t,
    startDate: new Date(t.startDate),
    endDate: new Date(t.endDate),
  };
}

/* -------------------------
   Component
   ------------------------- */
export default function MainCalendar() {
  const today = new Date();

  const [tasks, setTasks] = useState<Task[]>(() => [
    {
      id: Date.now(),
      title: "Math Assignment",
      subject: "Algebra",
      type: "Assignment",
      difficulty: 2,
      description: "Complete exercises 1–10",
      status: "Pending",
      startDate: new Date(),
      endDate: new Date(),
      color: "#F4C2C2",
    },
  ]);

  const [currentMonth, setCurrentMonth] = useState<Date>(today);
  const [activeView, setActiveView] = useState<"month" | "week" | "day">("month");

  const [showAddModal, setShowAddModal] = useState(false);
  const [editTask, setEditTask] = useState<Task | null>(null);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  /* -------------------------
     Calendar matrix (month)
     ------------------------- */
  const monthMatrix: Date[][] = useMemo(
    () => getMonthMatrix(currentMonth),
    [currentMonth]
  );

  /* -------------------------
     Month navigation
     ------------------------- */
  const nextMonth = () =>
    setCurrentMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));

  const prevMonth = () =>
    setCurrentMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));

  const goToToday = () => setCurrentMonth(new Date());

  /* -------------------------
     Save or update a task
     ------------------------- */
  function handleSaveTask(task: Task) {
    const normalized = normalizeTaskDates(task);

    setTasks((prev) => {
      const idx = prev.findIndex((t) => t.id === normalized.id);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = normalized;
        return copy;
      }
      return [...prev, normalized];
    });

    setShowAddModal(false);
    setEditTask(null);
  }

  /* -------------------------
     Delete task
     ------------------------- */
  function handleDeleteTask(id: number) {
    setTasks((prev) => prev.filter((t) => t.id !== id));
    setSelectedTask(null);
  }

  /* -------------------------
     Tasks grouped per day
     ------------------------- */
  const eventsByDay = useMemo(() => {
    const map = new Map<string, Task[]>();

    for (const task of tasks) {
      const t = normalizeTaskDates(task);

      const d = t.startDate;
      const key = `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;

      const arr = map.get(key) ?? [];
      arr.push(t);
      map.set(key, arr);
    }

    return map;
  }, [tasks]);

  const monthLabel = currentMonth.toLocaleString("default", {
    month: "long",
    year: "numeric",
  });

  /* -------------------------
     VIEW SWITCH (month/week/day)
     ------------------------- */
  function renderCalendarView() {
    if (activeView === "week") {
      return (
        <div
          style={{
            background: "#fff7f2",
            borderRadius: 12,
            padding: 20,
            textAlign: "center",
            border: "2px dashed #d8a27d",
            marginTop: 40,
          }}
        >
          Week View Coming Next (UI included from your screenshot)
        </div>
      );
    }

    if (activeView === "day") {
      return (
        <div
          style={{
            background: "#fff7f2",
            borderRadius: 12,
            padding: 20,
            textAlign: "center",
            border: "2px dashed #d8a27d",
            marginTop: 40,
          }}
        >
          Day View Coming Next (hourly vertical view)
        </div>
      );
    }

    /* MONTH VIEW (default) */
    return (
      <div className="calendar-grid">
        {/* Weekdays */}
        <div className="calendar-weekdays">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
            <div
              key={d}
              className="weekday"
              style={{
                textAlign: "center",
                fontWeight: 700,
                color: "#8a2e00",
              }}
            >
              {d}
            </div>
          ))}
        </div>

        {/* Month grid */}
        <div className="calendar-days">
          {monthMatrix.map((week, wi) => (
            <div key={wi} className="calendar-week">
              {week.map((day, di) => {
                const isCurrent = day.getMonth() === currentMonth.getMonth();
                const key = `${day.getFullYear()}-${day.getMonth()}-${day.getDate()}`;
                const events = eventsByDay.get(key) ?? [];

                return (
                  <div
                    key={di}
                    className={`calendar-day ${isCurrent ? "current-month" : "other-month"}`}
                  >
                    <span className="day-number">{day.getDate()}</span>

                    <div style={{ marginTop: 28 }}>
                      {events.map((ev) => (
                        <div
                          key={ev.id}
                          className="event-pill"
                          style={{ backgroundColor: ev.color }}
                          onClick={() => setSelectedTask(ev)}
                        >
                          <div style={{ fontWeight: 600 }}>{ev.title}</div>
                          {ev.description && (
                            <div style={{ fontSize: 12 }}>{ev.description}</div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    );
  }

  /* ------------------------- */

  return (
    <div className="flex min-h-screen">
      {/* =============== Sidebar =============== */}
      <Sidebar
        currentMonth={currentMonth}
        onSelect={(date: Date) => setCurrentMonth(date)}
      />

      {/* =============== Main Content =============== */}
      <main
        className="flex-1 p-6"
        style={{
          background: "linear-gradient(180deg,#ffe5e5 0%,#fff0d6 100%)",
        }}
      >
        {/* -------- Header -------- */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 style={{ fontSize: 40, color: "#5d2a02", fontWeight: 700 }}>
              {monthLabel}
            </h1>

            <button
              onClick={() => {
                setEditTask(null);
                setShowAddModal(true);
              }}
              style={{
                marginTop: 12,
                padding: "10px 18px",
                background: "#aa6c32",
                color: "#fff",
                borderRadius: 18,
                border: "none",
                fontWeight: 700,
                cursor: "pointer",
              }}
            >
              + Add Task
            </button>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {/* Navigation */}
            <div style={{ display: "flex", gap: 8 }}>
              <button className="nav-button" onClick={prevMonth}>‹</button>
              <button className="nav-button" onClick={goToToday}>Today</button>
              <button className="nav-button" onClick={nextMonth}>›</button>
            </div>

            {/* View switch */}
            <div style={{ display: "flex", gap: 8 }}>
              <button
                className="nav-button"
                onClick={() => setActiveView("month")}
              >
                Month
              </button>
              <button
                className="nav-button"
                onClick={() => setActiveView("week")}
              >
                Week
              </button>
              <button
                className="nav-button"
                onClick={() => setActiveView("day")}
              >
                Day
              </button>
            </div>
          </div>
        </div>

        {/* -------- MAIN CALENDAR VIEW -------- */}
        {renderCalendarView()}

        {/* Legend */}
        <div style={{ marginTop: 18 }}>
          <CalendarLegend />
        </div>
      </main>

      {/* ========== Add Task Modal ========== */}
      {showAddModal && (
        <AddTaskModal
          existingTask={editTask}
          onClose={() => {
            setShowAddModal(false);
            setEditTask(null);
          }}
          onSave={(t) =>
            handleSaveTask({
              ...t,
              id: typeof t.id === "number" ? t.id : Number(t.id) || Date.now(),
              startDate: new Date(t.startDate),
              endDate: new Date(t.endDate),
            })
          }
        />
      )}

      {/* ========== Task Details Modal ========== */}
      {selectedTask && (
        <TaskDetailsModal
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onEdit={(task) => {
            setEditTask(normalizeTaskDates(task));
            setShowAddModal(true);
            setSelectedTask(null);
          }}
          onDelete={(id: number) => handleDeleteTask(id)}
        />
      )}
    </div>
  );
}
