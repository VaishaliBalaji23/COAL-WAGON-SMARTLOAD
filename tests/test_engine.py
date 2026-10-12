from backend.services.engine import evaluate

def test_safe_case():
    result = evaluate({
        "gross_weight_kg": 55000,
        "target_weight_kg": 58000,
        "pll_limit_kg": 60500,
        "left_pct": 50,
        "right_pct": 50,
        "front_pct": 50,
        "rear_pct": 50,
        "cross_validation_error_pct": 0.2,
        "loading_rate_kg_min": 250,
        "maintenance_risk_pct": 10,
    })
    assert result["risk_label"] in {"SAFE", "CAUTION", "CRITICAL"}
    assert result["recommended_action"]
