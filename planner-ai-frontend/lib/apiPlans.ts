import { USER_ID } from "./apiSubjects";

const BASE_URL = "http://localhost:8000";

export interface AITaskEntry {
  id?: number;  // AI task database ID
  time_allotted: string;
  ai_task_name: string;
  task_name: string;  // subject name
  difficulty: number;
  priority: number;
}

export interface PlanResponse {
  id?: number;  // Plan database ID
  plan_date: string;
  entries: AITaskEntry[];
  notes: string | null;
}

export interface GeneratedPlanResponse {
  plans: PlanResponse[];
  message: string;
}

/**
 * Generate an AI plan for the user based on their subjects.
 * This calls the AI orchestrator to create study tasks.
 */
export async function generatePlan(): Promise<GeneratedPlanResponse> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to generate plan: " + msg);
  }

  return res.json();
}

/**
 * Get all plans for the user.
 */
export async function getPlans(): Promise<PlanResponse[]> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans`);

  if (!res.ok) {
    throw new Error("Failed to load plans");
  }

  return res.json();
}

/**
 * Get the latest plan for the user.
 */
export async function getLatestPlan(): Promise<PlanResponse> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/latest`);

  if (!res.ok) {
    throw new Error("Failed to load latest plan");
  }

  return res.json();
}

/**
 * Get the latest schedule (all plans from the latest generation).
 */
export async function getLatestSchedule(): Promise<PlanResponse[]> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/latest-schedule`);

  if (!res.ok) {
    throw new Error("Failed to load latest schedule");
  }

  return res.json();
}

/**
 * Get plan history for the user.
 */
export async function getPlanHistory(): Promise<PlanResponse[]> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/history`);

  if (!res.ok) {
    throw new Error("Failed to load plan history");
  }

  return res.json();
}

/**
 * Delete an AI task from a plan.
 */
export async function deleteAiTask(planId: number, aiTaskId: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/plans/${planId}/ai-tasks/${aiTaskId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to delete AI task: " + msg);
  }
}

/**
 * Delete an entire plan.
 */
export async function deletePlan(planId: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/${planId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to delete plan: " + msg);
  }
}

/**
 * Submit feedback for a specific plan.
 */
export async function submitFeedback(
  planId: number,
  rating: number,
  comments: string
): Promise<void> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      plan_id: planId,
      rating,
      comments,
    }),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to submit feedback: " + msg);
  }
}

/**
 * Reschedule a plan based on current and last feedback.
 */
export async function reschedulePlan(): Promise<GeneratedPlanResponse> {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/reschedule`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to reschedule plan: " + msg);
  }

  return res.json();
}