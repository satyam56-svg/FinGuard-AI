import { useState } from "react";
import { loginUser } from "../services/api";
import {
  ShieldAlert,
  Lock,
  User,
  Eye,
  EyeOff,
  Cpu,
  Activity,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
} from "lucide-react";

function Login({ onLogin, onSwitchToRegister }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await loginUser({
        username,
        password,
      });

      localStorage.setItem("finguard_token", response.access_token);

      onLogin(response.access_token);
    } catch (err) {
      setError(err.message || "Login failed.");
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
                  <h4>AI Risk Engine</h4>
                  <p>
                    Real-time ML risk scoring and automated anomaly detection.
                  </p>
                </div>
              </div>

              <div className="value-prop-item">
                <div className="value-prop-icon">
                  <Activity size={20} />
                </div>
                <div className="value-prop-text">
                  <h4>SHAP Explainability</h4>
                  <p>
                    Clear model feature impact breakdown for transparent security decisions.
                  </p>
                </div>
              </div>

              <div className="value-prop-item">
                <div className="value-prop-icon">
                  <CheckCircle2 size={20} />
                </div>
                <div className="value-prop-text">
                  <h4>Generative AI Summaries</h4>
                  <p>
                    Automated analyst recommendations powered by Gemini AI.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="status-message" style={{ margin: 0 }}>
            Enterprise Security • Encrypted JWT Authentication
          </div>
        </div>

        {/* Right Form Card */}
        <section className="auth-card">
          <div className="auth-header">
            <h2>Sign In</h2>
            <p>Enter your credentials to access the security console.</p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <div className="input-wrapper">
                <User className="input-icon" size={18} />
                <input
                  id="username"
                  type="text"
                  className="has-icon"
                  placeholder="e.g. analyst_user"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-wrapper">
                <Lock className="input-icon" size={18} />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  className="has-icon"
                  placeholder="••••••••"
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

            <button type="submit" className="analyze-button" disabled={loading}>
              {loading ? (
                <>Signing in...</>
              ) : (
                <>
                  Sign In <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <div className="auth-switch">
            <span>Don't have an account?</span>
            <button type="button" onClick={onSwitchToRegister}>
              Create Account
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Login;