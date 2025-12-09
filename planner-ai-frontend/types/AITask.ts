export interface AITask {
  id: string;
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

