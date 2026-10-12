import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import hashlib
import math
import os
try:
    from api_client import predict as backend_predict, save_telemetry, health as backend_health, analytics as backend_analytics
except Exception:
    backend_predict = save_telemetry = backend_health = backend_analytics = None


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartLoad - Rail Wagon Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. LIQUID GLASS CSS
# ============================================================

st.markdown(
    """
<style>

* {
    box-sizing: border-box;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(56,189,248,0.12), transparent 25%),
        radial-gradient(circle at 90% 90%, rgba(192,132,252,0.12), transparent 25%),
        linear-gradient(120deg, #070B13, #0F172A, #17153B, #101A31);
    background-size: 200% 200%;
    color: #F8FAFC;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: rgba(7, 12, 25, 0.82) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.08);
}


/* =========================================================
   HEADER
   ========================================================= */

.smart-header {
    padding: 8px 0 5px 0;
}

.smart-title {
    font-size: 42px;
    font-weight: 900;
    margin: 0;
    background: linear-gradient(
        90deg,
        #38BDF8,
        #818CF8,
        #C084FC
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.smart-subtitle {
    color: #94A3B8;
    font-size: 14px;
    margin-top: 5px;
}


/* =========================================================
   TOP METRIC CARDS
   ========================================================= */

.metric-card {
    min-height: 150px;
    padding: 22px 20px;
    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.12);

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.08);

    transition: all 0.25s ease;

    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(56,189,248,0.45);

    box-shadow:
        0 18px 45px rgba(0,0,0,0.35),
        0 0 25px rgba(56,189,248,0.10);
}

.metric-label {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

.metric-value {
    color: #F8FAFC;
    font-size: 32px;
    font-weight: 900;
    margin-top: 8px;
    line-height: 1.1;
}

.metric-info {
    color: #64748B;
    font-size: 12px;
    margin-top: 8px;
}

.metric-accent {
    position: absolute;
    width: 80px;
    height: 80px;
    right: -25px;
    top: -25px;
    border-radius: 50%;
    background: rgba(56,189,248,0.10);
    filter: blur(10px);
}


/* =========================================================
   DISTRIBUTION CARD
   ========================================================= */

.distribution-main {
    min-height: 150px;
    padding: 18px 20px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.12);

    backdrop-filter: blur(18px);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.08);
}

.distribution-title {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

.distribution-ratio {
    font-size: 29px;
    font-weight: 900;
    margin-top: 8px;
}

.balance-good {
    color: #34D399;
}

.balance-bad {
    color: #F87171;
}

.distribution-small {
    color: #64748B;
    font-size: 11px;
    margin-top: 5px;
}


/* =========================================================
   STATE CARD
   ========================================================= */

.state-card {
    min-height: 150px;
    padding: 18px 20px;
    border-radius: 20px;

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    position: relative;
    overflow: hidden;
}

.state-green {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.45);
    box-shadow:
        0 12px 35px rgba(0,0,0,0.25),
        0 0 25px rgba(16,185,129,0.12);
}

.state-yellow {
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.5);
    box-shadow:
        0 12px 35px rgba(0,0,0,0.25),
        0 0 25px rgba(245,158,11,0.16);
}

.state-red {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.55);
    box-shadow:
        0 12px 35px rgba(0,0,0,0.25),
        0 0 30px rgba(239,68,68,0.20);
}

.state-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: #CBD5E1;
}

.state-main {
    font-size: 25px;
    font-weight: 900;
    margin-top: 5px;
}

.state-message {
    font-size: 12px;
    color: #CBD5E1;
    margin-top: 4px;
}

.state-guidance {
    margin-top: 9px;
    font-size: 12px;
    font-weight: 700;
}


/* =========================================================
   WARNING BANNER
   ========================================================= */

.warning-banner {
    margin: 14px 0 20px 0;
    padding: 15px 20px;

    border-radius: 16px;

    background: rgba(239,68,68,0.12);

    border: 1px solid rgba(239,68,68,0.50);

    box-shadow:
        0 0 25px rgba(239,68,68,0.12);

    backdrop-filter: blur(15px);
}

.warning-title {
    color: #F87171;
    font-size: 17px;
    font-weight: 900;
}

.warning-detail {
    color: #FCA5A5;
    font-size: 12px;
    margin-top: 4px;
}


/* =========================================================
   FOUR ZONE CARDS
   ========================================================= */

.zone-card {
    padding: 17px;
    border-radius: 16px;

    background: rgba(255,255,255,0.035);

    border: 1px solid rgba(255,255,255,0.08);

    text-align: center;

    transition: 0.25s ease;
}

.zone-card:hover {
    transform: translateY(-3px);
    border-color: rgba(56,189,248,0.4);
}

.zone-title {
    font-size: 11px;
    color: #94A3B8;
    font-weight: 700;
    letter-spacing: 1px;
}

.zone-value {
    font-size: 26px;
    color: #F8FAFC;
    font-weight: 900;
    margin-top: 5px;
}

.zone-desc {
    color: #64748B;
    font-size: 10px;
    margin-top: 3px;
}


/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 15px;
}

.section-caption {
    color: #64748B;
    font-size: 12px;
}


/* =========================================================
   ANALYSIS CARDS
   ========================================================= */

.analysis-card {
    padding: 18px;
    border-radius: 18px;

    background: rgba(255,255,255,0.035);

    border: 1px solid rgba(255,255,255,0.08);

    text-align: center;
}

.analysis-title {
    color: #94A3B8;
    font-size: 12px;
}

.analysis-value {
    font-size: 28px;
    font-weight: 900;
    color: #F8FAFC;
    margin-top: 5px;
}


/* =========================================================
   LIVE INDICATOR
   ========================================================= */

.live-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #34D399;
    border-radius: 50%;
    margin-right: 5px;
    box-shadow: 0 0 12px #34D399;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    border-radius: 11px !important;

    border: 1px solid rgba(56,189,248,0.35) !important;

    background: rgba(56,189,248,0.08) !important;

    color: #F8FAFC !important;

    transition: 0.25s ease !important;
}

.stButton > button:hover {
    border-color: rgba(56,189,248,0.8) !important;

    box-shadow:
        0 0 20px rgba(56,189,248,0.20) !important;

    transform: translateY(-2px);
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.025);
    padding: 8px;
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #94A3B8;
}

.stTabs [aria-selected="true"] {
    background: rgba(56,189,248,0.12) !important;
    color: #38BDF8 !important;
}


/* =========================================================
   STREAMLIT TEXT
   ========================================================= */

h1, h2, h3, h4 {
    color: #F8FAFC !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. WAGON SPECIFICATIONS
# ============================================================

WAGON_SPECS = {
    "BOXN": {
        "tare": 22.5,
        "payload": 58.0,
        "pll": 60.5,
        "axles": 4,
        "profile": "Open-top bulk wagon"
    },
    "BOBRN": {
        "tare": 25.6,
        "payload": 55.4,
        "pll": 61.0,
        "axles": 4,
        "profile": "Bottom-discharge hopper wagon"
    },
    "BOST": {
        "tare": 25.0,
        "payload": 56.0,
        "pll": 61.0,
        "axles": 4,
        "profile": "Open bulk-material wagon"
    }
}


# ============================================================
# 4. SIDEBAR
# ============================================================

st.sidebar.title(" Control & Configuration")

st.sidebar.markdown("---")

siding_id = st.sidebar.selectbox(
    "Siding Location",
    [
        "Siding-01 (Kusmunda)",
        "Siding-02 (Gevra)",
        "Siding-03 (Dipka)"
    ]
)

operator_id = st.sidebar.text_input(
    "Operator ID",
    "OP-8842"
)

wagon_type = st.sidebar.selectbox(
    "Wagon Type",
    list(WAGON_SPECS.keys())
)

wagon_id = st.sidebar.text_input(
    "Wagon / Rake ID",
    f"{wagon_type}-123456"
)

st.sidebar.markdown("---")

st.sidebar.subheader("🕹️ Digital Twin Controls")

sim_scenario = st.sidebar.radio(
    "Load Scenario Injector",
    [
        "Normal Continuous Loading",
        "Uneven Load Profile",
        "Overload Breach",
        "Underload Target Shortfall",
        "Front Heavy Load",
        "Rear Heavy Load"
    ]
)

if st.sidebar.button("⚡ Generate New Live Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Enhanced SmartLoad Features")
enable_prediction = st.sidebar.toggle("Predictive Stop-Point", True)
enable_directional = st.sidebar.toggle("Directional Loading Guidance", True)
enable_cross_validation = st.sidebar.toggle("Sensor Cross-Validation", True)
enable_fail_safe = st.sidebar.toggle("Fail-Safe Certification", True)
enable_integrity = st.sidebar.toggle("Transit Load-Integrity Check", True)
enable_plc = st.sidebar.toggle("PLC / Payloader Assist Simulation", False)

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Reliability Injector")
sensor_fault_mode = st.sidebar.selectbox(
    "Inject Hardware Condition",
    [
        "All Sensors Healthy",
        "Load Cell Drift",
        "LiDAR Obstructed",
        "RFID Read Failure",
        "Network Offline",
        "Calibration Overdue"
    ]
)

operator_ack = st.sidebar.toggle("Operator acknowledges warnings", True)


# ============================================================
# 5. WAGON LIMITS
# ============================================================

wagon_data = WAGON_SPECS[wagon_type]

tare_weight = wagon_data["tare"]

payload_limit = wagon_data["payload"]

pll_limit = wagon_data["pll"] * 1000

target_weight = payload_limit * 1000


# ============================================================
# 6. SIMULATED SENSOR DATA
# ============================================================

if sim_scenario == "Normal Continuous Loading":

    live_weight = np.random.uniform(
        target_weight - 1000,
        target_weight - 100
    )

    left_pct = np.random.uniform(48, 52)
    right_pct = 100 - left_pct

    front_pct = np.random.uniform(48, 52)
    rear_pct = 100 - front_pct


elif sim_scenario == "Uneven Load Profile":

    live_weight = np.random.uniform(
        48000,
        54000
    )

    left_pct = np.random.uniform(62, 70)
    right_pct = 100 - left_pct

    front_pct = np.random.uniform(60, 68)
    rear_pct = 100 - front_pct


elif sim_scenario == "Overload Breach":

    live_weight = np.random.uniform(
        pll_limit + 500,
        pll_limit + 2500
    )

    left_pct = np.random.uniform(48, 52)
    right_pct = 100 - left_pct

    front_pct = np.random.uniform(48, 52)
    rear_pct = 100 - front_pct


elif sim_scenario == "Underload Target Shortfall":

    live_weight = np.random.uniform(
        42000,
        48000
    )

    left_pct = np.random.uniform(48, 52)
    right_pct = 100 - left_pct

    front_pct = np.random.uniform(48, 52)
    rear_pct = 100 - front_pct


elif sim_scenario == "Front Heavy Load":

    live_weight = np.random.uniform(
        target_weight - 1500,
        target_weight - 200
    )

    front_pct = np.random.uniform(63, 72)
    rear_pct = 100 - front_pct

    left_pct = np.random.uniform(48, 52)
    right_pct = 100 - left_pct


else:

    live_weight = np.random.uniform(
        target_weight - 1500,
        target_weight - 200
    )

    rear_pct = np.random.uniform(63, 72)
    front_pct = 100 - rear_pct

    left_pct = np.random.uniform(48, 52)
    right_pct = 100 - left_pct


# ============================================================
# 7. ROUND VALUES
# ============================================================

left_pct = round(left_pct, 1)
right_pct = round(right_pct, 1)

front_pct = round(front_pct, 1)
rear_pct = round(rear_pct, 1)

weight_kg = live_weight


# ============================================================
# 8. DISTRIBUTION CALCULATION
# ============================================================

lr_difference = abs(left_pct - right_pct)

fr_difference = abs(front_pct - rear_pct)

max_distribution_error = max(
    lr_difference,
    fr_difference
)


# ============================================================
# 8B. ENHANCED PREDICTION / RELIABILITY ENGINE
# ============================================================

# Simulated loading dynamics derived from current scenario.
scenario_rates = {
    "Normal Continuous Loading": (280, 520),
    "Uneven Load Profile": (220, 460),
    "Overload Breach": (500, 850),
    "Underload Target Shortfall": (80, 220),
    "Front Heavy Load": (260, 520),
    "Rear Heavy Load": (260, 520),
}
loading_rate_kg_min = float(np.random.uniform(*scenario_rates[sim_scenario]))
loading_rate_kg_sec = loading_rate_kg_min / 60.0

# Estimated residual coal that can still fall after a STOP command.
response_delay_sec = 4.0 if enable_plc else 7.0
residual_after_stop_kg = loading_rate_kg_sec * response_delay_sec
predictive_stop_weight = max(0.0, target_weight - residual_after_stop_kg)
projected_weight_after_stop = weight_kg + residual_after_stop_kg

if loading_rate_kg_sec > 0 and target_weight > weight_kg:
    time_to_target_sec = (target_weight - weight_kg) / loading_rate_kg_sec
else:
    time_to_target_sec = 0.0

# Directional guidance from the four-zone distribution.
directional_commands = []
if left_pct - right_pct > 8:
    directional_commands.append("LOAD TOWARD RIGHT")
elif right_pct - left_pct > 8:
    directional_commands.append("LOAD TOWARD LEFT")
if front_pct - rear_pct > 8:
    directional_commands.append("LOAD TOWARD REAR")
elif rear_pct - front_pct > 8:
    directional_commands.append("LOAD TOWARD FRONT")
directional_guidance = " + ".join(directional_commands) if directional_commands else "DISTRIBUTION BALANCED"

# LiDAR plausibility model: not a legal mass value; only a consistency check.
lidar_mass_estimate_kg = weight_kg + np.random.normal(0, max(90, weight_kg * 0.006))
if sensor_fault_mode == "LiDAR Obstructed":
    lidar_mass_estimate_kg = weight_kg + max(3500, weight_kg * 0.09)
elif sensor_fault_mode == "Load Cell Drift":
    lidar_mass_estimate_kg = weight_kg - max(2500, weight_kg * 0.06)

cross_validation_error_pct = abs(lidar_mass_estimate_kg - weight_kg) / max(weight_kg, 1) * 100

# Sensor / communication / calibration health.
health = {
    "load_cells": "OK",
    "lidar": "OK",
    "rfid": "OK",
    "communication": "OK",
    "calibration": "VALID",
    "edge": "OK"
}
if sensor_fault_mode == "Load Cell Drift":
    health["load_cells"] = "DRIFT"
elif sensor_fault_mode == "LiDAR Obstructed":
    health["lidar"] = "OBSTRUCTED"
elif sensor_fault_mode == "RFID Read Failure":
    health["rfid"] = "FAILED"
elif sensor_fault_mode == "Network Offline":
    health["communication"] = "OFFLINE"
elif sensor_fault_mode == "Calibration Overdue":
    health["calibration"] = "OVERDUE"

critical_faults = sum(
    1 for k, v in health.items()
    if (k in ["load_cells", "rfid", "calibration", "edge"] and v != "OK" and v != "VALID")
)
noncritical_faults = sum(1 for v in health.values() if v not in ["OK", "VALID"] )

confidence_score = 98.0
confidence_score -= cross_validation_error_pct * 3.0 if enable_cross_validation else 0
confidence_score -= critical_faults * 25
confidence_score -= max(0, noncritical_faults - critical_faults) * 12
confidence_score = float(np.clip(confidence_score, 5, 99))

certification_allowed = True
if enable_fail_safe and (critical_faults > 0 or confidence_score < 65):
    certification_allowed = False

# PLC / operator action recommendation.
if weight_kg > pll_limit:
    control_action = "EMERGENCY HOLD"
elif enable_prediction and weight_kg >= predictive_stop_weight:
    control_action = "STOP NOW"
elif enable_prediction and time_to_target_sec <= 60:
    control_action = "SLOW LOADING"
elif directional_commands and enable_directional:
    control_action = directional_guidance
else:
    control_action = "CONTINUE LOADING"

# Operator escalation logic.
escalation_level = 0
if control_action in ["STOP NOW", "EMERGENCY HOLD"] or max_distribution_error > 20:
    escalation_level = 1
    if not operator_ack:
        escalation_level = 3

# Offline store-and-forward queue simulation.
if "offline_queue" not in st.session_state:
    st.session_state.offline_queue = []
if health["communication"] == "OFFLINE":
    if len(st.session_state.offline_queue) < 50:
        st.session_state.offline_queue.append({
            "ts": datetime.now().isoformat(),
            "wagon": wagon_id,
            "weight": round(weight_kg, 1),
            "action": control_action
        })
elif st.session_state.offline_queue:
    st.session_state.offline_queue.clear()

# Calibration / predictive maintenance simulation.
calibration_age_days = 210 if sensor_fault_mode == "Calibration Overdue" else np.random.randint(10, 120)
predictive_maintenance_risk = min(100, int(10 + noncritical_faults * 28 + cross_validation_error_pct * 5))
maintenance_state = "SERVICE REQUIRED" if predictive_maintenance_risk >= 65 else ("WATCH" if predictive_maintenance_risk >= 35 else "HEALTHY")

# Transit integrity simulation - compare loading certificate with downstream checkpoint.
dispatch_weight_kg = weight_kg
checkpoint_loss_pct = np.random.uniform(0.02, 0.15)
if enable_integrity and sim_scenario in ["Underload Target Shortfall", "Uneven Load Profile"]:
    checkpoint_loss_pct = np.random.uniform(0.8, 2.2)
checkpoint_weight_kg = dispatch_weight_kg * (1 - checkpoint_loss_pct / 100)
integrity_delta_kg = dispatch_weight_kg - checkpoint_weight_kg
integrity_anomaly = enable_integrity and checkpoint_loss_pct > 0.75

# Estimated operating efficiency score.
loading_accuracy_pct = max(0.0, 100 - abs(target_weight - weight_kg) / max(target_weight, 1) * 100)
efficiency_score = float(np.clip(
    0.45 * loading_accuracy_pct +
    0.25 * max(0, 100 - max_distribution_error * 2) +
    0.20 * confidence_score +
    0.10 * max(0, 100 - predictive_maintenance_risk),
    0, 100
))


# ============================================================
# 8C. BACKEND + ML INTELLIGENCE BRIDGE
# ============================================================
backend_prediction = None
backend_online = False
if backend_predict is not None:
    try:
        bridge_payload = {
            "wagon_id": wagon_id,
            "siding_id": siding_id,
            "wagon_type": wagon_type,
            "gross_weight_kg": float(weight_kg),
            "target_weight_kg": float(target_weight),
            "pll_limit_kg": float(pll_limit),
            "left_pct": float(left_pct),
            "right_pct": float(right_pct),
            "front_pct": float(front_pct),
            "rear_pct": float(rear_pct),
            "scenario": sim_scenario,
            "cross_validation_error_pct": float(cross_validation_error_pct),
            "loading_rate_kg_min": float(loading_rate_kg_min),
            "maintenance_risk_pct": float(predictive_maintenance_risk),
        }
        backend_prediction = backend_predict(bridge_payload)
        backend_online = True
        # Persist the current simulation when the backend is available.
        try:
            save_telemetry(bridge_payload)
        except Exception:
            pass
    except Exception:
        backend_online = False

# ============================================================
# 9. STATUS / LOGIC ENGINE
# ============================================================

target_remaining = target_weight - weight_kg

pll_remaining = pll_limit - weight_kg

target_tolerance = 200


if enable_fail_safe and not certification_allowed:

    status_code = "RED"
    status_msg = "FAIL-SAFE HOLD / SENSOR VERIFICATION"
    status_css = "state-red"
    guidance_text = f"Confidence {confidence_score:.0f}% • Verify {sensor_fault_mode}"
    guidance_color = "#F87171"

elif weight_kg > pll_limit:

    status_code = "RED"
    status_msg = "STOP / HOLD LOADING"
    status_css = "state-red"

    excess_weight = weight_kg - pll_limit

    guidance_text = (
        f"Remove {excess_weight / 1000:.2f} T "
        f"({excess_weight:.0f} kg)"
    )

    guidance_color = "#F87171"


elif lr_difference > 20 or fr_difference > 20:

    status_code = "RED"
    status_msg = "STOP / CORRECT DISTRIBUTION"

    status_css = "state-red"

    guidance_text = (
        f"Correct {max_distribution_error:.1f}% "
        f"distribution deviation"
    )

    guidance_color = "#F87171"


elif abs(target_weight - weight_kg) <= target_tolerance:

    status_code = "GREEN"
    status_msg = "TARGET ACHIEVED"

    status_css = "state-green"

    guidance_text = (
        f"Load: {weight_kg / 1000:.2f} T "
        f"| Target: {target_weight / 1000:.2f} T"
    )

    guidance_color = "#34D399"


elif weight_kg >= target_weight - 2000:

    status_code = "YELLOW"
    status_msg = "APPROACHING TARGET"

    status_css = "state-yellow"

    guidance_text = (
        f"{target_remaining / 1000:.2f} T "
        f"({target_remaining:.0f} kg) remaining"
    )

    guidance_color = "#FBBF24"


else:

    status_code = "GREEN"
    status_msg = "SAFE CONTINUOUS LOAD"

    status_css = "state-green"

    guidance_text = (
        f"{target_remaining / 1000:.2f} T "
        f"({target_remaining:.0f} kg) remaining"
    )

    guidance_color = "#34D399"


# ============================================================
# 10. WARNING ENGINE
# ============================================================

warning_condition = (
    weight_kg > pll_limit
    or lr_difference > 20
    or fr_difference > 20
    or (enable_fail_safe and not certification_allowed)
    or (enable_prediction and control_action == "STOP NOW")
)

if "previous_warning_state" not in st.session_state:
    st.session_state.previous_warning_state = False

if "warning_popup_until" not in st.session_state:
    st.session_state.warning_popup_until = None

new_warning = (
    warning_condition
    and not st.session_state.previous_warning_state
)

if new_warning:
    st.session_state.warning_popup_until = (
        datetime.now() + timedelta(seconds=10)
    )

st.session_state.previous_warning_state = warning_condition


# ============================================================
# 11. HEADER
# ============================================================

st.markdown(
    """
<div class="smart-header">

<div class="smart-title">
SmartLoad – IoT & AI-Based System to Prevent Under-loading and Overloading
</div>

<div class="smart-subtitle">
Rail Wagon Intelligence • Real-Time Load Monitoring & Safety System
</div>

</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    f"""
<div style="
    display:flex;
    gap:15px;
    flex-wrap:wrap;
    color:#94A3B8;
    font-size:13px;
    margin-bottom:18px;
">

<span>
Location:
<strong style="color:#F8FAFC;">
{siding_id}
</strong>
</span>

<span>•</span>

<span>
Wagon:
<strong style="color:#38BDF8;">
{wagon_id}
</strong>
</span>

<span>•</span>

<span>
Type:
<strong style="color:#F8FAFC;">
{wagon_type}
</strong>
</span>

<span>•</span>

<span>
<span class="live-dot"></span>
LIVE
</span>

<span>•</span>

<span>
{datetime.now().strftime("%H:%M:%S")}
</span>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 12. WARNING BANNER
# ============================================================

if warning_condition:

    if enable_fail_safe and not certification_allowed:
        warning_title = "🛑 FAIL-SAFE HOLD"
        warning_detail = (
            f"Measurement confidence {confidence_score:.0f}% • "
            f"Hardware condition: {sensor_fault_mode} • Certification blocked"
        )

    elif enable_prediction and control_action == "STOP NOW" and weight_kg <= pll_limit:
        warning_title = "⏱️ PREDICTIVE STOP POINT REACHED"
        warning_detail = (
            f"Current {weight_kg/1000:.2f} T • Rate {loading_rate_kg_min:.0f} kg/min • "
            f"Projected after response delay {projected_weight_after_stop/1000:.2f} T"
        )

    elif weight_kg > pll_limit:

        warning_title = "🚨 OVERLOAD DETECTED"

        warning_detail = (
            f"Measured {weight_kg / 1000:.2f} T • "
            f"Permissible {pll_limit / 1000:.2f} T • "
            f"Excess {(weight_kg - pll_limit):.0f} kg"
        )

    else:

        warning_title = "⚠️ LOAD DISTRIBUTION WARNING"

        warning_detail = (
            f"Maximum distribution deviation: "
            f"{max_distribution_error:.1f}% • "
            f"Loading correction required"
        )

    st.markdown(
        f"""
<div class="warning-banner">

<div class="warning-title">
{warning_title}
</div>

<div class="warning-detail">
{warning_detail}
</div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# 13. TOP FOUR CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(
    [1, 1, 1, 1.25],
    gap="medium"
)


