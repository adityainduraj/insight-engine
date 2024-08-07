import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Identify numeric columns
    numeric_columns = df_imputed.select_dtypes(include=[np.number]).columns

    # Standardize numeric features
    scaler = StandardScaler()
    df_imputed[numeric_columns] = scaler.fit_transform(df_imputed[numeric_columns])

    return df_imputed