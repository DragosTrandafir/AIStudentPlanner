"use client";

import React from "react";
import { typeColors } from "@/utils/eventMapper";

// ---- Types ----
type TaskStatus = "Pending" | "In Progress" | "Completed";
type TaskType = "Assignment" | "Project" | "Practical Exam" | "Written Exam";

interface Task {
  id: number;
  title: string;
  subject: string;
  type: TaskType;
  difficulty: number;
  description: string;
  status: TaskStatus;
  startDate: Date | string;
  endDate: Date | string;
  color?: string;
}

interface Props {
  task: Task | null;
  onClose: () => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

interface DetailProps {
  label: string;
  value: React.ReactNode;
  extraClasses?: string;
}

// ---------------------------------------

export default function TaskModalDetails({
  task,
  onClose,
  onEdit,
  onDelete,
}: Props) {
  if (!task) return null;

  const handleDelete = () => {
    if (!window.confirm(`Delete "${task.title}"?`)) return;
    onDelete(task.id);
    onClose();
  };

  const bg = task.color || typeColors[task.type] || "#ddd";

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal-box">
        <h2 className="modal-title">📋 Task Details</h2>

        <div className="space-y-2 text-sm">
          <Detail label="Title" value={task.title} />
          <Detail label="Subject" value={task.subject || "—"} />

          <div>
            <label className="block text-sm mb-1">Type</label>
            <div
              className="px-2 py-1 rounded-lg text-sm font-semibold inline-block"
              style={{ background: bg }}
            >
              {task.type}
            </div>
          </div>

          <Detail label="Status" value={task.status} />
          <Detail label="Difficulty" value={`${task.difficulty}/5`} />

          <Detail
            label="Start"
            value={new Date(task.startDate).toLocaleString()}
          />
          <Detail
            label="End"
            value={new Date(task.endDate).toLocaleString()}
          />

          {task.description && (
            <Detail
              label="Description"
              value={task.description}
              extraClasses="whitespace-pre-line"
            />
          )}
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: 8,
            marginTop: 12,
          }}
        >
          <button className="modal-button" onClick={() => onEdit(task)}>
            ✏ Edit
          </button>

          <button
            className="modal-button modal-button-danger"
            onClick={handleDelete}
          >
            🗑 Delete
          </button>

          <button
            className="modal-button"
            onClick={onClose}
            style={{ background: "var(--accent)", color: "#fff" }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

// --- Sub-component fully typed ---
function Detail({ label, value, extraClasses = "" }: DetailProps) {
  return (
    <div>
      <label className="block text-sm mb-1">{label}</label>
      <div
        className={`px-2 py-1 rounded-lg text-sm ${extraClasses}`}
        style={{
          background: "var(--field-bg)",
          border: "1px solid var(--accent)",
          color: "var(--accent)",
        }}
      >
        {value}
      </div>
    </div>
  );
}
