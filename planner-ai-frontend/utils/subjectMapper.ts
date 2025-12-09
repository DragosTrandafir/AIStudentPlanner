import { SubjectResponse } from "@/types/SubjectResponse";
import { Task } from "@/types/Task";

export function backendTypeToUiType(type: string): Task["type"] {
  switch (type) {
    case "written":
      return "Written Exam";
    case "practical":
      return "Practical Exam";
    case "project":
      return "Project";
    default:
      return "Project";
  }
}

export function backendStatusToUiStatus(status: string): Task["status"] {
  switch (status) {
    case "not_started":
      return "Pending";
    case "in_progress":
      return "In Progress";
    case "completed":
      return "Completed";
    default:
      return "Pending";
  }
}

export function mapSubjectToTask(subject: SubjectResponse): Task {
  return {
    id: subject.id,
    title: subject.title,
    subject: subject.name,
    type: backendTypeToUiType(subject.type),
    difficulty: subject.difficulty ?? 1,
    description: subject.description ?? "",
    status: backendStatusToUiStatus(subject.status),
    startDate: new Date(subject.start_date),
    endDate: new Date(subject.end_date),
    color: "#F4C2C2",
  };
}