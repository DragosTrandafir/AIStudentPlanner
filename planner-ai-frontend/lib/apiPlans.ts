import { getAuthHeaders, getCurrentUserId } from "@/utils/apiUtils";

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
  generation_id?: string;  // UUID for schedule/generation grouping
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
  const USER_ID = getCurrentUserId();
  try {
    const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/generate`, {
      method: "POST",
      headers: getAuthHeaders(),
    });

    if (!res.ok) {
      const msg = await res.text();
      console.log(`[generatePlan] HTTP ${res.status}: ${msg}`);
    }

    return res.json();
  } catch (error) {
    console.log("[generatePlan] Error:", error);
    throw error;
  }
}

/**
 * Get all plans for the user.
 */
export async function getPlans(): Promise<PlanResponse[]> {
  const USER_ID = getCurrentUserId();
  try {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans`, {
      method: "GET",
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      throw new Error("Failed to load plans");
    }

    return res.json();
  } catch (error) {
    console.log("[getPlans] Error:", error);
    throw error;
  }
}

/**
 * Get the latest plan for the user.
 */
export async function getLatestPlan(): Promise<PlanResponse> {
  const USER_ID = getCurrentUserId();
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/latest`, {
      headers: getAuthHeaders()
  });
  if (!res.ok) {
    throw new Error("Failed to load latest plan");
  }

  return res.json();
}

/**
 * Get the latest schedule (all plans from the latest generation).
 */
export async function getLatestSchedule(): Promise<PlanResponse[]> {
  const USER_ID = getCurrentUserId();
  try {
    const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/latest-schedule`,
        {headers: getAuthHeaders()});

    if (!res.ok) {
      console.log(`[getLatestSchedule] HTTP ${res.status}`);
    }

    return res.json();
  } catch (error) {
    console.log("[getLatestSchedule] Error:", error);
    throw error;
  }
}

/**
 * Get plan history for the user.
 */
export async function getPlanHistory(): Promise<PlanResponse[]> {
  const USER_ID = getCurrentUserId();
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/history`,
        {headers: getAuthHeaders()});

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
    headers: getAuthHeaders()
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
  const USER_ID = getCurrentUserId();
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/${planId}`, {
    method: "DELETE",
    headers: getAuthHeaders()
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to delete plan: " + msg);
  }
}

/**
 * Submit feedback for a schedule/generation.
 * Can provide either generation_id or plan_id.
 */
export async function submitFeedback(
  rating: number,
  comments: string,
  generationId?: string,
  planId?: number
): Promise<void> {
  const USER_ID = getCurrentUserId();
  try {
    const res = await fetch(`${BASE_URL}/users/${USER_ID}/feedback`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        generation_id: generationId,
        plan_id: planId,
        rating,
        comments,
      }),
    });

    if (!res.ok) {
      const msg = await res.text();
      console.log(`[submitFeedback] HTTP ${res.status}: ${msg}`);
      throw new Error("Failed to submit feedback: " + msg);
    }
  } catch (error) {
    console.log("[submitFeedback] Error:", error);
    throw error;
  }
}

/**
 * Reschedule a plan based on current and last feedback.
 */
export async function reschedulePlan(): Promise<GeneratedPlanResponse> {
  const USER_ID = getCurrentUserId();
  try {
    const res = await fetch(`${BASE_URL}/users/${USER_ID}/plans/reschedule`, {
      method: "POST",
      headers: getAuthHeaders(),
    });

    if (!res.ok) {
      const msg = await res.text();
      console.log(`[reschedulePlan] HTTP ${res.status}: ${msg}`);
      throw new Error("Failed to reschedule plan: " + msg);
    }

    return res.json();
  } catch (error) {
    console.log("[reschedulePlan] Error:", error);
    throw error;
  }
}