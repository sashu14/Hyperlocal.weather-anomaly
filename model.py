from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

class WeatherAnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        
    def train(self, X):
        """Train the Isolation Forest model."""
        self.model.fit(X)
        
    def detect(self, X):
        """
        Detect anomalies. 
        Returns -1 for outliers/anomalies and 1 for inliers.
        We convert it to boolean: True for anomaly.
        """
        predictions = self.model.predict(X)
        return predictions == -1

    def get_anomaly_scores(self, X):
        """Lower scores indicate more anomalous points."""
        return self.model.decision_function(X)
