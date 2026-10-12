from pathlib import Path
import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent / "models" / "risk_model.joblib"

FEATURES = [
    "load_ratio",
    "max_distribution_error",
    "cross_validation_error_pct",
    "loading_rate_kg_min",
    "maintenance_risk_pct",
]

def _heuristic_predict(x):
    score = (
        55 * max(0.0, x[0] - 0.98)
        + 1.8 * max(0.0, x[1] - 10)
        + 2.2 * max(0.0, x[2] - 1)
        + 0.025 * max(0.0, x[3] - 450)
        + 0.7 * max(0.0, x[4] - 30)
    )
    if score >= 45:
        return "CRITICAL", min(0.99, 0.55 + score / 250)
    if score >= 18:
        return "CAUTION", min(0.94, 0.50 + score / 150)
    return "SAFE", max(0.51, 0.98 - score / 120)

def predict_risk(features: dict):
    values = [float(features.get(k, 0)) for k in FEATURES]
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        pred = model.predict([values])[0]
        probabilities = getattr(model, "predict_proba", lambda x: None)([values])
        if probabilities is not None:
            classes = list(model.classes_)
            probability = float(max(probabilities[0]))
        else:
            probability = 0.80
        return str(pred), probability
    return _heuristic_predict(values)