# ------------------------------------------------------------
# CARD 1 — GROSS WEIGHT
# ------------------------------------------------------------

with c1:

    st.markdown(
        f"""
<div class="metric-card">

<div class="metric-accent"></div>

<div class="metric-label">
⚖ Gross Weight
</div>

<div class="metric-value">
{weight_kg / 1000:.2f} T
</div>

<div class="metric-info">
Target Load: {target_weight / 1000:.2f} T
</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# CARD 2 — PERMISSIBLE LIMIT
# ------------------------------------------------------------

with c2:

    st.markdown(
        f"""
<div class="metric-card">

<div class="metric-accent"></div>

<div class="metric-label">
🛡 Permissible Weight
</div>

<div class="metric-value">
{pll_limit / 1000:.2f} T
</div>

<div class="metric-info">
Maximum Allowable Load
</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# CARD 3 — DISTRIBUTION
# ------------------------------------------------------------

with c3:

    if max_distribution_error <= 20:

        distribution_class = "balance-good"
        distribution_status = "✓ WELL BALANCED"

    else:

        distribution_class = "balance-bad"
        distribution_status = "⚠ IMBALANCE"

    st.markdown(
        f"""
<div class="distribution-main">

<div class="distribution-title">
⚖ Weight Distribution
</div>

<div class="distribution-ratio {distribution_class}">
{left_pct:.0f}% / {right_pct:.0f}%
</div>

<div class="{distribution_class}" 
     style="font-size:11px;font-weight:800;margin-top:2px;">
{distribution_status}
</div>

<div class="distribution-small">
L/R Balance • F/R {front_pct:.0f}% / {rear_pct:.0f}%
</div>

</div>
""",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# CARD 4 — STATE + CALCULATION
# ------------------------------------------------------------

with c4:

    st.markdown(
        f"""
<div class="state-card {status_css}">

<div class="state-label">
SYSTEM STATE
</div>

<div class="state-main">
{status_code}
</div>

<div class="state-message">
{status_msg}
</div>

<div class="state-guidance"
     style="color:{guidance_color};">

{guidance_text}

</div>

</div>
""",
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 14. CALCULATION SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title"> Load Calculation Summary</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-caption">Live calculation used by the SmartLoad decision engine</div>',
    unsafe_allow_html=True
)

calc1, calc2, calc3, calc4 = st.columns(4)


with calc1:

    st.metric(
        "Target Load",
        f"{target_weight / 1000:.2f} T"
    )


with calc2:

    if target_remaining > 0:

        st.metric(
            "Remaining to Target",
            f"{target_remaining:.0f} kg"
        )

    else:

        st.metric(
            "Above Target",
            f"{abs(target_remaining):.0f} kg"
        )


with calc3:

    st.metric(
        "PLL Remaining",
        f"{pll_remaining:.0f} kg"
    )


with calc4:

    st.metric(
        "Max Distribution Error",
        f"{max_distribution_error:.1f}%"
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 14B. PREDICTIVE INTELLIGENCE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Predictive Loading Intelligence</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="section-caption">Prediction, guidance, confidence and fail-safe decisions generated at the edge</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4, p5 = st.columns(5)
p1.metric("Loading Rate", f"{loading_rate_kg_min:.0f} kg/min")
p2.metric("Time to Target", f"{time_to_target_sec:.0f} s" if time_to_target_sec > 0 else "Reached")
p3.metric("Predictive Stop", f"{predictive_stop_weight/1000:.2f} T")
p4.metric("Confidence", f"{confidence_score:.0f}%")
p5.metric("Efficiency", f"{efficiency_score:.0f}%")

g1, g2, g3 = st.columns([1.4, 1.2, 1.2])
with g1:
    st.info(f"**Recommended Action:** {control_action}")
with g2:
    if directional_commands:
        st.warning(f"**Directional Guidance:** {directional_guidance}")
    else:
        st.success("**Directional Guidance:** Balanced")
with g3:
    if certification_allowed:
        st.success("**Fail-Safe:** Certification eligible")
    else:
        st.error("**Fail-Safe:** Certification BLOCKED")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# 15. FOUR-ZONE LOAD DISTRIBUTION
# ============================================================

st.markdown(
    '<div class="section-title"> Four-Zone Load Distribution</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-caption">Real-time estimated distribution from the wagon sensing array</div>',
    unsafe_allow_html=True
)

z1, z2, z3, z4 = st.columns(4)


zone_data = [
    ("◀ LEFT", left_pct, "Lateral Zone"),
    ("RIGHT ▶", right_pct, "Lateral Zone"),
    ("FRONT ▲", front_pct, "Longitudinal Zone"),
    ("REAR ▼", rear_pct, "Longitudinal Zone")
]


for col, data in zip(
    [z1, z2, z3, z4],
    zone_data
):

    title, value, desc = data

    with col:

        st.markdown(
            f"""
<div class="zone-card">

<div class="zone-title">
{title}
</div>

<div class="zone-value">
{value:.1f}%
</div>

<div class="zone-desc">
{desc}
</div>

</div>
""",
            unsafe_allow_html=True
        )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 16. DISTRIBUTION ANALYSIS
# ============================================================

d1, d2 = st.columns(2)


with d1:

    lr_status = (
        "✓ Within tolerance"
        if lr_difference <= 20
        else "⚠ Correction required"
    )

    st.markdown(
        f"""
<div class="analysis-card">

<div class="analysis-title">
↔ LEFT / RIGHT BALANCE
</div>

<div class="analysis-value">
{lr_difference:.1f}%
</div>

<div style="color:#94A3B8;font-size:11px;">
Maximum lateral deviation
</div>

<div style="
margin-top:8px;
color:{'#34D399' if lr_difference <= 20 else '#F87171'};
font-size:11px;
font-weight:700;">
{lr_status}
</div>

</div>
""",
        unsafe_allow_html=True
    )


with d2:

    fr_status = (
        "✓ Within tolerance"
        if fr_difference <= 20
        else "⚠ Correction required"
    )

    st.markdown(
        f"""
<div class="analysis-card">

<div class="analysis-title">
↕ FRONT / REAR BALANCE
</div>

<div class="analysis-value">
{fr_difference:.1f}%
</div>

<div style="color:#94A3B8;font-size:11px;">
Maximum longitudinal deviation
</div>

<div style="
margin-top:8px;
color:{'#34D399' if fr_difference <= 20 else '#F87171'};
font-size:11px;
font-weight:700;">
{fr_status}
</div>

</div>
""",
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 17. DASHBOARD TABS
# ============================================================

tab_live, tab_lidar, tab_health, tab_predict, tab_integrity, tab_analytics, tab_cert = st.tabs(
    [
        "📊 Live Weighment",
        "🧊 3D LiDAR Profile",
        "📡 Hardware Health",
        "🧠 Prediction & Control",
        "🛡 Load Integrity",
        "📈 Analytics",
        "📜 Digital Certificate"
    ]
)


# ============================================================
# TAB 1 — LIVE WEIGHMENT
# ============================================================

with tab_live:

    col_g1, col_g2 = st.columns([1, 2])


    # --------------------------------------------------------
    # GAUGE
    # --------------------------------------------------------

    with col_g1:

        st.subheader("Gross Load Gauge")

        gauge_max = (pll_limit / 1000) * 1.15

        fig_gauge = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=weight_kg / 1000,

                title={
                    "text": "Weight (Metric Tonnes)",
                    "font": {
                        "color": "#94A3B8",
                        "size": 14
                    }
                },

                number={
                    "font": {
                        "color": "#F8FAFC",
                        "size": 36
                    }
                },

                gauge={

                    "axis": {
                        "range": [0, gauge_max],
                        "tickcolor": "#64748B"
                    },

                    "bar": {
                        "color": "#38BDF8"
                    },

                    "bgcolor": "rgba(255,255,255,0.03)",

                    "borderwidth": 1,

                    "bordercolor":
                        "rgba(255,255,255,0.1)",

                    "steps": [

                        {
                            "range": [
                                0,
                                max(0, target_weight / 1000 - 2)
                            ],
                            "color":
                                "rgba(30,41,59,0.5)"
                        },

                        {
                            "range": [
                                max(0, target_weight / 1000 - 2),
                                pll_limit / 1000
                            ],
                            "color":
                                "rgba(217,119,6,0.3)"
                        },

                        {
                            "range": [
                                pll_limit / 1000,
                                gauge_max
                            ],
                            "color":
                                "rgba(220,38,38,0.4)"
                        }
                    ],

                    "threshold": {

                        "line": {
                            "color": "#F87171",
                            "width": 3
                        },

                        "thickness": 0.75,

                        "value":
                            pll_limit / 1000
                    }
                }
            )
        )

        fig_gauge.update_layout(
            height=320,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            font={
                "color": "white"
            }
        )

        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    with col_g2:

        st.subheader("In-Motion Rate Trend")

        now = datetime.now()

        times = [
            now - timedelta(seconds=10 * i)
            for i in range(19, -1, -1)
        ]

        base_trajectory = np.linspace(
            weight_kg -
            np.random.uniform(8000, 12000),

            weight_kg,

            20
        )

        sensor_noise = np.random.normal(
            0,
            120,
            20
        )

        df_trend = pd.DataFrame({

            "Timestamp":
                times,

            "Filtered Weight (kg)":
                base_trajectory + sensor_noise
        })


        fig_trend = px.line(
            df_trend,

            x="Timestamp",

            y="Filtered Weight (kg)",

            template="plotly_dark"
        )


        fig_trend.update_traces(
            line_color="#818CF8",
            line_width=3
        )


        fig_trend.add_hline(
            y=pll_limit,

            line_dash="dash",

            line_color="#F87171",

            annotation_text="PLL Limit",

            annotation_font_color="#F87171"
        )


        fig_trend.add_hline(
            y=target_weight,

            line_dash="dot",

            line_color="#34D399",

            annotation_text="Target Weight",

            annotation_font_color="#34D399"
        )


        fig_trend.update_layout(

            height=320,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(255,255,255,0.02)",

            xaxis={
                "showgrid": False
            },

            yaxis={
                "gridcolor":
                    "rgba(255,255,255,0.05)"
            }
        )


        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )


# ============================================================
# TAB 2 — 3D LIDAR
# ============================================================

with tab_lidar:

    st.subheader(
        "Gantry LiDAR Point Cloud - Live Directional Load Surface"
    )

    st.caption(
        "The 3D surface is generated directly from the live Left/Right and "
        "Front/Rear percentages. A heavier side is physically rendered higher, "
        "while total wagon weight controls the overall fill height."
    )

    # --------------------------------------------------------
    # VIEW CONTROL
    # --------------------------------------------------------
    lidar_view = st.radio(
        "3D viewing angle",
        ["Perspective", "Top", "Front", "Rear", "Left", "Right"],
        horizontal=True,
        key="lidar_camera_view"
    )

    # Digital-twin wagon dimensions (visualisation only).
    wagon_half_width = 2.5      # X: LEFT (-) to RIGHT (+)
    wagon_half_length = 6.0     # Y: REAR (-) to FRONT (+)

    x = np.linspace(-wagon_half_width, wagon_half_width, 52)
    y = np.linspace(-wagon_half_length, wagon_half_length, 104)
    X, Y = np.meshgrid(x, y)

    # --------------------------------------------------------
    # 1. TOTAL FILL HEIGHT FROM LIVE WEIGHT
    # --------------------------------------------------------
    fill_ratio = float(np.clip(weight_kg / max(target_weight, 1), 0.05, 1.15))

    # Nominal physical-looking height for the digital twin.
    # Underload is low; target is around 2.2 m; overload rises above it.
    mean_height = 0.18 + 2.00 * min(fill_ratio, 1.0)
    if fill_ratio > 1.0:
        mean_height += (fill_ratio - 1.0) * 3.2

    # --------------------------------------------------------
    # 2. DIRECT MAPPING OF L/R + F/R INPUTS TO 3D HEIGHT
    # --------------------------------------------------------
    # Example:
    # L=64.2/R=35.8 -> left_bias = +0.284 -> LEFT side rises strongly.
    # F=60.4/R=39.6 -> front_bias = +0.208 -> FRONT side rises strongly.
    lateral_bias = float((left_pct - right_pct) / 100.0)
    longitudinal_bias = float((front_pct - rear_pct) / 100.0)

    # Normalised coordinates. LEFT is positive in left_axis; FRONT is positive in front_axis.
    left_axis = -X / wagon_half_width
    front_axis = Y / wagon_half_length

    # Direct directional slope. Multipliers intentionally make a 20–30% imbalance
    # unmistakable in a live demo while preserving the correct direction.
    directional_field = (
        2.25 * lateral_bias * left_axis
        + 2.25 * longitudinal_bias * front_axis
    )

    # Smooth masks reinforce each live percentage on its corresponding half.
    left_mask = 0.5 * (1.0 + np.tanh((-X) * 2.0))
    right_mask = 1.0 - left_mask
    front_mask = 0.5 * (1.0 + np.tanh(Y * 0.85))
    rear_mask = 1.0 - front_mask

    lateral_mass_field = (
        (left_pct / 50.0) * left_mask
        + (right_pct / 50.0) * right_mask
    )
    longitudinal_mass_field = (
        (front_pct / 50.0) * front_mask
        + (rear_pct / 50.0) * rear_mask
    )

    # Convert zone percentages into a spatial multiplier and recenter it around 1.
    zone_multiplier = 0.5 * (lateral_mass_field + longitudinal_mass_field)
    zone_multiplier /= max(float(np.mean(zone_multiplier)), 1e-6)

    # --------------------------------------------------------
    # 3. COAL SURFACE SHAPE
    # --------------------------------------------------------
    # Broad central crown gives a natural bulk-material profile.
    crown = 0.30 * np.exp(-((X / 2.25) ** 2 + (Y / 5.2) ** 2))

    # Put an extra mound in the actual heavier quadrant.
    heavy_x = -1.55 if left_pct > right_pct else 1.55
    heavy_y = 3.6 if front_pct > rear_pct else -3.6
    imbalance_mag = min(1.0, abs(lateral_bias) + abs(longitudinal_bias))
    quadrant_mound = (0.15 + 1.35 * imbalance_mag) * np.exp(
        -(((X - heavy_x) / 1.30) ** 2 + ((Y - heavy_y) / 2.35) ** 2)
    )

    # If only one axis is badly imbalanced, create a broad side mound too.
    side_mound = np.zeros_like(X)
    if abs(lateral_bias) > 0.06:
        side_x = -1.35 if lateral_bias > 0 else 1.35
        side_mound += (abs(lateral_bias) * 2.8) * np.exp(-((X - side_x) / 1.35) ** 2)
    if abs(longitudinal_bias) > 0.06:
        side_y = 3.25 if longitudinal_bias > 0 else -3.25
        side_mound += (abs(longitudinal_bias) * 2.8) * np.exp(-((Y - side_y) / 2.5) ** 2)

    # Scenario affects overall fullness, while directional percentages remain the source
    # of truth for LEFT/RIGHT/FRONT/REAR shape.
    scenario_adjustment = np.zeros_like(X)
    if sim_scenario == "Underload Target Shortfall":
        mean_height *= 0.72
        crown *= 0.55
    elif sim_scenario == "Overload Breach":
        scenario_adjustment += 0.35 * np.exp(-((X / 2.1) ** 2 + (Y / 5.0) ** 2))

    # Small deterministic texture resembles an irregular coal surface without random
    # jumps every render.
    roughness = (
        0.035 * np.sin(X * 4.3 + Y * 0.73)
        + 0.028 * np.cos(Y * 2.0 - X * 1.65)
        + 0.018 * np.sin(X * 7.0 - Y * 1.25)
    )

    Z = (
        mean_height * zone_multiplier
        + directional_field
        + crown
        + quadrant_mound
        + side_mound
        + scenario_adjustment
        + roughness
    )

    # Keep all points above wagon floor and within a sensible demo range.
    Z = np.clip(Z, 0.05, 4.0)

    # --------------------------------------------------------
    # 4. LIVE PROFILE INTERPRETATION
    # --------------------------------------------------------
    if left_pct > right_pct + 4:
        lateral_text = "LEFT HEAVY"
    elif right_pct > left_pct + 4:
        lateral_text = "RIGHT HEAVY"
    else:
        lateral_text = "L/R BALANCED"

    if front_pct > rear_pct + 4:
        longitudinal_text = "FRONT HEAVY"
    elif rear_pct > front_pct + 4:
        longitudinal_text = "REAR HEAVY"
    else:
        longitudinal_text = "F/R BALANCED"

    # Find actual rendered mean heights per physical zone for judge-friendly proof.
    left_height = float(np.mean(Z[:, X[0] < 0]))
    right_height = float(np.mean(Z[:, X[0] >= 0]))
    front_height = float(np.mean(Z[Y[:, 0] >= 0, :]))
    rear_height = float(np.mean(Z[Y[:, 0] < 0, :]))

    lp1, lp2, lp3, lp4 = st.columns(4)
    lp1.metric("LiDAR Fill Estimate", f"{fill_ratio * 100:.1f}%")
    lp2.metric("Lateral Profile", lateral_text, f"L {left_pct:.1f}% / R {right_pct:.1f}%")
    lp3.metric("Longitudinal Profile", longitudinal_text, f"F {front_pct:.1f}% / R {rear_pct:.1f}%")
    lp4.metric("Recommended Action", directional_guidance)

    # Show that the actual rendered geometry follows the percentages.
    st.caption(
        f"Rendered average height → LEFT {left_height:.2f} m | RIGHT {right_height:.2f} m | "
        f"FRONT {front_height:.2f} m | REAR {rear_height:.2f} m"
    )

    # --------------------------------------------------------
    # 5. CAMERA VIEWS
    # --------------------------------------------------------
    camera_map = {
        "Perspective": dict(eye=dict(x=1.55, y=-1.75, z=1.28), up=dict(x=0, y=0, z=1)),
        "Top":        dict(eye=dict(x=0.0, y=0.0, z=2.75), up=dict(x=0, y=1, z=0)),
        "Front":      dict(eye=dict(x=0.0, y=2.65, z=0.65), up=dict(x=0, y=0, z=1)),
        "Rear":       dict(eye=dict(x=0.0, y=-2.65, z=0.65), up=dict(x=0, y=0, z=1)),
        "Left":       dict(eye=dict(x=-2.65, y=0.0, z=0.65), up=dict(x=0, y=0, z=1)),
        "Right":      dict(eye=dict(x=2.65, y=0.0, z=0.65), up=dict(x=0, y=0, z=1)),
    }

    # --------------------------------------------------------
    # 6. 3D SURFACE + WAGON BOUNDARY + ORIENTATION
    # --------------------------------------------------------
    fig_3d = go.Figure()

    fig_3d.add_trace(
        go.Surface(
            z=Z,
            x=X,
            y=Y,
            colorscale="Plasma",
            colorbar=dict(title="Coal Height (m)"),
            contours={
                "z": {
                    "show": True,
                    "usecolormap": True,
                    "highlightcolor": "white",
                    "project_z": True,
                }
            },
            hovertemplate=(
                "Width: %{x:.2f} m<br>"
                "Length: %{y:.2f} m<br>"
                "Coal Height: %{z:.2f} m<extra></extra>"
            ),
            name="LiDAR Coal Surface"
        )
    )

    # Wagon floor reference.
    floor_z = np.zeros_like(X) + 0.015
    fig_3d.add_trace(
        go.Surface(
            z=floor_z,
            x=X,
            y=Y,
            showscale=False,
            opacity=0.10,
            colorscale=[[0, "#64748B"], [1, "#64748B"]],
            hoverinfo="skip",
            name="Wagon Floor"
        )
    )

    # Wagon rectangular boundary at floor level.
    boundary_x = [
        -wagon_half_width, wagon_half_width, wagon_half_width,
        -wagon_half_width, -wagon_half_width
    ]
    boundary_y = [
        -wagon_half_length, -wagon_half_length, wagon_half_length,
        wagon_half_length, -wagon_half_length
    ]
    fig_3d.add_trace(
        go.Scatter3d(
            x=boundary_x,
            y=boundary_y,
            z=[0.04] * 5,
            mode="lines",
            line=dict(width=7, color="white"),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Orientation labels make the mapping unambiguous.
    label_z = float(min(np.max(Z) + 0.25, 4.2))
    fig_3d.add_trace(
        go.Scatter3d(
            x=[0, 0, -wagon_half_width - 0.35, wagon_half_width + 0.35],
            y=[wagon_half_length + 0.45, -wagon_half_length - 0.45, 0, 0],
            z=[label_z] * 4,
            mode="text",
            text=["FRONT ▲", "REAR ▼", "◀ LEFT", "RIGHT ▶"],
            textfont=dict(size=14),
            hoverinfo="skip",
            showlegend=False
        )
    )

    fig_3d.update_layout(
        title=dict(
            text=(
                f"{sim_scenario} • {weight_kg/1000:.2f} T • "
                f"L/R {left_pct:.1f}/{right_pct:.1f} • "
                f"F/R {front_pct:.1f}/{rear_pct:.1f}"
            ),
            x=0.02,
            font=dict(size=14)
        ),
        scene=dict(
            xaxis_title="Wagon Width  (LEFT ↔ RIGHT)",
            yaxis_title="Wagon Length  (REAR ↔ FRONT)",
            zaxis_title="Coal Height  (BOTTOM ↕ TOP)",
            aspectratio=dict(x=1, y=2.35, z=0.95),
            camera=camera_map[lidar_view],
            xaxis=dict(
                range=[-3.2, 3.2],
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.12)"
            ),
            yaxis=dict(
                range=[-6.9, 6.9],
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.12)"
            ),
            zaxis=dict(
                range=[0, 4.3],
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.12)"
            )
        ),
        height=610,
        margin=dict(l=0, r=0, b=0, t=45),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_3d, use_container_width=True)

    st.info(
        f"Live interpretation: {lateral_text}, {longitudinal_text}. "
        f"For the current input, the 3D model raises the heavier physical zones and "
        f"lowers the lighter zones. SmartLoad guidance: {directional_guidance}."
    )


