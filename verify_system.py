from data_handler import WeatherDataHandler
from utils import engineer_features, prepare_data_for_model
from model import WeatherAnomalyDetector
import pandas as pd

def test_pipeline():
    print("Initializing components...")
    handler = WeatherDataHandler() # Mock mode
    detector = WeatherAnomalyDetector(contamination=0.1)
    
    print("Fetching mock historical data...")
    df = handler.fetch_historical_data(days=2)
    print(f"Data shape: {df.shape}")
    
    print("Engineering features...")
    df = engineer_features(df)
    
    print("Training model...")
    X = prepare_data_for_model(df)
    detector.train(X)
    
    print("Detecting anomalies...")
    df['is_anomaly'] = detector.detect(X)
    anomalies = df[df['is_anomaly']]
    
    print(f"Detected {len(anomalies)} anomalies in {len(df)} data points.")
    
    if len(anomalies) > 0:
        print("Success: Anomalies detected in mock data.")
    else:
        print("Warning: No anomalies detected. Checking logic...")
        
    print("\nSample Anomalies:")
    print(anomalies[['timestamp', 'temp', 'humidity']].head())

if __name__ == "__main__":
    test_pipeline()
