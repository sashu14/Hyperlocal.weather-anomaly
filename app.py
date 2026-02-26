import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_handler import WeatherDataHandler
from utils import engineer_features, prepare_data_for_model
from model import WeatherAnomalyDetector
import time
from datetime import datetime

# Page config
st.set_page_config(page_title="Hyperlocal Weather Anomaly Detector", layout="wide", page_icon="🌦️")

# State management for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

def go_to_tracker():
    st.session_state.page = 'tracker'

def go_to_intro():
    st.session_state.page = 'intro'

# Custom CSS for premium look and landing page
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: radial-gradient(circle at top right, #1e2130, #0e1117);
        color: #ffffff;
    }
    
    /* Hero Section */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 100px 20px;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 40px auto;
        max-width: 900px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    .hero-badge {
        background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 20px;
        letter-spacing: 2px;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #00d1ff, #007bff, #b06ab3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #ccd0d8;
        max-width: 600px;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-top: 50px;
        width: 100%;
        max-width: 1000px;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.06);
        border-color: #00d1ff;
        box-shadow: 0 10px 30px rgba(0, 209, 255, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
        display: block;
    }
    
    .feature-card h3 {
        color: #00d1ff;
        margin-bottom: 10px;
        font-weight: 700;
    }
    
    .feature-card p {
        color: #a0a0a0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Metrics and Dashboard */
    .stMetric {
        background: rgba(30, 33, 48, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .anomaly-alert {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(135deg, #ff4b4b, #c0392b);
        color: white;
        font-weight: 800;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(255, 75, 75, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

# Landing Page Component
def intro_page():
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">Next-Gen Weather Tech</div>
            <h1 class="hero-title">Predicting the Unpredictable.</h1>
            <p class="hero-subtitle">Advanced anomaly detection for hyperlocal weather monitoring. Secure your assets with AI-driven climate intelligence.</p>
            <div class="feature-grid">
                <div class="feature-card">
                    <span class="feature-icon">🛰️</span>
                    <h3>Hyper-Local Precision</h3>
                    <p>High-frequency data ingestion from global meteorological stations for unmatched accuracy at the neighborhood level.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🧠</span>
                    <h3>Isolation Engine</h3>
                    <p>Proprietary Isolation Forest implementation identifies climate outliers and extreme shifts in real-time.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📊</span>
                    <h3>Visual Insights</h3>
                    <p>Interactive temporal mapping and correlation analysis for informed decision making in agriculture and logistics.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Launch Anomaly Tracker →", on_click=go_to_tracker, type="primary", use_container_width=True)

# Application Logic
if st.session_state.page == 'intro':
    intro_page()
else:
    st.title("🌦️ Hyperlocal Weather Anomaly Detector")
    st.sidebar.button("← Back to Intro", on_click=go_to_intro)
    
    # Sidebar Tracker Config
    st.sidebar.header("Tracking Console")
    city = st.sidebar.text_input("Target City", "New York")
    refresh_rate = st.sidebar.slider("Refresh Interval (s)", 5, 60, 10)
    
    # Initialize handler and detector
    # Note: API key is now handled internally/env var
    handler = WeatherDataHandler(city=city)
    detector = WeatherAnomalyDetector(contamination=0.05)

    # Main Dashboard logic
    def run_app():
        # Fetch historical data for training
        with st.spinner(f"Calibrating sensors for {city}..."):
            hist_df = handler.fetch_historical_data(days=7)
            hist_df = engineer_features(hist_df)
            
            # Train model
            X_train = prepare_data_for_model(hist_df)
            detector.train(X_train)
            
            # Detect historical anomalies
            hist_df['is_anomaly'] = detector.detect(X_train)
            
        # Placeholder for live updates
        placeholder = st.empty()
        
        while True:
            live_data = handler.fetch_live_data()
            live_df = pd.DataFrame([live_data])
            
            combined_df = pd.concat([hist_df.iloc[-10:], live_df], ignore_index=True)
            combined_df = engineer_features(combined_df)
            
            X_live = prepare_data_for_model(combined_df.tail(1))
            is_anomaly = detector.detect(X_live)[0]
            anomaly_score = detector.get_anomaly_scores(X_live)[0]
            
            with placeholder.container():
                # Alerts
                if is_anomaly:
                    st.markdown(f"""
                        <div class="anomaly-alert">
                            ⚠️ ANOMALY DETECTED IN {city.upper()}! <br>
                            Unusual weather pattern identified at {datetime.now().strftime('%H:%M:%S')}
                        </div>
                    """, unsafe_allow_html=True)
                
                # Metrics
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Temperature", f"{live_data['temp']:.1f}°C", delta=f"{live_data['temp'] - hist_df['temp'].mean():.1f}°C")
                m_col2.metric("Humidity", f"{live_data['humidity']}%")
                m_col3.metric("Pressure", f"{live_data['pressure']} hPa")
                m_col4.metric("Anomaly Score", f"{anomaly_score:.2f}", delta="Lower is worse", delta_color="inverse")
                
                # Visualization
                st.subheader("Sensor Analysis & Trend Mapping")
                
                plot_df = pd.concat([hist_df, combined_df.tail(1)], ignore_index=True)
                plot_df['is_anomaly'] = detector.detect(prepare_data_for_model(engineer_features(plot_df)))
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=plot_df['timestamp'], y=plot_df['temp'],
                    mode='lines', name='Temperature',
                    line=dict(color='#00d1ff', width=2)
                ))
                
                anomalies = plot_df[plot_df['is_anomaly']]
                fig.add_trace(go.Scatter(
                    x=anomalies['timestamp'], y=anomalies['temp'],
                    mode='markers', name='Anomaly',
                    marker=dict(color='red', size=10, symbol='x')
                ))
                
                fig.update_layout(
                    template="plotly_dark",
                    hovermode="x unified",
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("Humidity Flux")
                    fig_hum = px.line(plot_df, x='timestamp', y='humidity', template="plotly_dark", color_discrete_sequence=['#007bff'])
                    st.plotly_chart(fig_hum, use_container_width=True)
                with c2:
                    st.subheader("Atmospheric Correlation")
                    corr = plot_df[['temp', 'humidity', 'pressure', 'wind_speed']].corr()
                    fig_corr = px.imshow(corr, text_auto=True, template="plotly_dark", color_continuous_scale='RdBu_r')
                    st.plotly_chart(fig_corr, use_container_width=True)

            time.sleep(refresh_rate)

    if st.sidebar.button("Engage Tracker"):
        run_app()
    else:
        st.info("👈 Enter target location and click 'Engage Tracker' to begin AI analysis.")
