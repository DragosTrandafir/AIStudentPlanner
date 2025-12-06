export type TaskStatus = "Pending" | "In Progress" | "Completed";
export type TaskType = "Assignment" | "Project" | "Practical Exam" | "Written Exam";

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
}
