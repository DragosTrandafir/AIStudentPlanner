export interface SubjectResponse {
  id: number;
  student_id: number;
  title: string;
  name: string;
  type: "written" | "practical" | "project";
  status: "not_started" | "in_progress" | "completed";
  difficulty: number;
  start_date: string;
  end_date: string;
  description?: string | null;
}
