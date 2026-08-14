import {
  ShieldAlert,
  ShieldCheck,
  HelpCircle,
  TrendingUp,
  TrendingDown,
  Sparkles,
  AlertOctagon,
} from "lucide-react";

function PredictionResult({ result }) {
  const isFraud = result.prediction === 1;
  const riskLevelLower = (result.risk_level || "low").toLowerCase();

  return (
    <section
      className={`result-card animate-fade-in ${
        isFraud ? "is-fraud" : "is-genuine"
      }`}
    >
      <div className="result-header">
        <div>
          <h2>Transaction Analysis</h2>
          <p>FinGuard AI Real-Time Fraud Assessment</p>
        </div>

        <span
          className={
            isFraud ? "status-badge fraud" : "status-badge genuine"
          }
        >
          {isFraud ? (
            <>
              <ShieldAlert size={16} /> FRAUD DETECTED
            </>
          ) : (
            <>
              <ShieldCheck size={16} /> GENUINE
            </>
          )}
        </span>
      </div>

      <div className="risk-summary">
        <div className="risk-score-container">
          <span style={{ fontSize: "0.75rem", fontWeight: 600, color: "var(--text-secondary)", textTransform: "uppercase" }}>
            Risk Score
          </span>
          <div className={`risk-score-circle ${riskLevelLower}`}>
            <span className="risk-score-value">{result.risk_score}</span>
            <span className="risk-score-label">/ 100</span>
          </div>
        </div>

        <div className="risk-details">
          <div className="risk-metric-box">
            <span>Fraud Probability</span>
            <strong style={{ color: isFraud ? "var(--color-danger)" : "var(--color-success)" }}>
              {(result.fraud_probability * 100).toFixed(2)}%
            </strong>
          </div>

          <div className="risk-metric-box">
            <span>Risk Level</span>
            <strong style={{ textTransform: "uppercase" }}>
              {result.risk_level}
            </strong>
          </div>

          <div className="risk-metric-box">
            <span>Recommendation</span>
            <strong style={{ textTransform: "uppercase" }}>
              {result.recommendation}
            </strong>
          </div>
        </div>
      </div>

      {/* SHAP Explainability Section */}
      <div className="explanation-section">
        <h3>
          <HelpCircle size={18} className="text-primary" /> Why this decision?
        </h3>

        {result.explanation?.risk_factors?.length > 0 && (
          <div className="factor-group">
            <h4>Risk Factors (Increasing Fraud Probability)</h4>
            {result.explanation.risk_factors.map((factor, index) => (
              <div className="factor-card" key={`risk-${index}`}>
                <div className="factor-info">
                  <strong>{factor.feature}</strong>
                  <span>Value: {factor.value}</span>
                </div>
                <span className="impact-badge risk">
                  <TrendingUp size={14} /> +{factor.impact.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        )}

        {result.explanation?.protective_factors?.length > 0 && (
          <div className="factor-group" style={{ marginTop: "1.25rem" }}>
            <h4>Protective Factors (Reducing Fraud Risk)</h4>
            {result.explanation.protective_factors.map((factor, index) => (
              <div className="factor-card" key={`protective-${index}`}>
                <div className="factor-info">
                  <strong>{factor.feature}</strong>
                  <span>Value: {factor.value}</span>
                </div>
                <span className="impact-badge protective">
                  <TrendingDown size={14} /> -{factor.impact.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Gemini AI Intelligence Assessment Section */}
      {result.ai_report && (
        <div className="ai-report-section">
          <div className="ai-report-header">
            <Sparkles size={20} />
            <span>AI Analyst Assessment</span>
          </div>

          <div className="ai-report-grid">
            <div className="ai-report-block">
              <h4>Summary</h4>
              <p>{result.ai_report.summary}</p>
            </div>

            <div className="ai-report-block">
              <h4>Risk Reason</h4>
              <p>{result.ai_report.risk_reason}</p>
            </div>

            <div className="ai-report-block">
              <h4>Recommended Action</h4>
              <div style={{ marginTop: "0.25rem" }}>
                <span className="status-badge" style={{ backgroundColor: "rgba(59, 130, 246, 0.15)", color: "var(--primary-light)", border: "1px solid rgba(59, 130, 246, 0.3)" }}>
                  <AlertOctagon size={14} /> {result.ai_report.recommended_action}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default PredictionResult;