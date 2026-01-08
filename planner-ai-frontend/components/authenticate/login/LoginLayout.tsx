import LoginLeftPanel from "./LoginLeftPanel";
import LoginForm from "./LoginForm";

type Props = {
  onLogin: () => void;
  onRegister: () => void;
};

export default function LoginLayout({ onLogin, onRegister }: Props) {
  return (
    <div className="login-overlay">
      <div className="login-container">
        <LoginLeftPanel onRegister={onRegister} /> {/* 👈 */}
        <LoginForm onLogin={onLogin} />
      </div>
    </div>
  );
}
