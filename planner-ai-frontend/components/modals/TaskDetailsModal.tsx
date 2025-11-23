"use client";

import React from "react";
import { Task } from "@/types/Task";
import { typeColors } from "@/utils/eventMapper";

interface Props {
  task: Task;
  onClose: () => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

export default function TaskDetailsModal({
  task,
  onClose,
  onEdit,
  onDelete,
}: Props) {
  if (!task) return null;

  return (
    <div
      className="fixed inset-0 flex items-center justify-center z-50"
      style={{
        background: "rgba(0,0,0,0.35)",
        backdropFilter: "blur(3px)",
      }}
    >
      <div
        className="rounded-2xl shadow-xl p-8"
        style={{
          width: "550px",
          maxHeight: "90vh",
          overflowY: "auto",
          background: "linear-gradient(to bottom, #ffe8d9, #fff4e7)",
          border: "4px solid #e4b6a4",
        }}
      >
        {/* HEADER */}
        <h2
          className="text-center mb-6 font-bold"
          style={{ fontSize: "22px", color: "#7a3e25" }}
        >
          📋 Task Details
        </h2>

        {/* CONTENT */}
        <div className="space-y-3 text-[#5a3e2b] text-sm">
          <p>
            <strong>Title:</strong> {task.title}
          </p>

          <p>
            <strong>Subject:</strong> {task.subject || "—"}
          </p>

          <p>
            <strong>Type:</strong> {task.type}
          </p>

          <p>
            <strong>Status:</strong> {task.status}
          </p>

          <p>
            <strong>Difficulty:</strong> {task.difficulty}/5
          </p>

          <p>
            <strong>Start:</strong> {task.startDate.toLocaleString()}
          </p>

          <p>
            <strong>End:</strong> {task.endDate.toLocaleString()}
          </p>

          {task.description && (
            <p>
              <strong>Description:</strong> {task.description}
            </p>
          )}
        </div>

        {/* BUTTONS */}
        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={() => {
              onClose();        // închide detaliile
              onEdit(task);     // deschide edit modal
            }}
            className="px-5 py-2 rounded-lg font-semibold text-white"
            style={{
              background: "#c27045",
              border: "2px solid #a55a2b",
            }}
          >
            ✏ Edit
          </button>

          <button
            onClick={() => onDelete(task.id)}
            className="px-5 py-2 rounded-lg font-semibold text-white"
            style={{
              background: "#c24848",
              border: "2px solid #a33636",
            }}
          >
            🗑 Delete
          </button>

          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg font-semibold"
            style={{
              background: "#fff",
              border: "2px solid #caaea1",
              color: "#7a3e25",
            }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
