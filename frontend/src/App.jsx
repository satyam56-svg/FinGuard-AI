import { useEffect, useState } from "react";
import "./App.css";
import { checkHealth, predictTransaction } from "./services/api";
import TransactionForm from "./components/TransactionForm";
import PredictionResult from "./components/PredictionResult";
import Login from "./components/Login";
import Register from "./components/Register";
import PredictionHistory from "./components/PredictionHistory";
import AnalystDashboard from "./components/AnalystDashboard";
import AdminDashboard from "./components/AdminDashboard";
import { getCurrentUser } from "./services/auth";
import {
  ShieldAlert,
  Search,
  History,
  BarChart3,
  Users,
  LogOut,
  Menu,
  X,
  Server,
  AlertCircle,
} from "lucide-react";

function App() {
  const [token, setToken] = useState(() =>
    localStorage.getItem("finguard_token")
  );

  const currentUser = getCurrentUser();

  const [showRegister, setShowRegister] = useState(false);
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [activeTab, setActiveTab] = useState("analyze");
  const [mobileOpen, setMobileOpen] = useState(false);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkHealth()
      .then((data) => {
        if (data.status === "healthy" && data.model_loaded) {
          setBackendStatus("Backend Connected");
        } else {
          setBackendStatus("Backend Unavailable");
        }
      })
      .catch(() => {
        setBackendStatus("Backend Unavailable");
      });
  }, []);

  function handleLogin(newToken) {
    setToken(newToken);
    setShowRegister(false);
    setResult(null);
    setError(null);
    setActiveTab("analyze");
  }

  function handleLogout() {
    localStorage.removeItem("finguard_token");
    setToken(null);
    setResult(null);
    setError(null);
    setActiveTab("analyze");
    setMobileOpen(false);
  }

  async function handlePrediction(transaction) {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const prediction = await predictTransaction(transaction);
      setResult(prediction);
    } catch (err) {
      setError(err.message || "Unable to analyze transaction.");
    } finally {
      setLoading(false);
    }
  }

  // Authentication Screen Layout
  if (!token) {
    return (
      <div className="app">
        <main className="main-content" style={{ padding: 0, maxWidth: "none" }}>
          {showRegister ? (
            <Register onSwitchToLogin={() => setShowRegister(false)} />
          ) : (
            <Login
              onLogin={handleLogin}
              onSwitchToRegister={() => setShowRegister(true)}
            />
          )}
        </main>
      </div>
    );
  }

  const role = currentUser?.role || "USER";

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <aside className={`sidebar ${mobileOpen ? "mobile-open" : ""}`}>
        <div>
          <div className="sidebar-header">
            <div className="sidebar-logo-icon">
              <ShieldAlert size={22} />
            </div>
            <div className="sidebar-brand">
              <h1>FinGuard AI</h1>
              <span>Enterprise Fraud Hub</span>
            </div>
          </div>

          <nav className="nav-menu">
            <button
              type="button"
              className={`nav-item ${activeTab === "analyze" ? "active" : ""}`}
              onClick={() => {
                setActiveTab("analyze");
                setMobileOpen(false);
              }}
            >
              <Search size={18} />
              <span>Analyze Transaction</span>
            </button>

            <button
              type="button"
              className={`nav-item ${activeTab === "history" ? "active" : ""}`}
              onClick={() => {
                setActiveTab("history");
                setMobileOpen(false);
              }}
            >
              <History size={18} />
              <span>Prediction History</span>
            </button>

            {(role === "ANALYST" || role === "ADMIN") && (
              <button
                type="button"
                className={`nav-item ${
                  activeTab === "analyst" ? "active" : ""
                }`}
                onClick={() => {
                  setActiveTab("analyst");
                  setMobileOpen(false);
                }}
              >
                <BarChart3 size={18} />
                <span>Analyst Dashboard</span>
              </button>
            )}

            {role === "ADMIN" && (
              <button
                type="button"
                className={`nav-item ${activeTab === "admin" ? "active" : ""}`}
                onClick={() => {
                  setActiveTab("admin");
                  setMobileOpen(false);
                }}
              >
                <Users size={18} />
                <span>Admin Dashboard</span>
              </button>
            )}
          </nav>
        </div>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          <div className="user-profile-card">
            <div className="user-info-wrapper">
              <div className="avatar-circle">
                {currentUser?.username?.[0]?.toUpperCase() || "U"}
              </div>
              <div className="user-text-details">
                <span className="username-label">{currentUser?.username}</span>
                <span className={`role-badge ${role.toLowerCase()}`}>
                  {role}
                </span>
              </div>
            </div>
          </div>

          <button
            type="button"
            className="logout-button"
            onClick={handleLogout}
          >
            <LogOut size={16} /> Sign Out
          </button>
        </div>
      </aside>

      {/* Main App Section */}
      <div className="main-wrapper">
        {/* Sticky Top Header */}
        <header className="top-header">
          <div className="top-header-left">
            <button
              type="button"
              className="mobile-toggle"
              onClick={() => setMobileOpen(!mobileOpen)}
            >
              {mobileOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
            <div className="page-title-group">
              <h2>
                {activeTab === "analyze" && "Analyze Transaction"}
                {activeTab === "history" && "Prediction History"}
                {activeTab === "analyst" && "Analyst Intelligence Dashboard"}
                {activeTab === "admin" && "Admin Access Console"}
              </h2>
            </div>
          </div>

          <div className="backend-status-pill">
            <div
              className={`status-dot ${
                backendStatus === "Backend Connected" ? "healthy" : "unavailable"
              }`}
            />
            <Server size={14} className="text-secondary" />
            <span>{backendStatus}</span>
          </div>
        </header>

        {/* View Contents */}
        <main className="main-content">
          {activeTab === "analyze" && (
            <>
              <section className="hero-card">
                <h2>
                  <ShieldAlert size={22} className="text-primary" /> Transaction Risk Engine
                </h2>
                <p>
                  Evaluate transaction risk in real time using FinGuard AI's XGBoost ML model, SHAP feature impact explainability, and Gemini AI assessment.
                </p>
                <div className="status-message">
                  Backend Status: <strong>{backendStatus}</strong>
                </div>
              </section>

              <section className="transaction-card">
                <div className="section-header">
                  <div>
                    <h2>Analyze Transaction</h2>
                    <p>Enter financial transaction parameters below for immediate fraud detection.</p>
                  </div>
                </div>

                <TransactionForm
                  onSubmit={handlePrediction}
                  loading={loading}
                />
              </section>

              {error && (
                <section className="error-card">
                  <AlertCircle size={20} />
                  <div>
                    <h3 style={{ fontSize: "0.95rem", fontWeight: 700 }}>Prediction Error</h3>
                    <p style={{ fontSize: "0.875rem", marginTop: "0.2rem" }}>{error}</p>
                  </div>
                </section>
              )}

              {result && <PredictionResult result={result} />}
            </>
          )}

          {activeTab === "history" && <PredictionHistory />}

          {activeTab === "analyst" &&
            (role === "ANALYST" || role === "ADMIN") && (
              <AnalystDashboard />
            )}

          {activeTab === "admin" && role === "ADMIN" && <AdminDashboard />}
        </main>
      </div>
    </div>
  );
}

export default App;