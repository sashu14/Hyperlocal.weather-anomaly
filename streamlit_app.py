import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from data_handler import WeatherDataHandler
from utils import engineer_features, prepare_data_for_model
from model import WeatherAnomalyDetector

# Page Config
st.set_page_config(
    page_title="Hyperlocal Weather Anomaly Detector",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    .stApp {
        background: transparent;
    }
    h1, h2, h3 {
        color: #00d2ff !important;
        font-family: 'Inter', sans-serif;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    .anomaly-detected {
        background: rgba(255, 75, 75, 0.2);
        border: 2px solid #ff4b4b;
    }
    .normal-status {
        background: rgba(0, 255, 128, 0.1);
        border: 2px solid #00ff80;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/cloud-lighting.png", width=80)
    st.title("Sensor Hub")
    city = st.text_input("Target City", "New York")
    api_key = st.text_input("OpenWeather API Key (Optional)", type="password")
    contamination = st.slider("Anomaly Sensitivity", 0.01, 0.20, 0.05)
    
    st.markdown("---")
    st.info("💡 **Demo Mode:** If no API key is provided, the system uses high-fidelity synthetic data with randomized anomaly injection.")

# Title
st.title("🌦️ Hyperlocal Weather Anomaly Detector")
st.markdown("### Advanced AI-Driven Climate Intelligence")

# Initialize Session State
if 'detector' not in st.session_state:
    st.session_state.detector = None
if 'city' not in st.session_state or st.session_state.city != city:
    st.session_state.city = city
    st.session_state.detector = None

# Logic
handler = WeatherDataHandler(api_key=api_key if api_key else None, city=city)

if st.session_state.detector is None:
    with st.spinner(f"Calibrating sensors for {city}..."):
        st.session_state.detector = WeatherAnomalyDetector(contamination=contamination)
        # Train on historical data
        hist_df = handler.fetch_historical_data(days=7)
        hist_df = engineer_features(hist_df)
        X_train = prepare_data_for_model(hist_df)
        st.session_state.detector.train(X_train)
        time.sleep(1) # Aesthetic pause

# Fetch Live Data
live_data = handler.fetch_live_data()
live_df = pd.DataFrame([live_data])

# Fetch Recent History for Context
hist_recent = handler.fetch_historical_data(days=1).tail(10)
combined_df = pd.concat([hist_recent, live_df], ignore_index=True)
combined_df = engineer_features(combined_df)

# Detection
X_live = prepare_data_for_model(combined_df.tail(1))
is_anomaly = bool(st.session_state.detector.detect(X_live)[0])
anomaly_score = float(st.session_state.detector.get_anomaly_scores(X_live)[0])

# Layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Temperature", f"{live_data['temp']:.2f}°C", delta=f"{(live_data['temp'] - combined_df['temp_roll_avg'].iloc[-1]):.2f}°C")
with col2:
    st.metric("Humidity", f"{live_data['humidity']:.1f}%")
with col3:
    st.metric("Pressure", f"{live_data['pressure']:.0f} hPa")
with col4:
    st.metric("Wind Speed", f"{live_data['wind_speed']:.1f} m/s")

st.markdown("---")

# Anomaly Status
if is_anomaly:
    st.markdown(f'<div class="status-card anomaly-detected"><h3>⚠️ ANOMALY DETECTED</h3><p>Significant climatic deviation in {city}. Score: {anomaly_score:.3f}</p></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-card normal-status"><h3>✅ SYSTEM NORMAL</h3><p>Stable meteorological conditions in {city}. Score: {anomaly_score:.3f}</p></div>', unsafe_allow_html=True)

# Visualizations
st.markdown("### Real-Time Telemetry")
hist_data_full = handler.fetch_historical_data(days=3)
hist_data_full = engineer_features(hist_data_full)
hist_data_full['is_anomaly'] = st.session_state.detector.detect(prepare_data_for_model(hist_data_full))

# Trend Chart
fig = px.line(hist_data_full, x='timestamp', y='temp', title=f"Temperature Trends ({city})")
fig.add_trace(go.Scatter(
    x=hist_data_full[hist_data_full['is_anomaly']]['timestamp'],
    y=hist_data_full[hist_data_full['is_anomaly']]['temp'],
    mode='markers',
    name='Anomalies',
    marker=dict(color='red', size=10, symbol='x')
))
fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# Humidity / Pressure
c1, c2 = st.columns(2)
with c1:
    fig_h = px.area(hist_data_full, x='timestamp', y='humidity', title="Humidity Levels", color_discrete_sequence=['#00d2ff'])
    fig_h.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_h, use_container_width=True)
with c2:
    fig_p = px.line(hist_data_full, x='timestamp', y='pressure', title="Atmospheric Pressure", color_discrete_sequence=['#00ff80'])
    fig_p.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_p, use_container_width=True)

st.markdown("---")
st.caption(f"Last Sensor Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Architecture: Isolation Forest (Scikit-Learn)")