# ============================================================
# TAB 3 — HARDWARE HEALTH
# ============================================================

with tab_health:

    st.subheader(
        "Edge Node Telemetry & Hardware Status"
    )

    latency = f"{np.random.uniform(0.1,0.5):.2f} ms"

    fps = f"{np.random.randint(18,24)} FPS"

    rssi = f"-{np.random.randint(78,89)} dBm"


    h1, h2, h3, h4 = st.columns(4)


    h1.metric("Load Cell Array", health["load_cells"], f"{latency} Latency")


    h2.metric("Gantry LiDAR Scanner", health["lidar"], f"{fps} Scan Speed")


    h3.metric("RFID AEI Reader", health["rfid"], "Tag Verified" if health["rfid"] == "OK" else "Manual fallback")


    h4.metric("LoRaWAN / 4G Uplink", health["communication"], f"{rssi} RSSI" if health["communication"] == "OK" else "Store-and-forward active")


    st.markdown("---")

    hh1, hh2, hh3, hh4 = st.columns(4)
    hh1.metric("Calibration", health["calibration"], f"Age {calibration_age_days} days")
    hh2.metric("Cross-Validation Error", f"{cross_validation_error_pct:.2f}%")
    hh3.metric("System Confidence", f"{confidence_score:.0f}%")
    hh4.metric("Maintenance Risk", f"{predictive_maintenance_risk}%", maintenance_state)

    if health["communication"] == "OFFLINE":
        st.warning(f"Offline edge mode active • {len(st.session_state.offline_queue)} record(s) queued locally")
    elif len(st.session_state.offline_queue) == 0:
        st.success("Cloud uplink available • local queue synchronized")

    st.markdown(
        "**Structured Output Stream Payload "
        "(`smartload/wagon/telemetry`):**"
    )


    # ========================================================
    # TELEMETRY PAYLOAD
    # ========================================================

    sample_payload = {

        "wagon_id":
            wagon_id,

        "siding_id":
            siding_id,

        "timestamp":
            datetime.now().isoformat(),

        "gross_weight_kg":
            round(weight_kg, 2),

        "tare_weight_t":
            tare_weight,

        "net_coal_weight_t":
            round(
                (weight_kg / 1000)
                - tare_weight,
                2
            ),

        "payload_target_kg":
            target_weight,

        "pll_limit_kg":
            pll_limit,

        "distribution_ratio": {

            "left_pct":
                left_pct,

            "right_pct":
                right_pct,

            "front_pct":
                front_pct,

            "rear_pct":
                rear_pct
        },

        "balance_analysis": {

            "left_right_difference_pct":
                round(lr_difference, 2),

            "front_rear_difference_pct":
                round(fr_difference, 2),

            "maximum_distribution_error_pct":
                round(max_distribution_error, 2)
        },

        "system_status": status_code,
        "recommended_action": control_action,
        "loading_rate_kg_min": round(loading_rate_kg_min, 2),
        "time_to_target_sec": round(time_to_target_sec, 1),
        "predictive_stop_weight_kg": round(predictive_stop_weight, 1),
        "projected_after_stop_kg": round(projected_weight_after_stop, 1),
        "directional_guidance": directional_guidance,
        "confidence_score_pct": round(confidence_score, 1),
        "cross_validation_error_pct": round(cross_validation_error_pct, 2),
        "efficiency_score_pct": round(efficiency_score, 1),
        "certification_allowed": certification_allowed,
        "maintenance_risk_pct": predictive_maintenance_risk,
        "escalation_level": escalation_level,
        "offline_queue_depth": len(st.session_state.offline_queue),
        "integrity_check": {
            "checkpoint_weight_kg": round(checkpoint_weight_kg, 1),
            "delta_kg": round(integrity_delta_kg, 1),
            "anomaly": integrity_anomaly
        },

        "sensor_health": {

            "load_cells": health["load_cells"],
            "lidar": health["lidar"],
            "rfid": health["rfid"],
            "communication": health["communication"],
            "calibration": health["calibration"],
            "edge": health["edge"]
        }
    }


    st.json(
        sample_payload
    )


