from datetime import datetime
from ml.model import predict_risk

def evaluate(payload: dict):
    weight = float(payload.get("gross_weight_kg", 0))
    target = max(float(payload.get("target_weight_kg", 1)), 1)
    pll = float(payload.get("pll_limit_kg", target))
    left = float(payload.get("left_pct", 50))
    right = float(payload.get("right_pct", 50))
    front = float(payload.get("front_pct", 50))
    rear = float(payload.get("rear_pct", 50))
    cv_error = float(payload.get("cross_validation_error_pct", 0))
    rate = float(payload.get("loading_rate_kg_min", 0))
    maintenance = float(payload.get("maintenance_risk_pct", 0))

    max_error = max(abs(left-right), abs(front-rear))
    load_ratio = weight / target

    risk_label, probability = predict_risk({
        "load_ratio": load_ratio,
        "max_distribution_error": max_error,
        "cross_validation_error_pct": cv_error,
        "loading_rate_kg_min": rate,
        "maintenance_risk_pct": maintenance,
    })

    if weight > pll:
        action = "EMERGENCY HOLD"
    elif risk_label == "CRITICAL":
        action = "STOP NOW"
    elif risk_label == "CAUTION":
        action = "SLOW LOADING"
    else:
        action = "CONTINUE LOADING"

    confidence = max(5.0, min(99.0, probability * 100))
    return {
        "timestamp": datetime.now().isoformat(),
        "risk_label": risk_label,
        "risk_probability": round(probability, 4),
        "confidence": round(confidence, 1),
        "recommended_action": action,
        "load_ratio": round(load_ratio, 4),
        "max_distribution_error": round(max_error, 2),
    }
