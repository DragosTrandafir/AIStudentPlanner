import { Task } from "@/types/Task";
import { PlanResponse, AITaskEntry } from "@/lib/apiPlans";

/**
 * Parse time string like "18:00–20:00" or "18:00-20:00" into hours and minutes
 */
function parseTimeRange(timeAllotted: string): { startHour: number; startMin: number; endHour: number; endMin: number } {
  // Handle different dash characters (en-dash, em-dash, hyphen)
  const normalized = timeAllotted.replace(/[–—]/g, "-");
  const parts = normalized.split("-");

  if (parts.length !== 2) {
    // Default to 9:00-10:00 if parsing fails
    return { startHour: 9, startMin: 0, endHour: 10, endMin: 0 };
  }

  const parseTime = (time: string) => {
    const [hours, minutes] = time.trim().split(":").map(Number);
    return { hours: hours || 0, minutes: minutes || 0 };
  };

  const start = parseTime(parts[0]);
  const end = parseTime(parts[1]);

  return {
    startHour: start.hours,
    startMin: start.minutes,
    endHour: end.hours,
    endMin: end.minutes,
  };
}

/**
 * Get color based on priority (1 = highest priority = red, 5+ = low priority = green)
 */
function getAiTaskColor(priority: number): string {
  const colors: Record<number, string> = {
    1: "#FF6B6B", // High priority - red
    2: "#FFB84D", // orange
    3: "#FFE66D", // yellow
    4: "#4ECDC4", // teal
    5: "#95E1D3", // light green
  };
  return colors[Math.min(priority, 5)] || "#95E1D3";
}

/**
 * Map a single AI task entry to a Task object
 */
export function mapAiTaskEntryToTask(
  entry: AITaskEntry,
  plan: PlanResponse,
  index: number
): Task {
  const planDate = new Date(plan.plan_date);
  const { startHour, startMin, endHour, endMin } = parseTimeRange(entry.time_allotted);

  // Create start and end dates with proper times
  const startDate = new Date(planDate);
  startDate.setHours(startHour, startMin, 0, 0);

  const endDate = new Date(planDate);
  endDate.setHours(endHour, endMin, 0, 0);

  // Generate a unique numeric ID for the task
  // Using plan.id * 10000 + entry.id to ensure uniqueness
  const taskId = (plan.id || 0) * 10000 + (entry.id || index);

  return {
    id: taskId,
    title: entry.ai_task_name,
    subject: entry.task_name,
    type: "AI Study Task",
    difficulty: entry.difficulty,
    description: `AI-generated study task\nTime: ${entry.time_allotted}\nPriority: ${entry.priority}/10\nPlan notes: ${plan.notes || "None"}`,
    status: "Pending",
    startDate,
    endDate,
    color: getAiTaskColor(entry.priority),

    // AI-specific fields for editing/deleting
    isAiTask: true,
    planId: plan.id,
    aiTaskId: entry.id,
    priority: entry.priority,
  };
}

/**
 * Map all plans to Task objects
 */
export function mapPlansToTasks(plans: PlanResponse[]): Task[] {
  const tasks: Task[] = [];

  for (const plan of plans) {
    for (let i = 0; i < plan.entries.length; i++) {
      const entry = plan.entries[i];
      tasks.push(mapAiTaskEntryToTask(entry, plan, i));
    }
  }

  return tasks;
}