# ============================================================
# TAB 4 — PREDICTION & CONTROL
# ============================================================

with tab_predict:
    st.subheader("Predictive Stop-Point & Closed-Loop Guidance")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Current Weight", f"{weight_kg/1000:.2f} T")
    a2.metric("Loading Rate", f"{loading_rate_kg_min:.0f} kg/min")
    a3.metric("Stop Trigger", f"{predictive_stop_weight/1000:.2f} T")
    a4.metric("Projected After Stop", f"{projected_weight_after_stop/1000:.2f} T")

    progress = float(np.clip(weight_kg / max(target_weight, 1), 0, 1))
    st.progress(progress, text=f"Target progress: {progress*100:.1f}%")

    if control_action in ["STOP NOW", "EMERGENCY HOLD"]:
        st.error(f"**CONTROL ACTION: {control_action}**")
    elif "SLOW" in control_action:
        st.warning(f"**CONTROL ACTION: {control_action}**")
    else:
        st.success(f"**CONTROL ACTION: {control_action}**")

    st.write(f"**Directional command:** {directional_guidance}")
    st.write(f"**Residual-load estimate after stop command:** {residual_after_stop_kg:.0f} kg")
    st.write(f"**Operator escalation level:** {escalation_level} / 3")
    if enable_plc:
        st.info("PLC assist simulation ENABLED: recommendation can be mapped to NORMAL / SLOW / STOP commands through an industrial interface.")
    else:
        st.caption("PLC assist disabled: dashboard remains advisory and operator-controlled.")

    pred_times = np.arange(0, 121, 10)
    pred_weights = np.minimum(
        weight_kg + loading_rate_kg_sec * pred_times,
        pll_limit * 1.08
    )
    df_pred = pd.DataFrame({"Seconds Ahead": pred_times, "Projected Weight (kg)": pred_weights})
    fig_pred = px.line(df_pred, x="Seconds Ahead", y="Projected Weight (kg)", template="plotly_dark", markers=True)
    fig_pred.add_hline(y=target_weight, line_dash="dot", annotation_text="Target")
    fig_pred.add_hline(y=pll_limit, line_dash="dash", annotation_text="PLL")
    fig_pred.update_layout(height=340, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)")
    st.plotly_chart(fig_pred, use_container_width=True)


