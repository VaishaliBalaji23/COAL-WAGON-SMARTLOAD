from pathlib import Path
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "ml" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "risk_model.joblib"

rng = np.random.default_rng(42)
n = 5000

load_ratio = rng.uniform(0.65, 1.12, n)
dist_error = rng.uniform(0, 35, n)
cv_error = rng.uniform(0, 8, n)
rate = rng.uniform(50, 900, n)
maintenance = rng.uniform(0, 100, n)

X = np.column_stack([load_ratio, dist_error, cv_error, rate, maintenance])
risk_score = (
    55 * np.maximum(0, load_ratio - 0.98)
    + 1.8 * np.maximum(0, dist_error - 10)
    + 2.2 * np.maximum(0, cv_error - 1)
    + 0.025 * np.maximum(0, rate - 450)
    + 0.7 * np.maximum(0, maintenance - 30)
)

y = np.where(risk_score >= 45, "CRITICAL",
     np.where(risk_score >= 18, "CAUTION", "SAFE"))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=180, max_depth=12, random_state=42, class_weight="balanced"
)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))
joblib.dump(model, MODEL_PATH)
print(f"Saved: {MODEL_PATH}")
