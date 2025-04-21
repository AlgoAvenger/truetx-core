from ai_risk_engine.scorer import score_transaction

def test_score_transaction():
    result = score_transaction({"amount": 100})
    assert result["risk"] == "low"
