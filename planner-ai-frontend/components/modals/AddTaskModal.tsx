"use client";

import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { typeColors } from "@/utils/eventMapper";

/**
 * Add / Edit Task modal (TypeScript, no impure calls during render).
 *
 * Key decisions:
 * - The form state is initialized lazily with useState(() => ...) so Date.now()
 *   and new Dates run only once on mount (no impure calls during render).
 * - We avoid calling setState synchronously inside useEffect to satisfy ESLint.
 * - If you need the modal to respond to changes of `existingTask` while mounted,
 *   we can add a controlled update path later (but that previously caused cascading renders).
 */

/* ---------------- Types ---------------- */
type TaskStatus = "Pending" | "In Progress" | "Completed";
type TaskType = "Assignment" | "Project" | "Practical Exam" | "Written Exam";

export interface Task {
  id: number | string;
  title: string;
  subject?: string;
  type: TaskType;
  difficulty: number;
  description?: string;
  status: TaskStatus;
  startDate: Date;
  endDate: Date;
  color?: string;
}

interface Props {
  existingTask?: Partial<Task> | null; // allow partial since incoming task may be plain object
  onClose: () => void;
  onSave: (task: Task) => void;
}

/* -------------- Component -------------- */
export default function TaskModalAdd({
  existingTask = null,
  onClose,
  onSave,
}: Props) {
  // Lazy init so Date.now() runs only once (allowed inside useState lazy initializer)
  const [form, setForm] = useState<Task>(() => {
    // If editing an existing task, normalize dates and use its values
    if (existingTask && existingTask.startDate && existingTask.endDate) {
      return {
        id: existingTask.id ?? Date.now(),
        title: existingTask.title ?? "",
        subject: existingTask.subject ?? "",
        type: (existingTask.type as TaskType) ?? "Assignment",
        difficulty: existingTask.difficulty ?? 1,
        description: existingTask.description ?? "",
        status: (existingTask.status as TaskStatus) ?? "Pending",
        startDate: new Date(existingTask.startDate),
        endDate: new Date(existingTask.endDate),
        color: existingTask.color ?? (typeColors[(existingTask.type as TaskType) ?? "Assignment"] ?? "#ffd9b3"),
      };
    }

    // Default values for a new task
    const now = new Date();
    const oneHourLater = new Date(now.getTime() + 60 * 60 * 1000);
    return {
      id: Date.now(),
      title: "",
      subject: "",
      type: "Assignment",
      difficulty: 1,
      description: "",
      status: "Pending",
      startDate: now,
      endDate: oneHourLater,
      color: typeColors["Assignment"],
    };
  });

  // Save handler
  const handleSave = () => {
    if (!form.title || !form.title.trim()) {
      alert("Please enter a task title.");
      return;
    }

    const normalized: Task = {
      ...form,
      // ensure correct types
      id: form.id ?? Date.now(),
      title: String(form.title).trim(),
      subject: form.subject ?? "",
      type: form.type,
      difficulty: Number(form.difficulty) || 1,
      description: form.description ?? "",
      status: form.status,
      startDate: form.startDate instanceof Date ? form.startDate : new Date(form.startDate),
      endDate: form.endDate instanceof Date ? form.endDate : new Date(form.endDate),
      color: form.color ?? typeColors[form.type],
    };

    onSave(normalized);
    onClose();
  };

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal-box">
        <h2 className="modal-title">{existingTask ? "✏ Edit Task" : "✨ Add New Task"}</h2>

        <div>
          <label className="block text-sm mb-1">Task Title *</label>
          <input
            className="input-field"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            placeholder="e.g., Read chapter 5"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Subject / Project</label>
          <input
            className="input-field"
            value={form.subject}
            onChange={(e) => setForm({ ...form, subject: e.target.value })}
            placeholder="Optional"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Task Type</label>
          <select
            className="input-field"
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value as TaskType })}
          >
            <option>Assignment</option>
            <option>Project</option>
            <option>Practical Exam</option>
            <option>Written Exam</option>
          </select>
        </div>

        {/* Schedule */}
        <div className="p-2 rounded-lg mt-2">
          <h3 className="font-semibold mb-1 text-center text-sm">📅 Schedule</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label className="block text-xs mb-1">Start</label>
              <DatePicker
                selected={form.startDate}
                onChange={(d) => {
                  const date = d as Date;
                  setForm({
                    ...form,
                    startDate: date,
                    endDate: date > form.endDate ? date : form.endDate,
                  });
                }}
                showTimeSelect
                timeIntervals={15}
                dateFormat="MMM d, yyyy h:mm aa"
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-xs mb-1">End</label>
              <DatePicker
                selected={form.endDate}
                onChange={(d) => setForm({ ...form, endDate: d as Date })}
                showTimeSelect
                timeIntervals={15}
                dateFormat="MMM d, yyyy h:mm aa"
                className="input-field"
                minDate={form.startDate}
              />
            </div>
          </div>
        </div>

        <div>
          <label className="block text-sm mb-1">Difficulty (1–5)</label>
          <input
            className="input-field"
            type="number"
            min={1}
            max={5}
            value={form.difficulty}
            onChange={(e) => setForm({ ...form, difficulty: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Description</label>
          <textarea
            className="textarea-field"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            placeholder="Optional notes..."
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Status</label>
          <select
            className="input-field"
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value as TaskStatus })}
          >
            <option>Pending</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>
        </div>

        <div className="flex justify-end gap-2 mt-3">
          <button type="button" className="modal-button" onClick={onClose}>
            Cancel
          </button>

          <button
            type="button"
            className="modal-button"
            onClick={handleSave}
            style={{ background: "var(--accent)", color: "#fff" }}
          >
            {existingTask ? "Update Task" : "Save Task"}
          </button>
        </div>
      </div>
    </div>
  );
}
