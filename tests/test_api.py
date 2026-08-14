import httpx


BASE_URL = "http://127.0.0.1:8000"


def test_health():
    response = httpx.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_fraud_prediction():
    transaction = {
        "step": 1,
        "type": "TRANSFER",
        "amount": 181.0,
        "oldbalanceOrg": 181.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
        "isFlaggedFraud": 0,
        "origin_balance_error": 0.0,
        "destination_balance_error": 181.0,
        "origin_balance_change": -181.0,
        "destination_balance_change": 181.0,
    }

    response = httpx.post(
        f"{BASE_URL}/predict",
        json=transaction,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == 1
    assert data["risk_level"] == "CRITICAL"
    assert data["recommendation"] == "BLOCK_OR_REVIEW"

    assert data["fraud_probability"] == 0.919992


def test_invalid_transaction_type():
    transaction = {
        "step": 1,
        "type": "INVALID",
        "amount": 181.0,
        "oldbalanceOrg": 181.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
        "isFlaggedFraud": 0,
        "origin_balance_error": 0.0,
        "destination_balance_error": 181.0,
        "origin_balance_change": -181.0,
        "destination_balance_change": 181.0,
    }

    response = httpx.post(
        f"{BASE_URL}/predict",
        json=transaction,
    )

    assert response.status_code == 422

def test_genuine_prediction():
    transaction = {
        "step": 1,
        "type": "PAYMENT",
        "amount": 50.0,
        "oldbalanceOrg": 5000.0,
        "newbalanceOrig": 4950.0,
        "oldbalanceDest": 10000.0,
        "newbalanceDest": 10050.0,
        "isFlaggedFraud": 0,
        "origin_balance_error": 0.0,
        "destination_balance_error": 0.0,
        "origin_balance_change": -50.0,
        "destination_balance_change": 50.0,
    }

    response = httpx.post(
        f"{BASE_URL}/predict",
        json=transaction,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == 0
    assert data["risk_level"] == "LOW"
    assert data["recommendation"] == "ALLOW"