import { getAuthHeaders, getCurrentUserId } from "@/utils/apiUtils";

const BASE_URL = "http://localhost:8000";

export interface SubjectCreatePayload {
  title: string;
  name: string;
  type: "written" | "practical" | "project";
  status?: "not_started" | "in_progress" | "completed";
  difficulty?: number;
  start_date?: string;
  end_date?: string;
  description?: string;
}

export async function createSubject(subject: SubjectCreatePayload) {
  const USER_ID = getCurrentUserId();
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(subject),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to create subject: " + msg);
  }
  return res.json();
}

export async function getSubjects() {
    const USER_ID = getCurrentUserId();
    const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects`, {
        method: "GET",
        headers: getAuthHeaders()
      });

      if (!res.ok) throw new Error("Failed to load subjects");
      return res.json();
}
export async function deleteSubject(subjectId: number) {
  const USER_ID = getCurrentUserId();
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects/${subjectId}`, {
    method: "DELETE",
    headers: getAuthHeaders()
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to delete subject: " + msg);
  }
}
export async function updateSubject(id: number, subject: SubjectCreatePayload) {
  const USER_ID = getCurrentUserId();
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(subject),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to update subject: " + msg);
  }

  return res.json(); // IMPORTANT: returnează task-ul actualizat!
}



