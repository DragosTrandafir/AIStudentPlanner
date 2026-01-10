"use client";

import React from "react";
import { Task } from "@/types/Task";
import "@/styles/task_details.css";

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
    <div className="taskdetails-backdrop" onClick={onClose}>
      <div className="taskdetails-panel" onClick={(e) => e.stopPropagation()}>
        
        {/* HEADER */}
        <div className="taskdetails-header">
          <h2 className="taskdetails-title">📋 Task Details</h2>
          <button className="taskdetails-close" onClick={onClose}>✕</button>
        </div>

        {/* CONTENT */}
        <div className="taskdetails-content">

          <div className="taskdetails-row">
            <span className="taskdetails-label">Title:</span>
            <span className="taskdetails-value">{task.title}</span>
          </div>

          <div className="taskdetails-row">
            <span className="taskdetails-label">Subject:</span>
            <span className="taskdetails-value">{task.subject || "—"}</span>
          </div>

          <div className="taskdetails-row">
            <span className="taskdetails-label">Type:</span>
            <span className="taskdetails-tag">{task.type}</span>
          </div>

          <div className="taskdetails-row">
            <span className="taskdetails-label">Status:</span>
            <span className="taskdetails-tag">{task.status}</span>
          </div>

          <div className="taskdetails-row">
            <span className="taskdetails-label">Difficulty:</span>
            <span className="taskdetails-tag">{task.difficulty}/5</span>
          </div>

          <div className="taskdetails-divider"></div>

          <div className="taskdetails-row">
            <span className="taskdetails-label">Start:</span>
            <span className="taskdetails-value">
              {new Date(task.startDate).toLocaleString()}
            </span>
          </div>

          <div className="taskdetails-row">
            <span className="taskdetails-label">End:</span>
            <span className="taskdetails-value">
              {new Date(task.endDate).toLocaleString()}
            </span>
          </div>

          {/* Show priority for AI tasks */}
          {task.isAiTask && task.priority && (
            <div className="taskdetails-row">
              <span className="taskdetails-label">Priority:</span>
              <span className="taskdetails-tag">{task.priority}/10</span>
            </div>
          )}

          {/* AI Task indicator */}
          {task.isAiTask && (
            <div className="taskdetails-ai-badge">
              🤖 AI Generated Study Task
            </div>
          )}
        </div>

        {/* FOOTER BUTTONS */}
        <div className="taskdetails-footer">
          {/* Only show Edit button for non-AI tasks */}
          {!task.isAiTask && (
            <button
              className="taskdetails-btn edit"
              onClick={() => {
                onClose();
                onEdit(task);
              }}
            >
              ✏ Edit
            </button>
          )}

          <button
            className="taskdetails-btn delete"
            onClick={() => onDelete(task.id)}
          >
            🗑 Delete
          </button>

          <button className="taskdetails-btn close" onClick={onClose}>
            Close
          </button>
        </div>

      </div>
    </div>
  );
}
