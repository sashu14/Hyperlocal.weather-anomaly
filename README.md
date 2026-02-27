# 🌦️ Hyperlocal Weather Anomaly Detector

**Predicting the Unpredictable.** Advanced anomaly detection for hyperlocal weather monitoring. Secure your assets with AI-driven climate intelligence.

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge&logo=vercel)](https://hyperlocal-weather-anomaly.vercel.app)

![Verified Landing Page](/Users/sashvithareddy/.gemini/antigravity/brain/0b898eb1-6fdd-4c77-a17a-fa2f9d589d54/landing_page_verified_1772120797592.png)

## 🚀 Key Features
- **Live Vercel Deployment**: Access the premium analytics suite instantly at [hyperlocal-weather-anomaly.vercel.app](https://hyperlocal-weather-anomaly.vercel.app).
- **Next-Gen UI**: Premium HTML/CSS landing page with a modern gradient aesthetic and glassmorphism.
- **AI Anomaly Engine**: Uses **Isolation Forest** (unsupervised learning) to detect climate outliers and seasonal deviations in real-time.
- **Hyperlocal Precision**: High-frequency telemetry monitoring for temperature, humidity, and atmospheric pressure.
- **Sensory Analysis**: Real-time Plotly visualizations with trend mapping and statistical outlier labeling.
- **Smart Alerts**: Visual warning system for instant detection of significant meteorological shifts.

## ✨ Zero-Setup Demo Mode
**No API Key? No Problem.** 
This project features a built-in high-fidelity "Demo Mode". If no API key is detected, the system automatically generates synthetic meteorological data using seasonal oscillation models with randomized anomaly injection. This allows for an instant evaluation of the AI engine's detection capabilities without any external configuration.

## 🛠️ Tech Stack
- **Web Backend**: Flask (for Vercel/HTML deployment)
- **Dashboard**: Streamlit (for interactive data science viewing)
- **Visuals**: Plotly Express & Graph Objects
- **ML Model**: Scikit-Learn (Isolation Forest)
- **Data**: OpenWeatherMap API (Integrated & Mock Support)
- **Backend**: Pandas, NumPy, Python-Dotenv

## 📦 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Streamlit Dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```
   *The dashboard will be available at [http://localhost:8501](http://localhost:8501)*

## 🖥️ Usage Guide

1. **The Launchpad**: Upon opening, you'll be greeted by our premium landing page.
2. **Engage Tracker**: Click the **"Launch Anomaly Tracker →"** button. 
3. **Monitor**: The system immediately activates **Demo Mode** with live synthetic telemetry.
4. **Configure Target**: Enter any target **City** to see how the AI engine cross-references historical trends for that location.

## 🌎 Deployment Options

### 1. Vercel (Premium HTML UI)
- **Live URL**: [https://hyperlocal-weather-anomaly.vercel.app](https://hyperlocal-weather-anomaly.vercel.app)
- **Config**: Uses `vercel.json` and the Flask server in `api/index.py`.

### 2. Streamlit Cloud (Interactive Dashboard)
- **Best for**: Rapid iteration and data science visualization.
- **Config**: Uses `streamlit_app.py` and `requirements-streamlit.txt`.

---
*Built for Precision Agriculture, Logistics, and High-Stakes Insurance.*
