"use client";

export default function TaskDetailsModal({ task, onClose, onEdit, onDelete }) {
  if (!task) return null;

  const accentColor = "#8a0f5d"; // same accent as AddTaskModal
  const typeColors = {
    project: "#F3E5AB",
    written: "#AFEEEE",
    practical: "#98FB98",
  };
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

  //  Confirm deletion before removing a task
  const handleDelete = () => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete the task "${task.title}"?`
    );
    if (confirmDelete) {
      onDelete(task.id);
      onClose();
    }
  };

  const start = task.start_date || task.startDate;
  const end = task.end_date || task.endDate;

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
        {/* Header */}
        <h2
          className="text-xl font-bold text-center mb-4"
          style={{ color: accentColor }}
        >
          📋 Task Details
        </h2>

        {/* Content */}
        <div className="space-y-2 text-sm">
          <Detail label="Title" value={task.title} accentColor={accentColor} />
          <Detail
            label="Subject / Project"
            value={task.name || task.subject || "—"}
            accentColor={accentColor}
          />

          {/* Type */}
          <div>
            <label
              className="block text-sm mb-1"
              style={{ color: accentColor }}
            >
              Type
            </label>
            <div
              className="px-2 py-1 rounded-lg text-sm font-semibold inline-block"
              style={{
                backgroundColor: typeColors[task.type] || "#fff8f5",
                color: accentColor,
                border: `1px solid ${accentColor}`,
              }}
            >
              {typeLabels[task.type] || task.type}
            </div>
          </div>

          <Detail label="Status" value={statusLabels[task.status] || task.status} accentColor={accentColor} />
          <Detail
            label="Difficulty"
            value={`${task.difficulty}/5`}
            accentColor={accentColor}
          />
          <Detail
            label="Start"
            value={start ? new Date(start).toLocaleString() : "—"}
            accentColor={accentColor}
          />
          <Detail
            label="End"
            value={end ? new Date(end).toLocaleString() : "—"}
            accentColor={accentColor}
          />

          {task.description && (
            <Detail
              label="Description"
              value={task.description}
              accentColor={accentColor}
              extraClasses="whitespace-pre-line"
            />
          )}
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-2 mt-4">
          <button
            onClick={() => onEdit(task)}
            className="px-3 py-1 text-sm rounded-lg font-semibold transition-all active:translate-y-[1px]"
            style={{
              backgroundColor: "#fcd2e0",
              color: accentColor,
              border: `1px solid ${accentColor}`,
            }}
          >
            ✏ Edit
          </button>

          {/* 🔥 Crimson Delete Button */}
          <button
            onClick={handleDelete}
            className="px-3 py-1 text-sm rounded-lg font-semibold transition-all active:translate-y-[1px] text-white"
            style={{
              backgroundColor: "#dc143c", // Crimson
              border: "1px solid #b01030",
            }}
          >
            🗑 Delete
          </button>

          <button
            onClick={onClose}
            className="px-3 py-1 text-sm rounded-lg font-semibold transition-all active:translate-y-[1px]"
            style={{
              backgroundColor: accentColor,
              color: "#fff",
              border: `1px solid ${accentColor}`,
            }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

/* Small helper component */
function Detail({ label, value, accentColor, extraClasses = "" }) {
  return (
    <div>
      <label className="block text-sm mb-1" style={{ color: accentColor }}>
        {label}
      </label>
      <div
        className={`px-2 py-1 rounded-lg text-sm ${extraClasses}`}
        style={{
          backgroundColor: "#fff8f5",
          color: accentColor,
          border: `1px solid ${accentColor}`,
          wordBreak: "break-word",
        }}
      >
        {value}
      </div>
    </div>
  );
}
