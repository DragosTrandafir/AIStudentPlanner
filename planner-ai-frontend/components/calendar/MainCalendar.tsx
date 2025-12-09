"use client";
import Sidebar from "@/components/sidebar/Sidebar";

import AddTaskModal from "@/components/modals/AddTaskModal";
import TaskDetailsModal from "@/components/modals/TaskDetailsModal";

import WeekView from "@/components/calendar/WeekView";
import DayView from "@/components/calendar/DayView";
import CalendarHeader from "@/components/calendar/CalendarHeader";
import React, { useState, useMemo, useEffect } from "react";



import { getMonthMatrix, isSameDay } from "@/utils/dateUtils";
import { Task } from "@/types/Task";
import { AITask } from "@/types/AITask";
//import { useTheme } from "@/components/context/ThemeContext";


import "@/styles/calendar.css";
import { getSubjects, deleteSubject } from "@/lib/apiSubjects";
import { mapSubjectToTask } from "@/utils/subjectMapper";
import { generatePlan, getPlans, PlanResponse } from "@/lib/apiPlans";



export default function MainCalendar() {
  const today = new Date();
  // ---------------- LOAD TASKS FROM BACKEND ----------------
  const [tasks, setTasks] = useState<Task[]>([]);
  const [aiTasks, setAiTasks] = useState<AITask[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const subjects = await getSubjects();
        const mapped = subjects.map(mapSubjectToTask);
        setTasks(mapped);
      } catch (err) {
        console.error("Failed loading subjects", err);
      }
    }

    load();
  }, []);

  // Load existing AI tasks/plans on mount
  useEffect(() => {
    async function loadPlans() {
      try {
        const plans = await getPlans();
        const mappedAiTasks = mapPlansToAiTasks(plans);
        setAiTasks(mappedAiTasks);
      } catch (err) {
        console.error("Failed loading plans", err);
      }
    }
    loadPlans();
  }, []);


  /* ---------------- STATE ---------------- */
  const [selectedDate, setSelectedDate] = useState<Date>(today);
  const [currentMonth, setCurrentMonth] = useState<Date>(today);

  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  const [viewMode, setViewMode] = useState<"month" | "week" | "day">("month");

  const monthMatrix = useMemo(
    () => getMonthMatrix(currentMonth),
    [currentMonth]
  );
  const currentMonthLabel = currentMonth.toLocaleDateString("en-US", {
  month: "long",
  year: "numeric",
});





  /* ---------------- COLORS ---------------- */
  const typeColors = {
    Assignment: "#F4C2C2",
    Project: "#90EE90",
    "Written Exam": "#87CEFA",
    "Practical Exam": "#FFB6C1",
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

  /* ---------------- AI TASKS EVENT MAP ---------------- */
  const aiTasksMap = useMemo(() => {
    const map = new Map<string, AITask[]>();

    for (const t of aiTasks) {
      const d = new Date(t.date);
      const key = `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(t);
    }

    return map;
  }, [aiTasks]);

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
  setTasks(prev => {
    const idx = prev.findIndex(t => t.id === task.id);
    if (idx >= 0) {
      const copy = [...prev];
      copy[idx] = task;   // 🔥 UPDATE in place
      return copy;
    }
    return [...prev, task]; // 🔥 NEW
  });
}



  /* ---------------- DELETE TASK ---------------- */
  async function handleDelete(id: number) {
  try {
    await deleteSubject(id);

    setTasks((prev) => prev.filter((t) => t.id !== id));
    setSelectedTask(null);
  } catch (err) {
    console.error(err);
    alert("Failed to delete task.");
  }
}

/* ---------------- ADD / EDIT MODAL STATE ---------------- */
const [showAddModal, setShowAddModal] = useState(false);
const [editTask, setEditTask] = useState<Task | null>(null);

/* Open modal to CREATE a new task */
const openAddTaskModal = () => {
  setEditTask(null);        
  setShowAddModal(true); 
};

// Helper function to map plans to AI tasks for calendar display
function mapPlansToAiTasks(plans: PlanResponse[]): AITask[] {
  const aiTaskColors: Record<number, string> = {
    1: "#FF6B6B", // High priority - red
    2: "#FFB84D", // orange
    3: "#FFE66D", // yellow
    4: "#4ECDC4", // teal
    5: "#95E1D3", // light green
  };

  const mapped: AITask[] = [];
  let idCounter = 0;

  for (const plan of plans) {
    const planDate = new Date(plan.plan_date);

    for (const entry of plan.entries) {
      idCounter++;
      mapped.push({
        id: `ai-task-${idCounter}`,
        time_allotted: entry.time_allotted,
        ai_task_name: entry.ai_task_name,
        subject_name: entry.task_name, // task_name is the subject name from backend
        difficulty: entry.difficulty,
        priority: entry.priority,
        date: planDate,
        color: aiTaskColors[Math.min(entry.priority, 5)] || "#95E1D3",
      });
    }
  }

  return mapped;
}

// --- AI PLAN GENERATION ---
async function generateAIPlan() {
  console.log("AI Generate Plan triggered!");
  setIsGenerating(true);

  try {
    const response = await generatePlan();
    console.log("Generated plan:", response);

    // Map the generated plans to AI tasks for display
    const mappedAiTasks = mapPlansToAiTasks(response.plans);
    setAiTasks(mappedAiTasks);

    alert(`${response.message}`);
  } catch (err) {
    console.error("Failed to generate plan:", err);
    alert("Failed to generate AI plan. Please make sure you have subjects added and try again.");
  } finally {
    setIsGenerating(false);
  }
}

function regenerateAIPlan(feedback: string) {
  console.log("Regenerating plan with feedback:", feedback);
  alert("Regeneration with feedback will be added later!");
}





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
        onGeneratePlan={generateAIPlan}
        onRegeneratePlan={(feedback) => regenerateAIPlan(feedback)}
        isGenerating={isGenerating}
      />

      {/* MAIN */}
      <main className="flex-1 px-10 py-6 bg-gradient-to-b from-[#ffe5e5] to-[#fff0d6] overflow-auto">
        

       <CalendarHeader
        currentMonth={currentMonthLabel}
        onPrev={prev}
        onNext={next}
        onToday={goToToday}
        onAddTask={openAddTaskModal}   // ✅ FIXED
        view={viewMode}
        setView={setViewMode}
      />



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
                  const dayAiTasks = aiTasksMap.get(key) ?? [];

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

                      {/* ================== AI TASKS ================== */}
                      <div className="ai-task-container">
                        {dayAiTasks.map((aiTask) => (
                          <div
                            key={aiTask.id}
                            className="ai-task-pill"
                            style={{
                              backgroundColor: aiTask.color || "#95E1D3",
                            }}
                            title={`${aiTask.ai_task_name} (${aiTask.time_allotted}) - ${aiTask.subject_name}`}
                          >
                            <span className="ai-task-time">{aiTask.time_allotted.split("–")[0]}</span>
                            <span className="ai-task-name">{aiTask.ai_task_name}</span>
                          </div>
                        ))}
                      </div>
                      {/* ================== END AI TASKS ================== */}

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
