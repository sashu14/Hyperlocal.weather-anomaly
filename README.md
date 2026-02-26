# 🌦️ Hyperlocal Weather Anomaly Detector

**Predicting the Unpredictable.** Advanced anomaly detection for hyperlocal weather monitoring. Secure your assets with AI-driven climate intelligence.

![Verified Landing Page](/Users/sashvithareddy/.gemini/antigravity/brain/0b898eb1-6fdd-4c77-a17a-fa2f9d589d54/landing_page_verified_1772120797592.png)

## 🚀 Key Features
- **Next-Gen UI**: Premium HTML/CSS landing page with a modern gradient aesthetic.
- **AI Anomaly Engine**: Uses **Isolation Forest** (unsupervised learning) to detect climate outliers in real-time.
- **Hyperlocal Precision**: Monitors temperature, humidity, and atmospheric pressure at the neighborhood level.
- **Sensory Analysis**: Real-time Plotly visualizations with trend mapping and correlation matrices.
- **Smart Alerts**: Visual warning system for instant detection of weather deviations.

## ✨ Zero-Setup Demo Mode
**No API Key? No Problem.** 
This project features a built-in high-fidelity "Demo Mode". If no API key is detected, the system automatically generates synthetic meteorological data using seasonal oscillation models with randomized anomaly injection. This allows for an instant evaluation of the AI engine's detection capabilities without any external configuration.

## 🛠️ Tech Stack
- **Dashboard**: Streamlit (with Custom CSS/HTML)
- **Visuals**: Plotly Express & Graph Objects
- **ML Model**: Scikit-Learn (Isolation Forest)
- **Data**: OpenWeatherMap API (Integrated & Mock Support)
- **Backend**: Pandas, NumPy, Python-Dotenv

## 📦 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```
   *The dashboard will be available at [http://localhost:8501](http://localhost:8501)*

## 🖥️ Usage Guide

1. **The Launchpad**: Upon opening, you'll be greeted by our premium landing page.
2. **Engage Tracker**: Click the **"Launch Anomaly Tracker →"** button. 
3. **Configure Target**: In the sidebar, enter any target **City**. You can skip the API configuration entirely.
4. **Monitor**: Click **"Engage Tracker"** to start the AI sensors. The system will detect that no API key is present and immediately activate **Demo Mode** with live synthetic telemetry.

## 🌎 Deployment Options

### 1. Vercel (Live API & Analytics)
- **Best for**: Real-time monitoring with your own API key.
- **Config**: Uses `vercel.json` and the Flask server in `api/index.py`.
- **Setup**: Import repo to Vercel, it works out-of-the-box.

### 2. GitHub Pages (Rapid Showcase)
- **Best for**: Portfolios and instant visual demos.
- **Config**: Uses the standalone `docs/index.html`.
- **Setup**: 
  1. Go to **Settings > Pages** in your GitHub repo.
  2. Set **Source** to "Deploy from a branch".
  3. Select **Branch: main** and **Folder: /docs**.
  4. Your static showroom will be live at `https://sashu14.github.io/Hyperlocal.weather-anomaly/`.

---
*Built for Precision Agriculture, Logistics, and High-Stakes Insurance.*
