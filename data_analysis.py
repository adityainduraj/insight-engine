import pandas as pd

def get_summary_statistics(df):
    # Basic summary statistics
    summary = df.describe()

    # Additional statistics
    summary.loc['skew'] = df.skew()
    summary.loc['kurtosis'] = df.kurtosis()

    return summary