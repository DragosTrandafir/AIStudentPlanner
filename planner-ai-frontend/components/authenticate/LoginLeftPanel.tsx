type Props = {
  onRegister: () => void;
};

export default function LoginLeftPanel({ onRegister }: Props) {
  return (
    <div className="login-left">
      <div className="login-left-header">
        <h1>Welcome back!</h1>
        <p>You can sign in to access your planner.</p>
      </div>

      <div className="register-cta">
        <p className="register-text">
          Don’t have an account yet?
          <br />
          Create one now and start planning smarter.
        </p>

        <button className="register-btn" onClick={onRegister}>
          Register
        </button>
      </div>

      <div className="login-shapes">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}
