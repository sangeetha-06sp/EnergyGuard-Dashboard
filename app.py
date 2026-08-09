import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EnergyGuard",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    color: #6b7280;
    font-size: 16px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    text-align: center;
}

.value {
    font-size: 32px;
    font-weight: 700;
}

.label {
    font-size: 16px;
    color: #6b7280;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    '<div class="title">⚡ EnergyGuard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Electrical Distribution Health Monitoring & Protection System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# THRESHOLDS
# -----------------------------

CURRENT_THRESHOLD = 10.0
TEMPERATURE_THRESHOLD = 50.0

# Assumed values ONLY for estimated power
NOMINAL_VOLTAGE = 230
POWER_FACTOR = 0.85

# -----------------------------
# SIMULATED SENSOR VALUES
# -----------------------------

current = round(random.uniform(5, 12), 2)

temperature = round(
    random.uniform(28, 55),
    1
)

# Estimated power
power = round(
    (NOMINAL_VOLTAGE * current * POWER_FACTOR) / 1000,
    2
)

# -----------------------------
# STATUS LOGIC
# -----------------------------

current_alert = current > CURRENT_THRESHOLD
temperature_alert = temperature > TEMPERATURE_THRESHOLD

if current_alert or temperature_alert:

    device_status = "OFF"
    feeder_status = "FAULT"
    system_status = "ALERT"

else:

    device_status = "ON"
    feeder_status = "NORMAL"
    system_status = "SAFE"

# -----------------------------
# SENSOR CARDS
# -----------------------------

st.subheader("📊 Live Sensor Readings")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="card">
            <div class="label">⚡ CURRENT</div>
            <div class="value">{current} A</div>
            <div class="label">Threshold: {CURRENT_THRESHOLD} A</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="card">
            <div class="label">🌡️ TEMPERATURE</div>
            <div class="value">{temperature} °C</div>
            <div class="label">Threshold: {TEMPERATURE_THRESHOLD} °C</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="card">
            <div class="label">💡 ESTIMATED POWER</div>
            <div class="value">{power} kW</div>
            <div class="label">Based on 230 V & PF 0.85</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------
# SYSTEM STATUS
# -----------------------------

st.subheader("🛡️ System Status")

status1, status2, status3 = st.columns(3)

with status1:

    if device_status == "ON":
        st.success("🟢 DEVICE STATUS: ON")
    else:
        st.error("🔴 DEVICE STATUS: OFF")

with status2:

    if feeder_status == "NORMAL":
        st.success("🟢 FEEDER STATUS: NORMAL")
    else:
        st.error("🔴 FEEDER STATUS: FAULT")

with status3:

    if system_status == "SAFE":
        st.success("🟢 SYSTEM STATUS: SAFE")
    else:
        st.error("🚨 SYSTEM STATUS: ALERT")

st.divider()

# -----------------------------
# ALERT PANEL
# -----------------------------

st.subheader("🚨 Alert Notifications")

alerts = []

if current_alert:

    alerts.append(
        f"⚠️ HIGH CURRENT — "
        f"{current} A exceeded the {CURRENT_THRESHOLD} A threshold."
    )

if temperature_alert:

    alerts.append(
        f"🌡️ HIGH TEMPERATURE — "
        f"{temperature} °C exceeded the {TEMPERATURE_THRESHOLD} °C threshold."
    )

if alerts:

    for alert in alerts:
        st.error(alert)

else:

    st.success(
        "✅ No abnormal conditions detected. "
        "EnergyGuard system is operating normally."
    )

st.divider()

# -----------------------------
# GRAPH DATA
# -----------------------------

times = [
    datetime.now() - timedelta(minutes=i)
    for i in range(19, -1, -1)
]

current_values = [
    round(random.uniform(5, 12), 2)
    for _ in range(20)
]

temperature_values = [
    round(random.uniform(28, 55), 1)
    for _ in range(20)
]

power_values = [
    round(
        (230 * value * 0.85) / 1000,
        2
    )
    for value in current_values
]

# -----------------------------
# CURRENT GRAPH
# -----------------------------

st.subheader("⚡ Current Monitoring")

fig_current = go.Figure()

fig_current.add_trace(
    go.Scatter(
        x=times,
        y=current_values,
        mode="lines+markers",
        name="Current"
    )
)

fig_current.add_hline(
    y=CURRENT_THRESHOLD,
    line_dash="dash",
    annotation_text="Threshold"
)

fig_current.update_layout(
    xaxis_title="Time",
    yaxis_title="Current (A)",
    height=400
)

st.plotly_chart(
    fig_current,
    use_container_width=True
)

# -----------------------------
# TEMPERATURE GRAPH
# -----------------------------

st.subheader("🌡️ Temperature Monitoring")

fig_temperature = go.Figure()

fig_temperature.add_trace(
    go.Scatter(
        x=times,
        y=temperature_values,
        mode="lines+markers",
        name="Temperature"
    )
)

fig_temperature.add_hline(
    y=TEMPERATURE_THRESHOLD,
    line_dash="dash",
    annotation_text="Threshold"
)

fig_temperature.update_layout(
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
    height=400
)

st.plotly_chart(
    fig_temperature,
    use_container_width=True
)

# -----------------------------
# POWER GRAPH
# -----------------------------

st.subheader("💡 Estimated Power Monitoring")

fig_power = go.Figure()

fig_power.add_trace(
    go.Scatter(
        x=times,
        y=power_values,
        mode="lines+markers",
        name="Power"
    )
)

fig_power.update_layout(
    xaxis_title="Time",
    yaxis_title="Estimated Power (kW)",
    height=400
)

st.plotly_chart(
    fig_power,
    use_container_width=True
)

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "EnergyGuard | Industrial Electrical Distribution Monitoring System"
)
