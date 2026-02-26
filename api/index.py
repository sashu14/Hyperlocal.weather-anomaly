from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import pandas as pd
from datetime import datetime
import time
from data_handler import WeatherDataHandler
from utils import engineer_features, prepare_data_for_model
from model import WeatherAnomalyDetector

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Global instances (for demo purposes; in production, you might want to handle this differently)
detectors = {} # city -> detector

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'New York')
    
    handler = WeatherDataHandler(city=city)
    
    # Check if we have a trained detector for this city
    if city not in detectors:
        detectors[city] = WeatherAnomalyDetector(contamination=0.05)
        # Train on historical data
        hist_df = handler.fetch_historical_data(days=7)
        hist_df = engineer_features(hist_df)
        X_train = prepare_data_for_model(hist_df)
        detectors[city].train(X_train)
    
    # Fetch live data
    live_data = handler.fetch_live_data()
    live_df = pd.DataFrame([live_data])
    
    # We need some context for features like delta, so we fetch a bit of history too
    hist_recent = handler.fetch_historical_data(days=1).tail(10)
    combined_df = pd.concat([hist_recent, live_df], ignore_index=True)
    combined_df = engineer_features(combined_df)
    
    X_live = prepare_data_for_model(combined_df.tail(1))
    is_anomaly = bool(detectors[city].detect(X_live)[0])
    anomaly_score = float(detectors[city].get_anomaly_scores(X_live)[0])
    
    # Get historical points for the chart
    hist_data_full = handler.fetch_historical_data(days=3)
    hist_data_full = engineer_features(hist_data_full)
    hist_data_full['is_anomaly'] = detectors[city].detect(prepare_data_for_model(hist_data_full))
    
    # Format for JSON
    history = []
    for _, row in hist_data_full.iterrows():
        history.append({
            'timestamp': row['timestamp'].isoformat(),
            'temp': round(row['temp'], 2),
            'humidity': round(row['humidity'], 2),
            'pressure': round(row['pressure'], 2),
            'is_anomaly': bool(row['is_anomaly'])
        })
    
    return jsonify({
        'city': city,
        'current': {
            'temp': round(live_data['temp'], 2),
            'humidity': round(live_data['humidity'], 2),
            'pressure': round(live_data['pressure'], 2),
            'wind_speed': round(live_data['wind_speed'], 2),
            'timestamp': live_data['timestamp'].isoformat(),
            'is_anomaly': is_anomaly,
            'anomaly_score': round(anomaly_score, 3)
        },
        'history': history,
        'mean_temp': round(hist_data_full['temp'].mean(), 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
