"use client";
import "@/styles/user_detail.css";

type User = {
  fullName: string;
  username: string;
  email: string;
};

type Props = {
  user: User;
  theme: "light" | "dark" | "pink";
  onClose: () => void;
  onSignOut: () => void;
};

export default function UserProfileModal({
  user,
  theme,
  onClose,
  onSignOut,
}: Props) {
  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center">
      
      <div className={`user-modal ${theme}`}>

        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-700"
        >
          ✕
        </button>

        <h2 className="text-xl font-semibold mb-6">Profile</h2>

        <div className="space-y-4 text-sm">
          <div>
            <span className="label">Full name</span>
            <p className="value">{user.fullName}</p>
          </div>

          <div>
            <span className="label">Username</span>
            <p className="value">{user.username}</p>
          </div>

          <div>
            <span className="label">Email</span>
            <p className="value">{user.email}</p>
          </div>
        </div>

        <div className="divider" />

        <div className="profile-footer">
          <button className="signout-btn" onClick={onSignOut}>
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
}
