"use client";

import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Task, TaskType, TaskStatus } from "@/types/Task";
import "@/styles/date_picker.css";
import {
  createSubject,
  updateSubject,
  SubjectCreatePayload
} from "@/lib/apiSubjects";
import { mapSubjectToTask } from "@/utils/subjectMapper";



interface Props {
  existingTask?: Task | null;
  onClose: () => void;
  onSave: (task: Task) => void;
}

export default function AddTaskModal({ existingTask, onClose, onSave }: Props) {
  const [form, setForm] = useState<Task>(() => {
    if (existingTask) return existingTask;

    const now = new Date();
    const oneHourLater = new Date(now.getTime() + 60 * 60 * 1000);


    return {
      id: Date.now(),
      title: "",
      subject: "",
      type: "Project",
      difficulty: 1,
      description: "",
      status: "Pending",
      startDate: now,
      endDate: oneHourLater,
      color: "#F4C2C2",
    };

  });
  
   async function save() {
    if (!form.title.trim()) {
      alert("Please enter a task title");
      return;
    }

    let mappedType: SubjectCreatePayload["type"];
    if (form.type === "Written Exam") mappedType = "written";
    else if (form.type === "Practical Exam") mappedType = "practical";
    else mappedType = "project";

    let mappedStatus: SubjectCreatePayload["status"];
    if (form.status === "In Progress") mappedStatus = "in_progress";
    else if (form.status === "Completed") mappedStatus = "completed";
    else mappedStatus = "not_started";

    const payload: SubjectCreatePayload = {
      title: form.title,
      name: form.subject || "",
      type: mappedType,
      status: mappedStatus,
      difficulty: form.difficulty,
      start_date: form.startDate.toISOString(),
      end_date: form.endDate.toISOString(),
      description: form.description || "",
    };

    try {
      const backendSubject = existingTask
        ? await updateSubject(existingTask.id, payload)
        : await createSubject(payload);

      const updatedTask = mapSubjectToTask(backendSubject);

      onSave(updatedTask);
      onClose();
    } catch (err) {
      console.error(err);
      alert("Failed to save task.");
    }
  }




  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex justify-end"
      onClick={onClose}
    >
      <div
        className="h-full w-[560px] shadow-2xl flex flex-col animate-slideIn"
        style={{
          background: "var(--surface-1)",
          color: "var(--text-main)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* HEADER */}
        <div
          className="p-5 flex justify-between items-center"
          style={{ borderBottom: "1px solid var(--border-main)" }}
        >
          <h2 className="text-xl font-bold">{existingTask ? "Edit Task" : "Add New Task"}</h2>

          <button
            onClick={onClose}
            className="text-xl font-bold opacity-60 hover:opacity-100"
            style={{ color: "var(--text-main)" }}
          >
            ✕
          </button>
        </div>

        {/* CONTENT */}
        <div className="p-6 overflow-y-auto space-y-6">

          {/* TITLE & SUBJECT */}
          <div className="space-y-4">
            <div>
              <label className="font-semibold mb-1 block">Title *</label>
              <input
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                className="rounded-lg px-3 py-2 w-full"
                style={{
                  background: "var(--surface-2)",
                  color: "var(--text-main)",
                  border: "1px solid var(--border-main)",
                }}
              />
            </div>

            <div>
              <label className="font-semibold mb-1 block">Subject</label>
              <input
                value={form.subject}
                onChange={(e) => setForm({ ...form, subject: e.target.value })}
                className="rounded-lg px-3 py-2 w-full"
                style={{
                  background: "var(--surface-2)",
                  color: "var(--text-main)",
                  border: "1px solid var(--border-main)",
                }}
              />
            </div>
          </div>

          {/* DESCRIPTION + PROPERTIES */}
          <div className="grid grid-cols-2 gap-6">
            {/* DESCRIPTION */}
            <div>
              <label className="font-semibold mb-1 block">Description</label>
              <textarea
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                rows={10}
                className="rounded-lg px-3 py-2 w-full"
                style={{
                  background: "var(--surface-2)",
                  color: "var(--text-main)",
                  border: "1px solid var(--border-main)",
                }}
              />
            </div>

            {/* PROPERTIES */}
            <div className="space-y-4">

              {/* TYPE */}
              <div>
                <label className="font-semibold mb-1 block">Subject Type</label>
                <select
                  value={form.type}
                  onChange={(e) => setForm({ ...form, type: e.target.value as TaskType })}
                  className="rounded-lg px-3 py-2 w-full"
                  style={{
                    background: "var(--surface-2)",
                    color: "var(--text-main)",
                    border: "1px solid var(--border-main)",
                  }}
                >
                  <option>Project</option>
                  <option>Practical Exam</option>
                  <option>Written Exam</option>
                </select>
              </div>

              {/* STATUS */}
              <div>
                <label className="font-semibold mb-1 block">Status</label>
                <select
                  value={form.status}
                  onChange={(e) => setForm({ ...form, status: e.target.value as TaskStatus })}
                  className="rounded-lg px-3 py-2 w-full"
                  style={{
                    background: "var(--surface-2)",
                    color: "var(--text-main)",
                    border: "1px solid var(--border-main)",
                  }}
                >
                  <option>Pending</option>
                  <option>In Progress</option>
                  <option>Completed</option>
                </select>
              </div>

              {/* DIFFICULTY */}
              <div>
                <label className="font-semibold mb-1 block">Difficulty (1–5)</label>
                <input
                  type="number"
                  min={1}
                  max={5}
                  value={form.difficulty}
                  onChange={(e) => setForm({ ...form, difficulty: Number(e.target.value) })}
                  className="rounded-lg px-3 py-2 w-full"
                  style={{
                    background: "var(--surface-2)",
                    color: "var(--text-main)",
                    border: "1px solid var(--border-main)",
                  }}
                />
              </div>
            </div>
          </div>

          {/* DATES */}
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="font-semibold mb-1 block">Start Date</label>
              <DatePicker
                selected={form.startDate}
                onChange={(date) => setForm({ ...form, startDate: date as Date })}
                showTimeSelect
                dateFormat="MMM d, yyyy h:mm aa"
                className="datepicker-input"
              />

            </div>

            <div>
              <label className="font-semibold mb-1 block">End Date</label>
              <DatePicker
                selected={form.endDate}
                onChange={(date) => setForm({ ...form, endDate: date as Date })}
                showTimeSelect
                dateFormat="MMM d, yyyy h:mm aa"
                className="datepicker-input"
              />

            </div>
          </div>
        </div>

        {/* FOOTER */}
        <div
          className="p-5 flex justify-end gap-3"
          style={{ borderTop: "1px solid var(--border-main)" }}
        >
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg"
            style={{
              background: "var(--surface-2)",
              color: "var(--text-main)",
              border: "1px solid var(--border-main)",
            }}
          >
            Cancel
          </button>

          <button
            onClick={save}
            className="px-5 py-2 rounded-lg"
            style={{
              background: "var(--accent)",
              color: "var(--text-on-accent)",
            }}
          >
            Save Task
          </button>
        </div>
      </div>

      <style jsx>{`
        @keyframes slideIn {
          from {
            transform: translateX(100%);
          }
          to {
            transform: translateX(0);
          }
        }
        .animate-slideIn {
          animation: slideIn 0.25s ease-out;
        }
      `}</style>
    </div>
  );
}
