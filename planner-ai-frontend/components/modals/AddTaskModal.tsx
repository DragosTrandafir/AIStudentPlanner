"use client";

import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Task, TaskType, TaskStatus } from "@/types/Task";

interface Props {
  existingTask?: Task | null;
  onClose: () => void;
  onSave: (task: Task) => void;
}

export default function AddTaskModal({ existingTask, onClose, onSave }: Props) {
  const now = new Date();
  const oneHourLater = new Date(now.getTime() + 60 * 60 * 1000);

  const [form, setForm] = useState<Task>(
    existingTask || {
      id: Date.now(),
      title: "",
      subject: "",
      type: "Assignment",
      difficulty: 1,
      description: "",
      status: "Pending",
      startDate: now,
      endDate: oneHourLater,
      color: "#F4C2C2",
    }
  );

  function save() {
    if (!form.title.trim()) return alert("Please enter a task title");
    onSave({ ...form });
    onClose(); // închide modalul după save
  }

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
          width: "600px",
          maxHeight: "100vh",
          overflowY: "auto",
          background: "linear-gradient(to bottom, #ffe8d9, #fff4e7)",
          border: "5px solid #e4b6a4",
        }}
      >
        <h2
          className="text-center mb-6 font-bold"
          style={{ fontSize: "22px", color: "#7a3e25" }}
        >
          ✨ {existingTask ? "Edit Task" : "Add New Task"}
        </h2>

        {/* Title */}
        <div className="mb-4">
          <label className="text-sm font-semibold text-[#6b3b28]">
            Task Title *
          </label>
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full mt-1 px-3 py-2 rounded-lg text-black"
            style={{
              border: "2px solid #e0c4b3",
              background: "white",
            }}
          />
        </div>

        {/* Subject */}
        <div className="mb-4">
          <label className="text-sm font-semibold text-[#6b3b28]">
            Subject / Project
          </label>
          <input
            value={form.subject}
            onChange={(e) => setForm({ ...form, subject: e.target.value })}
            className="w-full mt-1 px-3 py-2 rounded-lg text-black"
            style={{
              border: "2px solid #e0c4b3",
              background: "white",
            }}
          />
        </div>

        {/* Task Type */}
        <div className="mb-4">
          <label className="text-sm font-semibold text-[#6b3b28]">
            Task Type
          </label>
          <select
            value={form.type}
            onChange={(e) =>
              setForm({ ...form, type: e.target.value as TaskType })
            }
            className="w-full mt-1 px-3 py-2 rounded-lg text-black"
            style={{ border: "2px solid #e0c4b3", background: "white" }}
          >
            <option>Assignment</option>
            <option>Project</option>
            <option>Practical Exam</option>
            <option>Written Exam</option>
          </select>
        </div>

        {/* Schedule */}
        <div
          className="rounded-2xl p-4 mb-4"
          style={{
            border: "2px solid #e4b6a4",
            background: "#ffe1da",
          }}
        >
          <p className="font-semibold mb-2 flex items-center gap-2 text-[#7a3e25]">
            📅 Schedule
          </p>

          <div className="grid grid-cols-2 gap-4">
            {/* Start */}
            <div>
              <label className="text-xs font-semibold text-[#6b3b28]">
                Start
              </label>
              <DatePicker
                selected={form.startDate}
                onChange={(date) =>
                  setForm({
                    ...form,
                    startDate: date as Date,
                    endDate:
                      (date as Date) > form.endDate
                        ? (date as Date)
                        : form.endDate,
                  })
                }
                showTimeSelect
                dateFormat="MMM d, yyyy h:mm aa"
                className="w-full mt-1 px-3 py-2 rounded-lg border-2 border-[#e0c4b3] bg-white text-black"
              />
            </div>

            {/* End */}
            <div>
              <label className="text-xs font-semibold text-[#6b3b28]">
                End
              </label>
              <DatePicker
                selected={form.endDate}
                onChange={(date) =>
                  setForm({
                    ...form,
                    endDate: date as Date,
                  })
                }
                showTimeSelect
                dateFormat="MMM d, yyyy h:mm aa"
                className="w-full mt-1 px-3 py-2 rounded-lg border-2 border-[#e0c4b3] bg-white text-black"
              />
            </div>
          </div>
        </div>

        {/* Difficulty */}
        <div className="mb-4">
          <label className="text-sm font-semibold text-[#6b3b28]">
            Difficulty (1–5)
          </label>
          <input
            type="number"
            min={1}
            max={5}
            value={form.difficulty}
            onChange={(e) =>
              setForm({ ...form, difficulty: Number(e.target.value) })
            }
            className="w-full mt-1 px-3 py-2 rounded-lg text-black"
            style={{
              border: "2px solid #e0c4b3",
              background: "white",
            }}
          />
        </div>

        {/* Description */}
        <div className="mb-4">
          <label className="text-sm font-semibold text-[#6b3b28]">
            Description
          </label>
          <textarea
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
            className="w-full mt-1 px-3 py-2 rounded-lg text-black"
            rows={3}
            style={{
              border: "2px solid #e0c4b3",
              background: "white",
            }}
          />
        </div>

        {/* Status */}
        <div className="mb-6">
          <label className="text-sm font-semibold text-[#6b3b28]">
            Status
          </label>
          <select
            value={form.status}
            onChange={(e) =>
              setForm({ ...form, status: e.target.value as TaskStatus })
            }
            className="w-full mt-1 px-3 py-2 rounded-lg text-black"
            style={{
              border: "2px solid #e0c4b3",
              background: "white",
            }}
          >
            <option>Pending</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg font-semibold"
            style={{
              background: "#fff",
              border: "2px solid #caaea1",
              color: "#7a3e25",
            }}
          >
            Cancel
          </button>

          <button
            onClick={save}
            className="px-5 py-2 rounded-lg font-semibold text-white"
            style={{
              background: "#c05b74",
              border: "2px solid #a5455c",
            }}
          >
            Save Task
          </button>
        </div>
      </div>
    </div>
  );
}
