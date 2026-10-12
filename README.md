# COAL WAGON SMARTLOAD — Full-Stack Intelligence Platform

This project is the **Coal Wagon / Rail Wagon SmartLoad system**. It is separate from SAMUDRA SAKSHI.

A complete demo-ready rail wagon load intelligence platform built around the existing SmartLoad dashboard.

## What is included

- **Frontend / Dashboard:** Streamlit + Plotly, retaining the existing SmartLoad Liquid Glass UI.
- **Backend API:** FastAPI REST service.
- **ML model:** Random Forest risk classifier trained on a synthetic rail-loading dataset.
- **Data layer:** SQLite telemetry/audit storage.
- **Simulation:** normal, uneven, overload, underload, front-heavy and rear-heavy scenarios.
- **3D LiDAR visualization:** interactive digital-twin style load surface.
- **Predictive control:** stop-point, loading rate, directional guidance and confidence.
- **Hardware health:** load-cell, LiDAR, RFID, communications and calibration states.
- **Load integrity:** dispatch/checkpoint anomaly detection.
- **Digital certificate:** SHA-256 tamper-evident record.
- **Analytics:** persisted telemetry and ML risk summary.

## Architecture

```text
Browser
   |
   v
Streamlit Dashboard (frontend/app.py)
   |
   +----> FastAPI REST API (backend/main.py)
   |          |
   |          +----> ML Risk Model (ml/models/risk_model.joblib)
   |          |
   |          +----> SQLite Telemetry DB (data/smartload.db)
   |
   +----> Plotly 2D/3D visualizations
```

## Windows setup

Open PowerShell in the project folder:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ml	rain_model.py
```

Terminal 1 — backend:

```powershell
uvicorn backend.main:app --reload
```

Terminal 2 — dashboard:

```powershell
streamlit run frontendpp.py
```

Open the Streamlit URL shown in the terminal, normally `http://localhost:8501`.

Backend API docs:

`http://127.0.0.1:8000/docs`

## API endpoints

- `GET /api/health`
- `POST /api/predict`
- `POST /api/telemetry`
- `GET /api/telemetry`
- `GET /api/analytics/summary`

## ML model

The included training script creates a reproducible synthetic dataset and trains a Random Forest classifier with these features:

- load ratio
- maximum distribution error
- sensor cross-validation error
- loading rate
- maintenance risk

Labels:

- SAFE
- CAUTION
- CRITICAL

This is a **demonstration model**, not a certified railway safety model. Replace the synthetic training data with validated operational/sensor data before real-world deployment.

## GitHub

```powershell
git init
git branch -M main
git add .
git commit -m "Build Coal Wagon SmartLoad full-stack platform"
git remote add origin https://github.com/YOUR-USERNAME/COAL-WAGON-SMARTLOAD.git
git push -u origin main
```

If the remote already contains a commit:

```powershell
git pull origin main --allow-unrelated-histories
git add .
git commit -m "Merge remote repository"
git push -u origin main
```