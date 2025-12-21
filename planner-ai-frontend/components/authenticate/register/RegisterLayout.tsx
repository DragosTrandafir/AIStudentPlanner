import RegisterLeftPanel from "./RegisterLeftPanel";
import RegisterForm from "./RegisterForm";

type Props = {
  onRegisterSuccess: () => void;
  onGoToLogin: () => void;
};

export default function RegisterLayout({
  onRegisterSuccess,
  onGoToLogin,
}: Props) {
  return (
    <div className="login-overlay">
      <div className="login-container">
        <RegisterLeftPanel />
        <RegisterForm
          onRegisterSuccess={onRegisterSuccess}
          onGoToLogin={onGoToLogin}
        />
      </div>
    </div>
  );
}
