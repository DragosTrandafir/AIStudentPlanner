"use client";

import { useState, useRef, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import AddTaskModal from "./AddTaskModal";
import TaskDetailsModal from "./TaskDetailsModal";

export default function CalendarPage() {
  const calendarRef = useRef(null);
  const [events, setEvents] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [currentMonth, setCurrentMonth] = useState("");
  const [editTask, setEditTask] = useState(null);

  // Event styles
  const eventStyleGetter = (event) => {
    return {
      style: {
        backgroundColor: event.extendedProps.color || "#FFF8E1",
        color: "#71460e",
        borderRadius: "10px",
        padding: "6px",
        fontWeight: 600,
        fontSize: "0.85rem",
        border: "1px solid rgba(0,0,0,0.1)",
      },
    };
  };

  const handleSaveTask = (task) => {
    setEvents((prev) => {
      const idx = prev.findIndex((ev) => ev.extendedProps.id === task.id);
      const newEvent = {
        title: task.title,
        start: new Date(task.startDate),
        end: new Date(task.endDate),
        extendedProps: { ...task },
      };
      if (idx >= 0) {
        const updated = [...prev];
        updated[idx] = newEvent;
        return updated;
      }
      return [...prev, newEvent];
    });
    setShowAddModal(false);
    setEditTask(null);
  };

  const handleDeleteTask = (taskId) => {
    setEvents((prev) => prev.filter((ev) => ev.extendedProps.id !== taskId));
  };

  const handleEventClick = (info) => setSelectedTask(info.event.extendedProps);

  const setView = (view) => {
    const api = calendarRef.current.getApi();
    api.changeView(view);
    updateMonth();
  };

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

  const updateMonth = () => {
    const api = calendarRef.current?.getApi();
    if (api) {
      const date = api.getDate();
      setCurrentMonth(
        date.toLocaleString("default", { month: "long", year: "numeric" })
      );
    }
  };

  useEffect(() => updateMonth(), []);

  return (
    <div className="p-6 min-h-screen" style={{ backgroundColor: "#f2dede" }}>
      {/* Header */}
      <div className="flex flex-col items-center mb-6">
        <h1 className="text-4xl font-bold text-[#71460e] mb-3">{currentMonth}</h1>

        {/* Navigation */}
        <div className="flex flex-wrap justify-center gap-2 mb-2">
          <button
            className="px-3 py-1 bg-white border border-[#71460e] rounded-lg shadow-sm text-[#71460e] hover:bg-[#ffe5e5]"
            onClick={handlePrev}
          >
            ← Prev
          </button>
          <button
            className="px-3 py-1 bg-white border border-[#71460e] rounded-lg shadow-sm text-[#71460e] hover:bg-[#ffe5e5]"
            onClick={handleToday}
          >
            Today
          </button>
          <button
            className="px-3 py-1 bg-white border border-[#71460e] rounded-lg shadow-sm text-[#71460e] hover:bg-[#ffe5e5]"
            onClick={handleNext}
          >
            Next →
          </button>
        </div>

        {/* View Controls */}
        <div className="flex gap-2 flex-wrap justify-center mb-4">
          <button
            className="px-3 py-1 bg-white rounded-lg shadow-sm hover:bg-[#ffe5e5] border border-[#71460e] text-[#71460e]"
            onClick={() => setView("dayGridMonth")}
          >
            Month
          </button>
          <button
            className="px-3 py-1 bg-white rounded-lg shadow-sm hover:bg-[#ffe5e5] border border-[#71460e] text-[#71460e]"
            onClick={() => setView("timeGridWeek")}
          >
            Week
          </button>
          <button
            className="px-3 py-1 bg-white rounded-lg shadow-sm hover:bg-[#ffe5e5] border border-[#71460e] text-[#71460e]"
            onClick={() => setView("timeGridDay")}
          >
            Day
          </button>
          <button
            className="px-4 py-1 bg-[#71460e] text-white rounded-lg shadow hover:bg-[#532e08]"
            onClick={() => setShowAddModal(true)}
          >
            + Add Task
          </button>
        </div>
      </div>

      {/* Calendar */}
      <div
        className="rounded-2xl shadow-md p-4"
        style={{
          background: "linear-gradient(180deg, #ffe5e5 0%, #ffd6d6 100%)",
          border: "2px solid #ffcaca",
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
          height="75vh"
          nowIndicator
          allDaySlot={false}
          dayMaxEvents={false}
          slotEventOverlap={false}
          eventOverlap={true}
          datesSet={updateMonth}
          eventContent={(arg) => (
            <div
              style={{
                padding: "4px",
                color: "#71460e",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              <div className="font-semibold">{arg.event.title}</div>
              {arg.event.extendedProps.description && (
                <div className="text-xs opacity-90 truncate">
                  {arg.event.extendedProps.description}
                </div>
              )}
            </div>
          )}
          dayHeaderContent={(arg) => (
            <div
              style={{
                color: "#71460e",
                fontWeight: "600",
                textAlign: "center",
              }}
            >
              {arg.text}
            </div>
          )}
          dayCellContent={(arg) => (
            <div
              style={{
                color: "#71460e",
                fontWeight: "600",
                textAlign: "right",
                paddingRight: "4px",
              }}
            >
              {arg.dayNumberText}
            </div>
          )}
        />
      </div>

      {/* Modals */}
      {showAddModal && (
        <AddTaskModal
          onClose={() => {
            setShowAddModal(false);
            setEditTask(null);
          }}
          onSave={handleSaveTask}
          existingTask={editTask}
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
        />
      )}
    </div>
  );
}