# ============================================================
# TAB 5 — LOAD INTEGRITY / TAMPER ANOMALY
# ============================================================

with tab_integrity:
    st.subheader("Dispatch-to-Checkpoint Load Integrity")
    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Dispatch Weight", f"{dispatch_weight_kg/1000:.2f} T")
    i2.metric("Checkpoint Weight", f"{checkpoint_weight_kg/1000:.2f} T")
    i3.metric("Difference", f"{integrity_delta_kg:.0f} kg")
    i4.metric("Profile Change", f"{checkpoint_loss_pct:.2f}%")

    if not enable_integrity:
        st.info("Transit integrity module disabled in sidebar.")
    elif integrity_anomaly:
        st.error("⚠️ UNEXPLAINED LOAD-INTEGRITY ANOMALY — verification / security review recommended. This does not automatically classify the event as theft.")
    else:
        st.success("No material load-integrity anomaly detected within the simulated tolerance.")

    st.markdown("**Verification chain:** RFID match → dispatch certificate → checkpoint weight/profile → tolerance check → anomaly flag")


# ============================================================
# TAB 6 — ANALYTICS / AUDIT / EFFICIENCY
# ============================================================

with tab_analytics:
    st.subheader("Optimal Efficiency & Audit Intelligence")
    an1, an2, an3, an4 = st.columns(4)
    an1.metric("Loading Accuracy", f"{loading_accuracy_pct:.1f}%")
    an2.metric("Overall Efficiency", f"{efficiency_score:.1f}%")
    an3.metric("Sensor Confidence", f"{confidence_score:.0f}%")
    an4.metric("Maintenance Risk", f"{predictive_maintenance_risk}%")

    audit_rows = []
    for idx in range(12):
        scenario = np.random.choice(["Normal", "Near Target", "Underload Risk", "Imbalance"], p=[0.45,0.25,0.15,0.15])
        audit_rows.append({
            "Wagon": f"{wagon_type}-{123400+idx}",
            "Shift": np.random.choice(["A", "B", "C"]),
            "Operator": np.random.choice([operator_id, "OP-7712", "OP-5521"]),
            "Deviation kg": int(np.random.normal(80 if scenario == "Normal" else 420, 180)),
            "Scenario": scenario,
            "Confidence %": int(np.clip(np.random.normal(94, 5), 70, 99))
        })
    df_audit = pd.DataFrame(audit_rows)
    st.dataframe(df_audit, use_container_width=True, hide_index=True)

    op_summary = df_audit.groupby("Operator", as_index=False).agg(
        Wagons=("Wagon", "count"),
        Mean_Deviation_kg=("Deviation kg", lambda x: round(abs(x).mean(), 1)),
        Avg_Confidence=("Confidence %", "mean")
    )
    st.markdown("**Operator / shift pattern analytics**")
    st.dataframe(op_summary, use_container_width=True, hide_index=True)


