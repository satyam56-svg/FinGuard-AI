import { useState } from "react";
import { registerUser } from "../services/api";
import {
  ShieldAlert,
  Lock,
  User,
  Mail,
  Eye,
  EyeOff,
  Cpu,
  Activity,
  CheckCircle2,
  AlertCircle,
  UserPlus,
} from "lucide-react";

function Register({ onSwitchToLogin }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await registerUser({
        username,
        email,
        password,
      });

      setSuccess("Registration successful. You can now sign in.");

      setUsername("");
      setEmail("");
      setPassword("");
    } catch (err) {
      setError(err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-container animate-fade-in">
        {/* Left Information Panel */}
        <div className="auth-visual-panel">
          <div>
            <div className="auth-brand">
              <div className="auth-brand-icon">
                <ShieldAlert size={24} />
              </div>
              <div className="auth-brand-text">
                <h1>FinGuard AI</h1>
                <span>Fraud Intelligence Platform</span>
              </div>
            </div>

            <div className="auth-value-props">
              <div className="value-prop-item">
                <div className="value-prop-icon">
                  <Cpu size={20} />
                </div>
                <div className="value-prop-text">
                  <h4>Account Setup</h4>
                  <p>
                    Create your security credentials to access FinGuard AI analysis tools.
                  </p>
                </div>
              </div>

              <div className="value-prop-item">
                <div className="value-prop-icon">
                  <Activity size={20} />
                </div>
                <div className="value-prop-text">
                  <h4>Role Based Intelligence</h4>
                  <p>
                    Default user privileges with upgrade path to Analyst and Admin consoles.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="status-message" style={{ margin: 0 }}>
            FinGuard AI • Multi-layered Security Engine
          </div>
        </div>

        {/* Right Form Card */}
        <section className="auth-card">
          <div className="auth-header">
            <h2>Create Account</h2>
            <p>Register to start evaluating transaction risks.</p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="register-username">Username</label>
              <div className="input-wrapper">
                <User className="input-icon" size={18} />
                <input
                  id="register-username"
                  type="text"
                  className="has-icon"
                  minLength="3"
                  maxLength="50"
                  placeholder="Choose a username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="register-email">Email Address</label>
              <div className="input-wrapper">
                <Mail className="input-icon" size={18} />
                <input
                  id="register-email"
                  type="email"
                  className="has-icon"
                  placeholder="name@company.com"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="register-password">Password</label>
              <div className="input-wrapper">
                <Lock className="input-icon" size={18} />
                <input
                  id="register-password"
                  type={showPassword ? "text" : "password"}
                  className="has-icon"
                  minLength="8"
                  maxLength="72"
                  placeholder="Min. 8 characters"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {error && (
              <div className="validation-error">
                <AlertCircle size={18} />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="success-message">
                <CheckCircle2 size={18} />
                <span>{success}</span>
              </div>
            )}

            <button type="submit" className="analyze-button" disabled={loading}>
              {loading ? (
                <>Creating Account...</>
              ) : (
                <>
                  Create Account <UserPlus size={18} />
                </>
              )}
            </button>
          </form>

          <div className="auth-switch">
            <span>Already have an account?</span>
            <button type="button" onClick={onSwitchToLogin}>
              Sign In
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Register;