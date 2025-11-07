"use client";

export default function TaskDetailsModal({ task, onClose, onEdit, onDelete }) {
  if (!task) return null;

  const labelColors = {
    Assignment: "bg-[#F4C2C2] text-[#3B2F2F]",
    Project: "bg-[#F3E5AB] text-[#3B2F2F]",
    "Written Exam": "bg-[#AFEEEE] text-[#3B2F2F]",
    "Practical Exam": "bg-[#98FB98] text-[#3B2F2F]",
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-3">
      <div
        className="w-full max-w-lg p-8 rounded-3xl shadow-2xl border border-amber-300"
        style={{ backgroundColor: "#3B2F2F", color: "#FAEBD7" }}
      >
        {/* Header */}
        <div className="text-center mb-3">
          <h2 className="text-3xl font-bold text-amber-200 drop-shadow-md">
            📋 Task Details
          </h2>
          <p className="text-sm text-amber-100 opacity-80">
            Review all information about your task below.
          </p>
        </div>

        {/* Task Content */}
        <div className="space-y-4 mt-4">
          <div>
            <span className="block text-sm text-amber-100 mb-1">Title</span>
            <div className="p-2 rounded-lg bg-[#5A4B3C] text-white">
              {task.title}
            </div>
          </div>

          <div>
            <span className="block text-sm text-amber-100 mb-1">
              Subject / Project
            </span>
            <div className="p-2 rounded-lg bg-[#5A4B3C] text-white">
              {task.subject || "—"}
            </div>
          </div>

          <div>
            <span className="block text-sm text-amber-100 mb-1">Type</span>
            <div
              className={`inline-block px-3 py-1 rounded-lg font-semibold text-sm ${
                labelColors[task.type] || ""
              }`}
            >
              {task.type}
            </div>
          </div>

          <div>
            <span className="block text-sm text-amber-100 mb-1">Status</span>
            <div className="p-2 rounded-lg bg-[#5A4B3C] text-white">
              {task.status}
            </div>
          </div>

          <div>
            <span className="block text-sm text-amber-100 mb-1">Difficulty</span>
            <div className="p-2 rounded-lg bg-[#5A4B3C] text-white">
              {task.difficulty}/5
            </div>
          </div>

          <div>
            <span className="block text-sm text-amber-100 mb-1">Start</span>
            <div className="p-2 rounded-lg bg-[#5A4B3C] text-white">
              {new Date(task.startDate).toLocaleString()}
            </div>
          </div>

          <div>
            <span className="block text-sm text-amber-100 mb-1">End</span>
            <div className="p-2 rounded-lg bg-[#5A4B3C] text-white">
              {new Date(task.endDate).toLocaleString()}
            </div>
          </div>

          {task.description && (
            <div>
              <span className="block text-sm text-amber-100 mb-1">
                Description
              </span>
              <div className="p-2 rounded-lg bg-[#5A4B3C] text-white whitespace-pre-line">
                {task.description}
              </div>
            </div>
          )}
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-3 mt-8">
          <button
            onClick={() => onEdit(task)}
            className="px-4 py-2 bg-amber-400 text-brown-900 font-semibold rounded-lg hover:bg-amber-300"
          >
            ✏ Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="px-4 py-2 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600"
          >
            🗑 Delete
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
