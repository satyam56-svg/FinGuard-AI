from sqlalchemy.orm import Session

from backend.app.database.models import PredictionAudit


def create_prediction_audit(
    db: Session,
    user_id: int,
    prediction_result: dict,
) -> PredictionAudit:

    audit = PredictionAudit(
        user_id=user_id,
        prediction=prediction_result["prediction"],
        fraud_probability=prediction_result["fraud_probability"],
        risk_score=prediction_result["risk_score"],
        risk_level=prediction_result["risk_level"],
        recommendation=prediction_result["recommendation"],
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit

def get_user_prediction_history(
    db: Session,
    user_id: int,
) -> list[PredictionAudit]:

    return list(
        db.query(PredictionAudit)
        .filter(
            PredictionAudit.user_id == user_id
        )
        .order_by(
            PredictionAudit.id.desc()
        )
        .all()
    )