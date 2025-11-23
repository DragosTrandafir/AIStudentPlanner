"use client";

import ArrowCalendarButton from "@/components/buttons/ArrowCalendarButton";
import TodayButton from "@/components/buttons/TodayButton";
import AddTaskButton from "@/components/buttons/AddTaskButton";

interface CalendarHeaderProps {
  currentMonth: Date;
  onPrev: () => void;
  onNext: () => void;
  onToday: () => void;
}

export default function CalendarHeader({
  currentMonth,
  onPrev,
  onNext,
  onToday,
}: CalendarHeaderProps) {
  const monthName = currentMonth.toLocaleString("default", { month: "long" });
  const year = currentMonth.getFullYear();

  return (
    <div className="calendar-header">
      <div className="header-left">
        <h2>{monthName} {year}</h2>
        <AddTaskButton onClick={() => console.log("open modal")}>
          + Add Task
        </AddTaskButton>
      </div>

      <div className="header-right">
        <ArrowCalendarButton direction="left" onClick={onPrev} />
        <TodayButton onClick={onToday}>Today</TodayButton>
        <ArrowCalendarButton direction="right" onClick={onNext} />
      </div>
    </div>
  );
}
