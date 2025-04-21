def score_transaction(tx):
    return {"score": 0.95, "risk": "low"} if tx else {"score": 0.0, "risk": "high"}
