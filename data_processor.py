import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    # Separate numeric and non-numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    non_numeric_columns = df.select_dtypes(exclude=[np.number]).columns

    # Convert non-numeric data in numeric columns to NaN
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle missing values for numeric columns
    numeric_imputer = SimpleImputer(strategy='mean')
    df[numeric_columns] = numeric_imputer.fit_transform(df[numeric_columns])

    # Handle missing values for non-numeric columns
    non_numeric_imputer = SimpleImputer(strategy='most_frequent')
    df[non_numeric_columns] = non_numeric_imputer.fit_transform(df[non_numeric_columns])

    # Standardize numeric features
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df