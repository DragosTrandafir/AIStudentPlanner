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

  /* ---------------- COLORS PER TYPE ---------------- */
  const typeColors = {
    Assignment: "#F4C2C2",
    Project: "#F3E5AB",
    "Written Exam": "#bde0fe",
    "Practical Exam": "#c8f7c5",
  };

  /* ---------------- MULTI-DAY EVENT EXPANSION ---------------- */
  const eventsByDay = useMemo(() => {
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
      const nextWeek = new Date(selectedDate);
      nextWeek.setDate(selectedDate.getDate() + 7);
      setSelectedDate(nextWeek);
    } else {
      const nextDay = new Date(selectedDate);
      nextDay.setDate(selectedDate.getDate() + 1);
      setSelectedDate(nextDay);
    }
  };

  const prev = () => {
    if (viewMode === "month") {
      setCurrentMonth(
        new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, 1)
      );
    } else if (viewMode === "week") {
      const prevWeek = new Date(selectedDate);
      prevWeek.setDate(selectedDate.getDate() - 7);
      setSelectedDate(prevWeek);
    } else {
      const prevDay = new Date(selectedDate);
      prevDay.setDate(selectedDate.getDate() - 1);
      setSelectedDate(prevDay);
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

  /* ============================================================
     RENDER
  ============================================================ */
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

      {/* MAIN CONTENT */}
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

          <div className="flex flex-col gap-3 items-end">
            <div className="flex gap-2 main-header-buttons">
              <button className="nav-button" onClick={prev}>‹</button>
              <button className="nav-button" onClick={goToToday}>Today</button>
              <button className="nav-button" onClick={next}>›</button>
            </div>

            <div className="flex gap-2 main-header-buttons">
              <button className={`nav-button ${viewMode === "month" ? "active-view" : ""}`}
                onClick={() => setViewMode("month")}
              >
                Month
              </button>

              <button className={`nav-button ${viewMode === "week" ? "active-view" : ""}`}
                onClick={() => setViewMode("week")}
              >
                Week
              </button>

              <button className={`nav-button ${viewMode === "day" ? "active-view" : ""}`}
                onClick={() => setViewMode("day")}
              >
                Day
              </button>
            </div>
          </div>
        </div>

        {/* ---------------- MONTH VIEW + MULTI-DAY BARS ---------------- */}
        {viewMode === "month" && (
          <div className="calendar-container">
            <div className="calendar-weekdays">
              {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((d) => (
                <div key={d}>{d}</div>
              ))}
            </div>

            <div className="calendar-grid-days">
              {monthMatrix.flatMap((week, wi) =>
                week.map((day, di) => {
                  const key = `${day.getFullYear()}-${day.getMonth()}-${day.getDate()}`;
                  const events = eventsByDay.get(key) ?? [];

                  const inMonth = day.getMonth() === currentMonth.getMonth();
                  const selected = isSameDay(day, selectedDate);

                  return (
                    <div
                      key={`${wi}-${di}`}
                      className={`calendar-day-cell ${inMonth ? "in-month" : "out-month"} ${
                        selected ? "selected" : ""
                      }`}
                      onClick={() => setSelectedDate(day)}
                    >
                      <div className="day-number">{day.getDate()}</div>

                      {/* MULTI-DAY BARS */}
                      <div className="event-wrapper">
                        {events.map((ev) => {
                          const start = new Date(ev.startDate);
                          const end = new Date(ev.endDate);

                          const isStart =
                            start.getFullYear() === day.getFullYear() &&
                            start.getMonth() === day.getMonth() &&
                            start.getDate() === day.getDate();

                          const isEnd =
                            end.getFullYear() === day.getFullYear() &&
                            end.getMonth() === day.getMonth() &&
                            end.getDate() === day.getDate();

                          const spanDays =
                            Math.floor(
                              (end.getTime() - start.getTime()) /
                                (1000 * 60 * 60 * 24)
                            ) + 1;

                          // draw bar only on start day
                          if (!isStart) return null;

                          return (
                            <div
                              key={ev.id}
                              className="event-bar"
                              style={{
                                width: `calc(${spanDays} * 100% + ${(spanDays - 1) *
                                  2}px)`,
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
                        })}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {viewMode === "week" && (
          <WeekView selectedDate={selectedDate} tasks={tasks} onSelectTask={setSelectedTask} />
        )}

        {viewMode === "day" && (
          <DayView selectedDate={selectedDate} tasks={tasks} onSelectTask={setSelectedTask} />
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
