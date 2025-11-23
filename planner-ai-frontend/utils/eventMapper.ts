// /utils/eventMapper.ts

export type TaskType =
  | "Assignment"
  | "Project"
  | "Written Exam"
  | "Practical Exam";

export interface Task {
  id: string;
  title: string;
  type: TaskType;
  startDate: string | Date;
  endDate: string | Date;
  description?: string;
  color?: string;
}

export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  allDay: boolean;
  backgroundColor: string;
  borderColor: string;
  extendedProps: Task & { color: string };
}

export const typeColors: Record<TaskType, string> = {
  Assignment: "#F4C2C2",
  Project: "#F3E5AB",
  "Written Exam": "#AFEEEE",
  "Practical Exam": "#98FB98",
};

export function mapTaskToEvent(task: Task): CalendarEvent {
  const color = task.color || typeColors[task.type] || "#ccc";

  return {
    id: task.id,
    title: task.title,
    start: new Date(task.startDate),
    end: new Date(task.endDate),
    allDay: true,
    backgroundColor: color,
    borderColor: color,
    extendedProps: {
      ...task,
      color,
    },
  };
}
