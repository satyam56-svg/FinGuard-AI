import { useCallback, useEffect, useState } from "react";
import { getPredictionHistory } from "../services/api";
import {
    History,
    RotateCw,
    ShieldAlert,
    ShieldCheck,
    Inbox,
    AlertCircle,
} from "lucide-react";

function PredictionHistory() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadHistory = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const data = await getPredictionHistory();
            setHistory(data);
        } catch (err) {
            setError(
                err.message || "Unable to load prediction history."
            );
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadHistory();
    }, [loadHistory]);

    return (
        <section className="history-card animate-fade-in">
            <div className="section-header">
                <div>
                    <h2>
                        <History size={20} className="text-primary" /> Prediction History
                    </h2>
                    <p>Recent fraud detection assessments performed on your account.</p>
                </div>

                <button
                    type="button"
                    className="secondary-button"
                    onClick={loadHistory}
                    disabled={loading}
                >
                    <RotateCw size={16} className={loading ? "animate-spin" : ""} />
                    {loading ? "Refreshing..." : "Refresh"}
                </button>
            </div>

            {error && (
                <div className="error-card" style={{ marginBottom: "1rem" }}>
                    <AlertCircle size={18} />
                    <span>{error}</span>
                </div>
            )}

            {loading && (
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                    <div className="skeleton-box" style={{ height: "48px", width: "100%" }} />
                    <div className="skeleton-box" style={{ height: "48px", width: "100%" }} />
                    <div className="skeleton-box" style={{ height: "48px", width: "100%" }} />
                </div>
            )}

            {!loading && !error && history.length === 0 && (
                <div className="empty-state">
                    <Inbox />
                    <p>No prediction history records found.</p>
                </div>
            )}

            {!loading && !error && history.length > 0 && (
                <div className="table-responsive">
                    <table className="custom-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Result</th>
                                <th>Probability</th>
                                <th>Risk Score</th>
                                <th>Risk Level</th>
                                <th>Recommendation</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item) => {
                                const isFraud = item.prediction === 1;

                                return (
                                    <tr key={item.id}>
                                        <td>
                                            <strong style={{ fontFamily: "var(--font-mono)" }}>
                                                #{item.id}
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
                                                {(item.fraud_probability * 100).toFixed(2)}%
                                            </strong>
                                        </td>
                                        <td>
                                            <span style={{ fontFamily: "var(--font-mono)", fontWeight: 600 }}>
                                                {item.risk_score}
                                            </span>
                                        </td>
                                        <td>
                                            <span
                                                style={{
                                                    fontSize: "0.8rem",
                                                    fontWeight: 700,
                                                    textTransform: "uppercase",
                                                }}
                                            >
                                                {item.risk_level}
                                            </span>
                                        </td>
                                        <td>
                                            <span
                                                style={{
                                                    fontSize: "0.8rem",
                                                    fontWeight: 600,
                                                    textTransform: "uppercase",
                                                }}
                                            >
                                                {item.recommendation}
                                            </span>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </section>
    );
}

export default PredictionHistory;