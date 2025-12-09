export interface AITask {
  id: string;
  db_id?: number;  // Database ID for deletion
  plan_id?: number;  // Plan ID for deletion
  time_allotted: string;
  ai_task_name: string;
  subject_name: string;
  difficulty: number;
  priority: number;
  date: Date;
  color?: string;
}

export interface Plan {
  plan_date: string;
  entries: AITask[];
  notes: string | null;
}

