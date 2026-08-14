import { useCallback, useEffect, useState } from "react";
import {
  getAnalystStats,
  getRiskDistribution,
  getRecentPredictions,
} from "../services/api";
import {
  BarChart3,
  ShieldAlert,
  ShieldCheck,
  RotateCw,
  AlertCircle,
  Activity,
  Percent,
  Layers,
  Inbox,
} from "lucide-react";

function AnalystDashboard() {
  const [stats, setStats] = useState(null);
  const [riskDistribution, setRiskDistribution] = useState(null);
  const [recentPredictions, setRecentPredictions] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
        const [statsData, riskData, recentData] = await Promise.all([
            getAnalystStats(),
            getRiskDistribution(),
            getRecentPredictions(),
        ]);

        setStats(statsData);
        setRiskDistribution(riskData);
        setRecentPredictions(recentData);
    } catch (err) {
        setError(err.message || "Unable to load analyst dashboard.");
    } finally {
        setLoading(false);
    }
}, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  if (loading) {
    return (
      <section className="dashboard-card animate-fade-in">
        <div className="section-header">
          <h2>
            <BarChart3 size={20} className="text-primary" /> Analyst Dashboard
          </h2>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "1rem", marginBottom: "1.5rem" }}>
          <div className="skeleton-box" style={{ height: "90px" }} />
          <div className="skeleton-box" style={{ height: "90px" }} />
          <div className="skeleton-box" style={{ height: "90px" }} />
          <div className="skeleton-box" style={{ height: "90px" }} />
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="dashboard-card animate-fade-in">
        <div className="section-header">
          <h2>
            <BarChart3 size={20} className="text-primary" /> Analyst Dashboard
          </h2>
        </div>
        <div className="error-card" style={{ marginBottom: "1rem" }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
        <button
          type="button"
          className="secondary-button"
          onClick={loadDashboard}
        >
          <RotateCw size={16} /> Retry Loading
        </button>
      </section>
    );
  }

  const totalDist =
    (riskDistribution?.low || 0) +
    (riskDistribution?.medium || 0) +
    (riskDistribution?.high || 0) +
    (riskDistribution?.critical || 0) || 1;

  return (
    <section className="dashboard-card animate-fade-in">
      <div className="section-header">
        <div>
          <h2>
            <BarChart3 size={20} className="text-primary" /> Analyst Intelligence Dashboard
          </h2>
          <p>Global oversight of fraud detection metrics and risk category distribution.</p>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={loadDashboard}
        >
          <RotateCw size={16} /> Refresh
        </button>
      </div>

      {/* KPI Cards */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <span>
              <Layers size={14} style={{ display: "inline", marginRight: 4 }} /> Total Predictions
            </span>
            <strong>{stats.total_predictions}</strong>
          </div>

          <div className="stat-card">
            <span style={{ color: "var(--color-danger)" }}>
              <ShieldAlert size={14} style={{ display: "inline", marginRight: 4 }} /> Fraud Predictions
            </span>
            <strong style={{ color: "var(--color-danger)" }}>
              {stats.fraud_predictions}
            </strong>
          </div>

          <div className="stat-card">
            <span style={{ color: "var(--color-success)" }}>
              <ShieldCheck size={14} style={{ display: "inline", marginRight: 4 }} /> Non-Fraud Predictions
            </span>
            <strong style={{ color: "var(--color-success)" }}>
              {stats.non_fraud_predictions}
            </strong>
          </div>

          <div className="stat-card">
            <span>
              <Percent size={14} style={{ display: "inline", marginRight: 4 }} /> Fraud Rate
            </span>
            <strong>{stats.fraud_rate.toFixed(2)}%</strong>
          </div>

          <div className="stat-card">
            <span>
              <Activity size={14} style={{ display: "inline", marginRight: 4 }} /> Avg Risk Score
            </span>
            <strong>{stats.average_risk_score}</strong>
          </div>
        </div>
      )}

      {/* Risk Distribution Cards with Visual Bars */}
      {riskDistribution && (
        <div className="dashboard-section">
          <h3>Risk Tier Distribution</h3>
          <div className="risk-distribution-grid">
            <div className="distribution-card">
              <div className="distribution-card-header">
                <span className="low">LOW RISK</span>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                  {Math.round((riskDistribution.low / totalDist) * 100)}%
                </span>
              </div>
              <strong>{riskDistribution.low}</strong>
              <div className="distribution-progress-track">
                <div
                  className="distribution-progress-fill low"
                  style={{ width: `${(riskDistribution.low / totalDist) * 100}%` }}
                />
              </div>
            </div>

            <div className="distribution-card">
              <div className="distribution-card-header">
                <span className="medium">MEDIUM RISK</span>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                  {Math.round((riskDistribution.medium / totalDist) * 100)}%
                </span>
              </div>
              <strong>{riskDistribution.medium}</strong>
              <div className="distribution-progress-track">
                <div
                  className="distribution-progress-fill medium"
                  style={{ width: `${(riskDistribution.medium / totalDist) * 100}%` }}
                />
              </div>
            </div>

            <div className="distribution-card">
              <div className="distribution-card-header">
                <span className="high">HIGH RISK</span>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                  {Math.round((riskDistribution.high / totalDist) * 100)}%
                </span>
              </div>
              <strong>{riskDistribution.high}</strong>
              <div className="distribution-progress-track">
                <div
                  className="distribution-progress-fill high"
                  style={{ width: `${(riskDistribution.high / totalDist) * 100}%` }}
                />
              </div>
            </div>

            <div className="distribution-card">
              <div className="distribution-card-header">
                <span className="critical">CRITICAL RISK</span>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                  {Math.round((riskDistribution.critical / totalDist) * 100)}%
                </span>
              </div>
              <strong>{riskDistribution.critical}</strong>
              <div className="distribution-progress-track">
                <div
                  className="distribution-progress-fill critical"
                  style={{ width: `${(riskDistribution.critical / totalDist) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Predictions Table */}
      <div className="dashboard-section">
        <h3>Recent Transactions Analyzed</h3>

        {recentPredictions.length === 0 ? (
          <div className="empty-state">
            <Inbox />
            <p>No recent predictions found.</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Prediction ID</th>
                  <th>Status</th>
                  <th>Probability</th>
                  <th>Risk Tier</th>
                  <th>Score</th>
                  <th>Recommendation</th>
                </tr>
              </thead>
              <tbody>
                {recentPredictions.map((prediction) => {
                  const isFraud = prediction.prediction === 1;

                  return (
                    <tr key={prediction.id}>
                      <td>
                        <strong style={{ fontFamily: "var(--font-mono)" }}>
                          #{prediction.id}
                        </strong>
                      </td>
                      <td>
                        <span
                          className={
                            isFraud
                              ? "status-badge fraud"
                              : "status-badge genuine"
                          }
                        >
                          {isFraud ? (
                            <>
                              <ShieldAlert size={14} /> FRAUD
                            </>
                          ) : (
                            <>
                              <ShieldCheck size={14} /> GENUINE
                            </>
                          )}
                        </span>
                      </td>
                      <td>
                        <strong
                          style={{
                            fontFamily: "var(--font-mono)",
                            color: isFraud
                              ? "var(--color-danger)"
                              : "var(--color-success)",
                          }}
                        >
                          {(prediction.fraud_probability * 100).toFixed(2)}%
                        </strong>
                      </td>
                      <td>
                        <span
                          style={{
                            fontSize: "0.8rem",
                            fontWeight: 700,
                            textTransform: "uppercase",
                          }}
                        >
                          {prediction.risk_level}
                        </span>
                      </td>
                      <td>
                        <span style={{ fontFamily: "var(--font-mono)", fontWeight: 600 }}>
                          {prediction.risk_score}
                        </span>
                      </td>
                      <td>
                        <span style={{ fontSize: "0.8rem", fontWeight: 600 }}>
                          {prediction.recommendation}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

export default AnalystDashboard;