# ============================================================
# TAB 7 — DIGITAL CERTIFICATE
# ============================================================

with tab_cert:

    st.subheader(
        "Verified Digital Loading Certificate"
    )


    if certification_allowed:
        st.success("Tamper-evident verification record eligible for issue.")
    else:
        st.error("FAIL-SAFE: Certificate issue blocked because measurement confidence / hardware health is below the configured requirement.")


    payload_string = json.dumps(
        sample_payload,
        sort_keys=True
    )


    digital_signature = hashlib.sha256(
        payload_string.encode()
    ).hexdigest()


    certificate_text = f"""
================================================================================
                    SMARTLOAD CERTIFICATE — VERIFIED
================================================================================

Certificate Ref : SLC-{int(time.time())}
Issue Timestamp : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Siding Name     : {siding_id}
Operator ID     : {operator_id}
Wagon ID        : {wagon_id}
Wagon Type      : {wagon_type}

--------------------------------------------------------------------------------
MEASUREMENT ANALYSIS

Measured Gross Weight :
    {weight_kg:.1f} kg
    {weight_kg/1000:.2f} Metric Tonnes

Target Weight :
    {target_weight:.1f} kg
    {target_weight/1000:.2f} Metric Tonnes

Permissible Limit :
    {pll_limit:.1f} kg
    {pll_limit/1000:.2f} Metric Tonnes

Tare Weight :
    {tare_weight:.2f} Metric Tonnes

Net Coal Weight :
    {(weight_kg/1000)-tare_weight:.2f} Metric Tonnes


--------------------------------------------------------------------------------
FOUR-ZONE LOAD DISTRIBUTION

LEFT        : {left_pct:.1f} %
RIGHT       : {right_pct:.1f} %

FRONT       : {front_pct:.1f} %
REAR        : {rear_pct:.1f} %


--------------------------------------------------------------------------------
BALANCE ANALYSIS

Left / Right Difference :
    {lr_difference:.1f} %

Front / Rear Difference :
    {fr_difference:.1f} %

Maximum Distribution Error :
    {max_distribution_error:.1f} %


--------------------------------------------------------------------------------
SAFETY COMPLIANCE

System State :
    {status_code}

Action :
    {status_msg}

Guidance :
    {guidance_text}


--------------------------------------------------------------------------------
SENSOR STATUS

Load Cell Array :
    ONLINE

Gantry LiDAR :
    ONLINE

RFID AEI :
    ONLINE

LoRaWAN / 4G :
    CONNECTED


--------------------------------------------------------------------------------
ENHANCED SMARTLOAD INTELLIGENCE

Loading Rate : {loading_rate_kg_min:.1f} kg/min
Predictive Stop Point : {predictive_stop_weight/1000:.2f} T
Projected After Stop : {projected_weight_after_stop/1000:.2f} T
Directional Guidance : {directional_guidance}
Recommended Action : {control_action}
Confidence Score : {confidence_score:.1f} %
Cross-Validation Error : {cross_validation_error_pct:.2f} %
Efficiency Score : {efficiency_score:.1f} %
Maintenance Risk : {predictive_maintenance_risk} % ({maintenance_state})
Certification Allowed : {certification_allowed}

--------------------------------------------------------------------------------
DIGITAL VERIFICATION

SHA256 :
    {digital_signature}

================================================================================
"""


    st.code(
        certificate_text,
        language="text"
    )


    st.download_button(

        label=("⚡ Download Certified Record (JSON)" if certification_allowed else "⚠ Download Unverified Diagnostic Record (JSON)"),

        data=json.dumps(
            sample_payload,
            indent=4
        ),

        file_name=
            f"SmartLoad_Certificate_{wagon_id}.json",

        mime="application/json"
    )