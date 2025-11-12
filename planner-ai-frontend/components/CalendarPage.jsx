"use client";

import { useState, useRef, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import AddTaskModal from "./AddTaskModal";
import TaskDetailsModal from "./TaskDetailsModal";
import { ChevronLeft, ChevronRight } from "lucide-react";

// Backend config
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
// TODO: Replace with real logged-in user id
const USER_ID = typeof window !== "undefined" && window.localStorage.getItem("user_id")
  ? Number(window.localStorage.getItem("user_id"))
  : 1;

export default function CalendarPage() {
  const calendarRef = useRef(null);
  const [events, setEvents] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [currentMonth, setCurrentMonth] = useState("");
  const [editTask, setEditTask] = useState(null);
  const [miniDate, setMiniDate] = useState(new Date());
  const [loading, setLoading] = useState(false);

  // Backend enum -> friendly label and color
  const typeLabels = {
    project: "Project",
    written: "Written Exam",
    practical: "Practical Exam",
  };
  const typeColors = {
    project: "#F3E5AB",
    written: "#AFEEEE",
    practical: "#98FB98",
  };

  // Transform backend subject -> FullCalendar event
  const subjectToEvent = (subject) => {
    const start = subject.start_date ? new Date(subject.start_date) : null;
    const end = subject.end_date ? new Date(subject.end_date) : null;
    if (!start) return null; // skip items without a start date

    const isSameDay = end && start.toDateString() === end.toDateString();
    const color = typeColors[subject.type] || "#FFF8E1";

    return {
      title: subject.title,
      start,
      ...(end ? { end } : {}),
      backgroundColor: color,
      borderColor: color,
      allDay: !!(end && isSameDay),
      extendedProps: { ...subject },
    };
  };

  const loadSubjects = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/users/${USER_ID}/subjects/`);
      if (!res.ok) throw new Error("Failed to load subjects");
      const data = await res.json();
      const mapped = data
        .map(subjectToEvent)
        .filter(Boolean);
      setEvents(mapped);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => updateMonth(), []);
  useEffect(() => {
    loadSubjects();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSavedSubject = (subject) => {
    // subject returned from AddTaskModal (POST/PUT)
    const ev = subjectToEvent(subject);
    if (!ev) return;
    setEvents((prev) => {
      const idx = prev.findIndex((p) => p.extendedProps.id === subject.id);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = ev;
        return copy;
      }
      return [...prev, ev];
    });
    setShowAddModal(false);
    setEditTask(null);
  };

  const handleDeleteTask = async (taskId) => {
    try {
      const res = await fetch(`${API_BASE}/users/${USER_ID}/subjects/${taskId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Delete failed");
      setEvents((prev) => prev.filter((ev) => ev.extendedProps.id !== taskId));
    } catch (e) {
      console.error(e);
      alert("Failed to delete task");
    }
  };

  const handleEventClick = (info) => setSelectedTask(info.event.extendedProps);

  const eventStyleGetter = () => ({
    style: {
      color: "#71460e",
      borderRadius: "10px",
      fontWeight: 600,
      fontSize: "0.85rem",
      boxShadow: "1px 1px 4px rgba(0,0,0,0.15)",
      padding: "4px",
    },
  });

  //  Navigation controls for main calendar
  const handlePrev = () => {
    calendarRef.current?.getApi().prev();
    updateMonth();
  };
  const handleNext = () => {
    calendarRef.current?.getApi().next();
    updateMonth();
  };
  const handleToday = () => {
    calendarRef.current?.getApi().today();
    updateMonth();
  };

  // Update displayed month (and sync mini calendar)
  const updateMonth = () => {
    const api = calendarRef.current?.getApi();
    if (api) {
      const date = api.getDate();
      setCurrentMonth(
        date.toLocaleString("default", { month: "long", year: "numeric" })
      );
      setMiniDate(date);
    }
  };

  //  Mini calendar → main calendar sync
  const handleMiniSelect = (date) => {
    const api = calendarRef.current?.getApi();
    if (api) {
      api.gotoDate(date);
      updateMonth();
    }
  };

  useEffect(() => {
    const accentColor = "#e63d00";
    const style = document.createElement("style");
    style.innerHTML = `
      /* Borders */
      .fc-theme-standard td, .fc-theme-standard th {
        border: 1px solid ${accentColor} !important;
      }
      .fc-scrollgrid {
        border: 2px solid ${accentColor} !important;
        border-radius: 10px;
      }

      /* Today cell */
      .fc-day-today {
        background-color: rgba(230, 61, 0, 0.08) !important;
        border: 2px solid ${accentColor} !important;
        border-radius: 8px;
      }

      /* Weekday names (Mon, Tue...) */
      .fc .fc-col-header-cell-cushion {
        color: ${accentColor} !important;
        font-weight: 700;
      }

      /* Day numbers (1, 2, 3...) */
      .fc-daygrid-day-number {
        color: ${accentColor} !important;
        font-weight: 600;
      }

      /* Faded days from previous/next month */
      .fc-day-other .fc-daygrid-day-number {
        color: rgba(230, 61, 0, 0.5) !important;
      }

      /* Hover on day cells */
      .fc-daygrid-day:hover {
        background-color: rgba(230, 61, 0, 0.05) !important;
        transition: background-color 0.2s ease;
      }
    `;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);

  return (
    <div
      className="flex min-h-screen overflow-hidden"
      style={{
        background: "linear-gradient(180deg, #ffe5e5 0%, #fff0d6 100%)",
        fontFamily: "Georgia, 'Times New Roman', serif",
      }}
    >
      {/* Sidebar */}
      <aside className="w-72 flex flex-col justify-between border-r border-[#e3caa8] bg-[#fff8f0] shadow-md p-4 fixed top-0 left-0 bottom-0">
        <div>
          <h2 className="text-2xl font-bold text-[#71460e] mb-4">Task Legend</h2>
          <ul className="space-y-3 text-[#71460e]">
            {/* Only backend-supported types */}
            <Legend color={typeColors.project} label={typeLabels.project} />
            <Legend color={typeColors.written} label={typeLabels.written} />
            <Legend color={typeColors.practical} label={typeLabels.practical} />
          </ul>
        </div>

        <div className="mt-8 mb-2">
          <MiniCalendar
            date={miniDate}
            onPrev={() =>
              setMiniDate(new Date(miniDate.getFullYear(), miniDate.getMonth() - 1, 1))
            }
            onNext={() =>
              setMiniDate(new Date(miniDate.getFullYear(), miniDate.getMonth() + 1, 1))
            }
            onSelectDate={handleMiniSelect}
          />
        </div>
      </aside>

      {/* Main Calendar */}
      <main
        className="flex-1 p-6 transition-all duration-300"
        style={{
          marginLeft: "18rem",
          width: "calc(100% - 18rem)",
          overflowX: "auto",
        }}
      >
        <div className="flex justify-between items-start mb-6">
          <div className="flex flex-col items-start">
            <h1 className="text-4xl font-bold text-[#71460e] capitalize mb-3">
              {currentMonth}
            </h1>
            <AddButton onClick={() => setShowAddModal(true)} />
          </div>

          <div className="flex flex-col items-center gap-3">
            <div className="flex items-center gap-3">
              <ArrowButton direction="left" onClick={handlePrev} />
              <TodayButton label="Today" onClick={handleToday} />
              <ArrowButton direction="right" onClick={handleNext} />
            </div>

            <div className="flex gap-2">
              <TodayButton
                label="Month"
                onClick={() => calendarRef.current?.getApi().changeView("dayGridMonth")}
              />
              <TodayButton
                label="Week"
                onClick={() => calendarRef.current?.getApi().changeView("timeGridWeek")}
              />
              <TodayButton
                label="Day"
                onClick={() => calendarRef.current?.getApi().changeView("timeGridDay")}
              />
            </div>
          </div>
        </div>

        {/* Big Calendar */}
        <div
          className="rounded-2xl shadow-md p-4 mx-auto"
          style={{
            background: "linear-gradient(180deg, #fff5f8 0%, #ffe9f0 100%)",
            border: "2px solid #ffcaca",
            maxWidth: "1200px",
          }}
        >
          <FullCalendar
            ref={calendarRef}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="dayGridMonth"
            headerToolbar={false}
            events={events}
            eventPropGetter={eventStyleGetter}
            eventClick={handleEventClick}
            height="auto"
            contentHeight="auto"
            nowIndicator
            allDaySlot={false}
            firstDay={1}
            displayEventTime={false}
            dayMaxEventRows={false}
            eventMaxStack={9999}
            eventOverlap={true}
            aspectRatio={1.8}
            datesSet={updateMonth}
            eventContent={(arg) => {
              const { title, extendedProps } = arg.event;
              return (
                <div
                  style={{
                    padding: "4px",
                    color: "#71460e",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                >
                  <div className="font-semibold">{title}</div>
                  {extendedProps?.description && (
                    <div className="text-xs opacity-80 truncate">
                      {extendedProps.description}
                    </div>
                  )}
                </div>
              );
            }}
          />
          {loading && (
            <div className="text-center text-sm text-[#71460e] mt-2">Loading…</div>
          )}
        </div>
      </main>

      {/* Modals */}
      {showAddModal && (
        <AddTaskModal
          onClose={() => {
            setShowAddModal(false);
            setEditTask(null);
          }}
          onSave={handleSavedSubject}
          existingTask={editTask}
          apiBase={API_BASE}
          userId={USER_ID}
        />
      )}
      {selectedTask && (
        <TaskDetailsModal
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onEdit={(task) => {
            setSelectedTask(null);
            setEditTask(task);
            setShowAddModal(true);
          }}
          onDelete={handleDeleteTask}
        />
      )}
    </div>
  );
}

/* Small Components */
function Legend({ color, label }) {
  return (
    <li className="flex items-center gap-2">
      <span
        className="w-4 h-4 rounded"
        style={{ backgroundColor: color, border: "1px solid #71460e" }}
      ></span>
      {label}
    </li>
  );
}

function TodayButton({ label, onClick }) {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-[#fff8f0] border border-[#71460e] rounded-xl text-[#71460e] text-sm font-semibold shadow-md hover:bg-[#ffe5e5] transition-all active:translate-y-[3px] active:shadow-inner"
    >
      {label}
    </button>
  );
}

function ArrowButton({ direction, onClick }) {
  return (
    <button
      onClick={onClick}
      className="p-2 bg-[#fff8f0] border border-[#71460e] rounded-full text-[#71460e] hover:bg-[#ffe5e5] active:translate-y-[3px] transition-all shadow-md"
    >
      {direction === "left" ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
    </button>
  );
}

function AddButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="px-5 py-2 bg-[#aa6c32] text-white text-lg font-bold rounded-2xl shadow-md hover:bg-[#b38b66] transition-all active:translate-y-[4px] active:shadow-inner"
    >
      + Add Task
    </button>
  );
}

function MiniCalendar({ date, onPrev, onNext, onSelectDate }) {
  const today = new Date();
  const year = date.getFullYear();
  const month = date.getMonth();

  let firstDay = new Date(year, month, 1).getDay();
  firstDay = (firstDay + 6) % 7;

  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const prevMonthDays = new Date(year, month, 0).getDate();

  // Build list of visible days (including prev/next months)
  const days = [];
  for (let i = 0; i < firstDay; i++)
    days.push({ day: prevMonthDays - firstDay + i + 1, current: false });
  for (let i = 1; i <= daysInMonth; i++) days.push({ day: i, current: true });
  while (days.length % 7 !== 0)
    days.push({ day: days.length - daysInMonth - firstDay + 1, current: false });

  const weekdayLabels = ["M", "T", "W", "T", "F", "S", "S"];

  return (
    <div className="bg-white shadow-sm rounded-xl border border-gray-300 p-3 w-full">
      <div className="flex justify-between items-center mb-2">
        <button onClick={onPrev} className="text-gray-600 hover:text-[#71460e]">
          <ChevronLeft size={18} />
        </button>
        <div className="font-semibold text-[#71460e] text-sm">
          {date.toLocaleString("default", { month: "long", year: "numeric" })}
        </div>
        <button onClick={onNext} className="text-gray-600 hover:text-[#71460e]">
          <ChevronRight size={18} />
        </button>
      </div>

      <div className="grid grid-cols-7 text-center text-xs font-semibold text-[#71460e] mb-1">
        {weekdayLabels.map((d, i) => (
          <div key={i}>{d}</div>
        ))}
      </div>

      <div className="grid grid-cols-7 text-center text-sm">
        {days.map((d, i) => {
          const isToday =
            d.current &&
            today.getDate() === d.day &&
            today.getMonth() === month &&
            today.getFullYear() === year;
          return (
            <div
              key={i}
              onClick={() => d.current && onSelectDate(new Date(year, month, d.day))}
              className={`py-1 cursor-pointer transition-all ${
                d.current ? "text-[#71460e]" : "text-gray-400"
              } hover:bg-[#ffe5e5] rounded-lg`}
            >
              <div
                className={`w-6 h-6 mx-auto flex items-center justify-center rounded-full ${
                  isToday ? "bg-red-500 text-white font-bold" : ""
                }`}
              >
                {d.day}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
