import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def perform_feature_engineering(df, options):
    if "Date/Time Features" in options:
        df = add_date_features(df)
    if "One-Hot Encoding" in options:
        df = perform_one_hot_encoding(df)
    if "Scaling" in options:
        df = perform_scaling(df)
    return df

def add_date_features(df):
    # Implementation of date/time feature extraction
    pass

def perform_one_hot_encoding(df):
    # Implementation of one-hot encoding
    pass

def perform_scaling(df):
    # Implementation of numerical feature scaling
    pass
