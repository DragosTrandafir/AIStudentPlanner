"use client";

interface MiniMonthViewProps {
  selectedMonth: Date;
  selectedDate: Date | null;
  onSelect: (date: Date) => void;
}

export default function MiniMonthView({
  selectedMonth,
  selectedDate,
  onSelect,
}: MiniMonthViewProps) {
  const year = selectedMonth.getFullYear();
  const month = selectedMonth.getMonth();

  const jsFirstDay = new Date(year, month, 1).getDay();
  const firstDay = (jsFirstDay + 6) % 7;
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const cells: Array<number | null> = [];
  for (let i = 0; i < firstDay; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);

  const today = new Date();

  const isToday = (day: number | null) =>
    !!day &&
    today.getFullYear() === year &&
    today.getMonth() === month &&
    today.getDate() === day;

  const isSelected = (day: number | null) =>
    !!day &&
    selectedDate &&
    selectedDate.getFullYear() === year &&
    selectedDate.getMonth() === month &&
    selectedDate.getDate() === day;

  const monthLabel = selectedMonth.toLocaleString("default", {
    month: "long",
    year: "numeric",
  });

  return (
    <div
      className="p-4 rounded-xl shadow-md mini-calendar-container"
      style={{
        width: "220px",
        background: "var(--mini-bg)",
        border: "1px solid var(--mini-border)",
      }}
    >
      {/* HEADER */}
      <div
        className="flex justify-between items-center mb-2 font-semibold"
        style={{ color: "var(--text-main)" }}
      >
        <button
          onClick={() => onSelect(new Date(year, month - 1, 1))}
          style={{ color: "var(--text-main)" }}
        >
          ‹
        </button>
        <span>{monthLabel}</span>
        <button
          onClick={() => onSelect(new Date(year, month + 1, 1))}
          style={{ color: "var(--text-main)" }}
        >
          ›
        </button>
      </div>

      {/* WEEKDAYS */}
      <div
        className="grid grid-cols-7 text-center text-xs font-semibold mb-1"
        style={{ color: "var(--text-secondary)" }}
      >
        {["M", "T", "W", "T", "F", "S", "S"].map((d, i) => (
          <div key={i}>{d}</div>
        ))}
      </div>

      {/* DAYS */}
      <div className="grid grid-cols-7 text-center text-sm">
        {cells.map((day, i) => {
          const isCurrent = isToday(day);
          const selected = isSelected(day);

          let bg = "transparent";
          let color = "var(--text-main)";

          if (isCurrent) {
            bg = "var(--accent)"; // today
            color = "var(--text-on-accent)";
          }

          if (selected) {
            bg = "var(--mini-selected)"; // selected
            color = "var(--text-on-accent)";
          }

          return (
            <div
              key={i}
              onClick={() => day && onSelect(new Date(year, month, day))}
              className="mini-day"
              style={{
                opacity: day ? 1 : 0.25,
                background: bg,
                color,
                fontWeight: isCurrent || selected ? "700" : "500",
                padding: "6px 0",
                borderRadius: "10px",
                cursor: day ? "pointer" : "default",
                margin: "2px",
              }}
            >
              {day || ""}
            </div>
          );
        })}
      </div>
    </div>
  );
}
