"use client";

import React from "react";

export interface MiniMonthViewProps {
  selectedMonth: Date;
  onSelect: (date: Date) => void;
}

export default function MiniMonthView({ selectedMonth, onSelect }: MiniMonthViewProps) {
  const year = selectedMonth.getFullYear();
  const month = selectedMonth.getMonth();

  // Fix Monday-first
  const jsFirst = new Date(year, month, 1).getDay(); // 0 = Sunday
  const firstDay = (jsFirst + 6) % 7; // shift so Monday = 0

  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const cells: Array<number | null> = [];
  for (let i = 0; i < firstDay; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);

  const dayHeaders = [
    { key: "Mon", label: "M" },
    { key: "Tue", label: "T" },
    { key: "Wed", label: "W" },
    { key: "Thu", label: "T" },
    { key: "Fri", label: "F" },
    { key: "Sat", label: "S" },
    { key: "Sun", label: "S" },
  ];

  return (
    <div className="mini-cal">
      <div className="mini-cal-month">
        {selectedMonth.toLocaleString("default", { month: "long", year: "numeric" })}
      </div>

      <div className="mini-cal-grid">
        {dayHeaders.map((h) => (
          <div key={h.key} className="mini-cal-day-header">
            {h.label}
          </div>
        ))}

        {cells.map((c, i) => (
          <div
            key={i}
            className={`mini-cal-day ${c ? "" : "muted"}`}
            onClick={() => c && onSelect(new Date(year, month, c))}
          >
            {c || ""}
          </div>
        ))}
      </div>
    </div>
  );
}
