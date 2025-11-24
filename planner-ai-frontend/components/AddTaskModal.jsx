"use client";
import { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function AddTaskModal({ onClose, onSave, existingTask, apiBase, userId }) {
  // Keep state values in BACKEND shape to minimize mapping
  const [formData, setFormData] = useState({
    title: "",
    name: "", // backend 'name' is the Subject / Project field
    type: "project", // backend enum: project | written | practical
    difficulty: 1,
    description: "",
    status: "not_started", // backend enum: not_started | in_progress | completed
  });

  //  Date state for task scheduling (Date objects for UI)
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date(new Date().getTime() + 60 * 60 * 1000));

  // Populate form if editing an existing task (backend shape)
  useEffect(() => {
    if (!existingTask) return;
    Promise.resolve().then(() => {
      setFormData({
        title: existingTask.title || "",
        name: existingTask.name || "",
        type: existingTask.type || "project",
        difficulty: existingTask.difficulty ?? 1,
        description: existingTask.description || "",
        status: existingTask.status || "not_started",
      });
      if (existingTask.start_date) setStartDate(new Date(existingTask.start_date));
      if (existingTask.end_date) setEndDate(new Date(existingTask.end_date));
    });
  }, [existingTask]);

  const typeLabels = {
    project: "Project",
    written: "Written Exam",
    practical: "Practical Exam",
  };

  const statusLabels = {
    not_started: "Not Started",
    in_progress: "In Progress",
    completed: "Completed",
  };

  const handleSubmit = async () => {
    if (!formData.title.trim()) {
      alert("Please enter a task title.");
      return;
    }
    if (!formData.name.trim()) {
      alert("Please enter the task name.");
      return;
    }

    const payload = {
      title: formData.title,
      name: formData.name,
      type: formData.type,
      status: formData.status,
      difficulty: Number(formData.difficulty),
      start_date: startDate ? new Date(startDate).toISOString() : null,
      end_date: endDate ? new Date(endDate).toISOString() : null,
      description: formData.description || null,
    };

    try {
      const url = existingTask?.id
        ? `${apiBase}/users/${userId}/tasks/${existingTask.id}`
        : `${apiBase}/users/${userId}/tasks/`;
      const method = existingTask?.id ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || "Failed to save task");
      }
      const saved = await res.json();
      onSave(saved);
      onClose();
    } catch (e) {
      console.error(e);
      alert("Error saving task");
    }
  };

  const accentColor = "#8a0f5d";

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 px-3">
      <div
        className="w-full max-w-md p-4 rounded-2xl shadow-2xl border"
        style={{
          backgroundColor: "#ffefd5",
          borderColor: accentColor,
          color: accentColor,
          maxHeight: "90vh",
          overflowY: "auto",
        }}
      >
        <h2
          className="text-xl font-bold text-center mb-4"
          style={{ color: accentColor }}
        >
          {existingTask ? "✏ Edit Task" : "✨ Add New Task"}
        </h2>

        <div className="space-y-2">
          {/* Title */}
          <div>
            <label className="block text-sm mb-1" style={{ color: accentColor }}>
              Task Title *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-2 py-1 rounded-lg text-sm"
              style={{
                backgroundColor: "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            />
          </div>

          {/* Subject Name (backend 'name') */}
          <div>
            <label className="block text-sm mb-1" style={{ color: accentColor }}>
              Subject / Project
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-2 py-1 rounded-lg text-sm"
              style={{
                backgroundColor: "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            />
          </div>

          {/* Type (backend enum) */}
          <div>
            <label className="block text-sm mb-1" style={{ color: accentColor }}>
              Task Type
            </label>
            <select
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              className="w-full px-2 py-1 rounded-lg text-sm"
              style={{
                backgroundColor: "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            >
              <option value="project">{typeLabels.project}</option>
              <option value="practical">{typeLabels.practical}</option>
              <option value="written">{typeLabels.written}</option>
            </select>
          </div>

          {/* Dates Section */}
          <div
            className="p-2 rounded-lg mt-2"
            style={{
              backgroundColor: "#ffe6f1",
              border: `1px solid ${accentColor}`,
            }}
          >
            <h3
              className="font-semibold mb-1 text-center text-sm"
              style={{ color: accentColor }}
            >
              📅 Schedule
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <div
                className="p-1 rounded-lg"
                style={{
                  border: `1px solid ${accentColor}`,
                  backgroundColor: "#fff8f5",
                }}
              >
                <label className="block text-xs mb-1" style={{ color: accentColor }}>
                  Start
                </label>
                <DatePicker
                  selected={startDate}
                  onChange={(date) => {
                    setStartDate(date);
                    if (date > endDate) setEndDate(date);
                  }}
                  showTimeSelect
                  timeFormat="HH:mm"
                  timeIntervals={15}
                  dateFormat="MMM d, yyyy h:mm aa"
                  className="w-full px-2 py-1 rounded-lg text-xs"
                  style={{
                    backgroundColor: "#fff",
                    color: accentColor,
                    border: `1px solid ${accentColor}`,
                  }}
                />
              </div>

              <div
                className="p-1 rounded-lg"
                style={{
                  border: `1px solid ${accentColor}`,
                  backgroundColor: "#fff8f5",
                }}
              >
                <label className="block text-xs mb-1" style={{ color: accentColor }}>
                  End
                </label>
                <DatePicker
                  selected={endDate}
                  onChange={(date) => setEndDate(date)}
                  showTimeSelect
                  timeFormat="HH:mm"
                  timeIntervals={15}
                  dateFormat="MMM d, yyyy h:mm aa"
                  className="w-full px-2 py-1 rounded-lg text-xs"
                  style={{
                    backgroundColor: "#fff",
                    color: accentColor,
                    border: `1px solid ${accentColor}`,
                  }}
                  minDate={startDate}
                />
              </div>
            </div>
          </div>

          {/* Difficulty */}
          <div>
            <label className="block text-sm mb-1" style={{ color: accentColor }}>
              Difficulty (1–5)
            </label>
            <input
              type="number"
              min="1"
              max="5"
              value={formData.difficulty}
              onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              className="w-full px-2 py-1 rounded-lg text-sm"
              style={{
                backgroundColor: "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm mb-1" style={{ color: accentColor }}>
              Description
            </label>
            <textarea
              rows="2"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-2 py-1 rounded-lg text-sm"
              style={{
                backgroundColor: "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            />
          </div>

          {/* Status (backend enum) */}
          <div>
            <label className="block text-sm mb-1" style={{ color: accentColor }}>
              Status
            </label>
            <select
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              className="w-full px-2 py-1 rounded-lg text-sm"
              style={{
                backgroundColor: "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            >
              <option value="not_started">{statusLabels.not_started}</option>
              <option value="in_progress">{statusLabels.in_progress}</option>
              <option value="completed">{statusLabels.completed}</option>
            </select>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-2 mt-4">
          <button
            onClick={onClose}
            className="px-3 py-1 text-sm rounded-lg font-semibold transition-all active:translate-y-[1px]"
            style={{
              backgroundColor: "#fcd2e0",
              color: accentColor,
              border: `1px solid ${accentColor}`,
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="px-3 py-1 text-sm rounded-lg font-semibold transition-all active:translate-y-[1px]"
            style={{
              backgroundColor: accentColor,
              color: "#fff",
              border: `1px solid ${accentColor}`,
            }}
          >
            {existingTask ? "Update Task" : "Save Task"}
          </button>
        </div>
      </div>
    </div>
  );
}
