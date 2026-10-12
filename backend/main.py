from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.db.database import init_db, insert_telemetry, recent_telemetry
from backend.services.engine import evaluate

app = FastAPI(
    title="SmartLoad Backend API",
    version="1.0.0",
    description="Backend services for SmartLoad rail wagon intelligence."
)

class Telemetry(BaseModel):
    wagon_id: str = "BOXN-123456"
    siding_id: str = "Siding-01"
    wagon_type: str = "BOXN"
    gross_weight_kg: float = Field(..., ge=0)
    target_weight_kg: float = Field(..., gt=0)
    pll_limit_kg: float = Field(..., gt=0)
    left_pct: float = 50
    right_pct: float = 50
    front_pct: float = 50
    rear_pct: float = 50
    scenario: str = "Normal Continuous Loading"
    cross_validation_error_pct: float = 0
    loading_rate_kg_min: float = 0
    maintenance_risk_pct: float = 0
    timestamp: str | None = None

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status": "online", "service": "SmartLoad Backend", "timestamp": datetime.now().isoformat()}

@app.post("/api/predict")
def predict(data: Telemetry):
    result = evaluate(data.model_dump())
    return result

@app.post("/api/telemetry")
def telemetry(data: Telemetry):
    payload = data.model_dump()
    result = evaluate(payload)
    record = {**payload, **result}
    insert_telemetry(record)
    return {"stored": True, "prediction": result}

@app.get("/api/telemetry")
def telemetry_history(limit: int = 100):
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="limit must be 1..1000")
    return recent_telemetry(limit)

@app.get("/api/analytics/summary")
def analytics_summary():
    rows = recent_telemetry(1000)
    if not rows:
        return {"records": 0, "safe": 0, "caution": 0, "critical": 0, "avg_confidence": 0}
    labels = [r.get("risk_label") for r in rows]
    conf = [float(r.get("confidence") or 0) for r in rows]
    return {
        "records": len(rows),
        "safe": labels.count("SAFE"),
        "caution": labels.count("CAUTION"),
        "critical": labels.count("CRITICAL"),
        "avg_confidence": round(sum(conf) / len(conf), 1),
    }
