
// Helper to get the token and format headers
export function getAuthHeaders() {
  const token = localStorage.getItem("authToken");

  // Optional: Safety check
  if (!token) {
    console.warn("No auth token found! Requests might fail.");
  }

  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}

// Helper to get the logged-in User ID
export function getCurrentUserId(): number {
  const storedUser = localStorage.getItem("currentUser");

  if (!storedUser) {
    throw new Error("User is not logged in");
  }

  try {
    const user = JSON.parse(storedUser);
    if (!user.id) throw new Error("User object is missing ID");
    return user.id;
  } catch (error) {
    throw new Error("Failed to parse user data");
  }
}