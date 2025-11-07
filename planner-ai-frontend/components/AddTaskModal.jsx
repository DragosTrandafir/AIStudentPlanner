"use client";
import { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function AddTaskModal({ onClose, onSave, existingTask }) {
  const [formData, setFormData] = useState({
    title: "",
    subject: "",
    type: "Assignment",
    difficulty: 1,
    description: "",
    status: "Pending",
  });

  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(
    new Date(new Date().getTime() + 60 * 60 * 1000)
  );

  useEffect(() => {
    if (!existingTask) return;
    Promise.resolve().then(() => {
      setFormData({
        title: existingTask.title || "",
        subject: existingTask.subject || "",
        type: existingTask.type || "Assignment",
        difficulty: existingTask.difficulty || 1,
        description: existingTask.description || "",
        status: existingTask.status || "Pending",
      });
      setStartDate(new Date(existingTask.startDate));
      setEndDate(new Date(existingTask.endDate));
    });
  }, [existingTask]);

  const typeColors = {
    "Assignment": "#F4C2C2",
    "Project": "#F3E5AB",
    "Written Exam": "#AFEEEE",
    "Practical Exam": "#98FB98",
  };

  const handleSave = () => {
    if (!formData.title.trim()) {
      alert("Please enter a task title.");
      return;
    }

    onSave({
      ...formData,
      startDate,
      endDate,
      color: typeColors[formData.type],
      id: existingTask?.id || Date.now(),
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-3">
      <div
        className="w-full max-w-lg p-8 rounded-3xl shadow-2xl border border-amber-300"
        style={{ backgroundColor: "#3B2F2F", color: "#FAEBD7" }}
      >
        <h2 className="text-3xl font-bold text-center mb-6 text-amber-200">
          {existingTask ? "✏ Edit Task" : "✨ Add New Task"}
        </h2>

        <div className="space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm text-amber-100 mb-1">Task Title *</label>
            <input
              type="text"
              placeholder="Enter task name"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white placeholder-amber-200"
            />
          </div>

          {/* Subject */}
          <div>
            <label className="block text-sm text-amber-100 mb-1">Subject / Project</label>
            <input
              type="text"
              placeholder="e.g. Literature, Science..."
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white"
            />
          </div>

          {/* Type */}
          <div>
            <label className="block text-sm text-amber-100 mb-1">Task Type</label>
            <select
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white"
            >
              <option>Assignment</option>
              <option>Project</option>
              <option>Practical Exam</option>
              <option>Written Exam</option>
            </select>
          </div>

          {/* Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-amber-100 mb-1">Start Date & Time</label>
              <DatePicker
                selected={startDate}
                onChange={(date) => {
                  setStartDate(date);
                  if (date > endDate) setEndDate(date);
                }}
                showTimeSelect
                timeFormat="HH:mm"
                timeIntervals={15}
                dateFormat="MMMM d, yyyy h:mm aa"
                className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white"
              />
            </div>
            <div>
              <label className="block text-sm text-amber-100 mb-1">End Date & Time</label>
              <DatePicker
                selected={endDate}
                onChange={(date) => setEndDate(date)}
                showTimeSelect
                timeFormat="HH:mm"
                timeIntervals={15}
                dateFormat="MMMM d, yyyy h:mm aa"
                className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white"
                minDate={startDate}
              />
            </div>
          </div>

          {/* Difficulty */}
          <div>
            <label className="block text-sm text-amber-100 mb-1">Difficulty (1–5)</label>
            <input
              type="number"
              min="1"
              max="5"
              value={formData.difficulty}
              onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm text-amber-100 mb-1">Description</label>
            <textarea
              placeholder="Describe what to do..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white placeholder-amber-200"
            />
          </div>

          {/* Status */}
          <div>
            <label className="block text-sm text-amber-100 mb-1">Status</label>
            <select
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              className="w-full p-2 rounded-lg bg-[#5A4B3C] text-white"
            >
              <option>Pending</option>
              <option>In Progress</option>
              <option>Completed</option>
            </select>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-3 mt-8">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-amber-400 text-brown-900 font-semibold rounded-lg hover:bg-amber-300"
          >
            {existingTask ? "Update Task" : "Save Task"}
          </button>
        </div>
      </div>
    </div>
  );
}
