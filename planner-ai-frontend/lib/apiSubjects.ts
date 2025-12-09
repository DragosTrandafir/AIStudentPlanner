export const USER_ID = 1;
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
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(subject),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to create subject: " + msg);
  }
  return res.json();
}

export async function getSubjects() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects`);
  if (!res.ok) throw new Error("Failed to load subjects");
  return res.json();
}
export async function deleteSubject(subjectId: number) {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects/${subjectId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to delete subject: " + msg);
  }
}
export async function updateSubject(id: number, subject: SubjectCreatePayload) {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/subjects/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(subject),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error("Failed to update subject: " + msg);
  }

  return res.json(); // IMPORTANT: returnează task-ul actualizat!
}



