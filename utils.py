import pandas as pd

def engineer_features(df):
    """
    Generate features for anomaly detection.
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Time-based features
    df['hour'] = df['timestamp'].dt.hour
    
    # Rolling averages for trend detection
    df['temp_roll_avg'] = df['temp'].rolling(window=6).mean()
    df['temp_delta'] = df['temp'] - df['temp_roll_avg']
    
    # Lag features
    df['temp_lag_1'] = df['temp'].shift(1)
    
    # Fill NaNs created by rolling/lag
    df = df.bfill()
    
    return df

def prepare_data_for_model(df):
    """
    Select features for the Isolation Forest model.
    """
    features = ['temp', 'humidity', 'pressure', 'wind_speed', 'temp_delta']
    return df[features]
