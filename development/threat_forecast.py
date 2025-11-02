"""
Threat Forecasting Module for N.E.T.R.A.
Uses Prophet for time series forecasting of threat counts, probabilities, and location-specific risks.
"""

import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta
import numpy as np
import os

# Load historical data - use absolute path resolution
def get_data_path():
    """Get the correct path to the data file regardless of where the module is called from"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_path = os.path.join(parent_dir, 'netra_threat_log_large.csv')
    return data_path

def load_data():
    DATA_PATH = get_data_path()
    df = pd.read_csv(DATA_PATH, parse_dates=['Timestamp'])
    return df

def forecast_threat_counts(df, days_ahead=10):
    """Forecast total daily threat counts for next N days"""
    # Aggregate by day
    df['date'] = df['Timestamp'].dt.date
    daily_counts = df.groupby('date').size().reset_index(name='count')
    daily_counts.columns = ['ds', 'y']
    
    # Prophet model
    model = Prophet(daily_seasonality=True)
    model.fit(daily_counts)
    
    # Future dataframe
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)
    
    # Only future predictions
    forecast = forecast.tail(days_ahead)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

def forecast_threat_probabilities(df, days_ahead=10):
    """Forecast average daily threat probability and HIGH/CRITICAL rates"""
    df['date'] = df['Timestamp'].dt.date
    # Average probability per day
    avg_prob = df.groupby('date')['Threat_Probability'].mean().reset_index()
    avg_prob.columns = ['ds', 'y']
    
    model = Prophet(daily_seasonality=True)
    model.fit(avg_prob)
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)
    forecast = forecast.tail(days_ahead)
    
    # HIGH/CRITICAL rate per day
    df['is_high'] = df['Threat_Level'].isin(['HIGH', 'CRITICAL']).astype(int)
    high_rate = df.groupby('date')['is_high'].mean().reset_index()
    high_rate.columns = ['ds', 'y']
    model2 = Prophet(daily_seasonality=True)
    model2.fit(high_rate)
    future2 = model2.make_future_dataframe(periods=days_ahead)
    forecast2 = model2.predict(future2)
    forecast2 = forecast2.tail(days_ahead)
    
    return {
        'avg_prob': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
        'high_rate': forecast2[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    }

def forecast_top_locations(df, days_ahead=10, top_n=5):
    """Forecast threat counts for top N locations"""
    df['date'] = df['Timestamp'].dt.date
    top_locs = df['Location'].value_counts().head(top_n).index.tolist()
    results = {}
    for loc in top_locs:
        loc_df = df[df['Location'] == loc]
        daily_counts = loc_df.groupby('date').size().reset_index(name='count')
        daily_counts.columns = ['ds', 'y']
        if len(daily_counts) < 5:
            continue
        model = Prophet(daily_seasonality=True)
        model.fit(daily_counts)
        future = model.make_future_dataframe(periods=days_ahead)
        forecast = model.predict(future)
        forecast = forecast.tail(days_ahead)
        results[loc] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return results

def run_all_forecasts(days_ahead=10):
    df = load_data()
    threat_counts = forecast_threat_counts(df, days_ahead)
    threat_probs = forecast_threat_probabilities(df, days_ahead)
    top_locations = forecast_top_locations(df, days_ahead)
    return {
        'threat_counts': threat_counts,
        'threat_probs': threat_probs,
        'top_locations': top_locations
    }

if __name__ == "__main__":
    forecasts = run_all_forecasts(days_ahead=10)
    print("=== Threat Count Forecast ===")
    print(forecasts['threat_counts'])
    print("\n=== Threat Probability Forecast ===")
    print(forecasts['threat_probs']['avg_prob'])
    print("\n=== HIGH/CRITICAL Rate Forecast ===")
    print(forecasts['threat_probs']['high_rate'])
    print("\n=== Top Locations Forecast ===")
    for loc, df in forecasts['top_locations'].items():
        print(f"Location: {loc}")
        print(df)
