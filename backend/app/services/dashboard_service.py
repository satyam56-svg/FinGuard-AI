from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.database.models import PredictionAudit


def get_dashboard_stats(db: Session) -> dict:
    total_predictions = (
        db.query(func.count(PredictionAudit.id))
        .scalar()
        or 0
    )

    fraud_predictions = (
        db.query(func.count(PredictionAudit.id))
        .filter(PredictionAudit.prediction == 1)
        .scalar()
        or 0
    )

    non_fraud_predictions = (
        total_predictions - fraud_predictions
    )

    fraud_rate = (
        (fraud_predictions / total_predictions) * 100
        if total_predictions > 0
        else 0.0
    )

    average_risk_score = (
        db.query(func.avg(PredictionAudit.risk_score))
        .scalar()
        or 0.0
    )

    return {
        "total_predictions": total_predictions,
        "fraud_predictions": fraud_predictions,
        "non_fraud_predictions": non_fraud_predictions,
        "fraud_rate": round(fraud_rate, 2),
        "average_risk_score": round(
            float(average_risk_score),
            2,
        ),
    }

def get_risk_distribution(
    db: Session,
) -> dict[str, int]:

    risk_levels = (
        db.query(
            PredictionAudit.risk_level,
            func.count(PredictionAudit.id),
        )
        .group_by(PredictionAudit.risk_level)
        .all()
    )

    distribution = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0,
    }

    for risk_level, count in risk_levels:
        key = risk_level.lower()

        if key in distribution:
            distribution[key] = count

    return distribution

def get_recent_predictions(
    db: Session,
    limit: int = 10,
) -> list[PredictionAudit]:

    return list(
        db.query(PredictionAudit)
        .order_by(
            PredictionAudit.id.desc()
        )
        .limit(limit)
        .all()
    )