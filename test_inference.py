from ml_pipeline.inference.predictor import FraudPredictor


predictor = FraudPredictor()


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


result = predictor.predict(transaction)


print("\n" + "=" * 60)
print("FINGUARD AI — INFERENCE RESULT")
print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")