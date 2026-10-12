import os
import requests

BACKEND_URL = os.getenv("SMARTLOAD_BACKEND_URL", "http://127.0.0.1:8000")

def health():
    return requests.get(f"{BACKEND_URL}/api/health", timeout=2).json()

def predict(payload):
    return requests.post(f"{BACKEND_URL}/api/predict", json=payload, timeout=3).json()

def save_telemetry(payload):
    return requests.post(f"{BACKEND_URL}/api/telemetry", json=payload, timeout=3).json()

def analytics():
    return requests.get(f"{BACKEND_URL}/api/analytics/summary", timeout=2).json()
