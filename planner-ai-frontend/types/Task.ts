export type TaskStatus = "Pending" | "In Progress" | "Completed";
export type TaskType = "Assignment" | "Project" | "Practical Exam" | "Written Exam" | "AI Study Task";

export interface Task {
  id: number;
  title: string;
  subject?: string;
  type: TaskType;
  difficulty?: number;
  description?: string;
  status?: TaskStatus;
  startDate: Date;
  endDate: Date;
  color?: string;

  // AI Task specific fields
  isAiTask?: boolean;
  planId?: number;
  aiTaskId?: number;
  priority?: number;
}
