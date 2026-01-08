export type StoredUser = {
  fullName: string;
  username: string;
  email: string;
};

// Save user to localStorage
export const saveUser = (user: StoredUser) => {
  localStorage.setItem("currentUser", JSON.stringify(user));
};

// Load user from localStorage
export const loadUser = (): StoredUser | null => {
  const data = localStorage.getItem("currentUser");
  return data ? JSON.parse(data) : null;
};

// Clear user on logout
export const clearUser = () => {
  localStorage.removeItem("currentUser");
};
