"""
Anomaly Detection Engine for Life Expectancy Dataset
Computes IQR-based and Z-score based outlier flags without mutating or deleting underlying data.
"""

from typing import Tuple, List, Optional
import numpy as np
import pandas as pd


def detect_iqr_anomalies(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Returns boolean series marking values outside [Q1 - multiplier*IQR, Q3 + multiplier*IQR].
    """
    valid = series.dropna()
    if len(valid) == 0:
        return pd.Series(False, index=series.index)

    q1 = valid.quantile(0.25)
    q3 = valid.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    return (series < lower_bound) | (series > upper_bound)


def detect_zscore_anomalies(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Returns boolean series marking values where |z-score| > threshold.
    """
    valid = series.dropna()
    if len(valid) < 3 or valid.std() == 0:
        return pd.Series(False, index=series.index)

    mean = valid.mean()
    std = valid.std()
    z_scores = (series - mean).abs() / std
    return z_scores > threshold


def compute_anomaly_flags(
    df: pd.DataFrame,
    indicators: Optional[List[str]] = None,
    method: str = "iqr",
    by_status: bool = False
) -> pd.DataFrame:
    """
    Computes anomaly flags for specified indicators and attaches flag columns.
    Original columns remain untouched.
    
    Args:
        df: DataFrame containing life expectancy data.
        indicators: List of column names to check for anomalies. Defaults to key indicators.
        method: 'iqr' (default) or 'zscore'.
        by_status: If True, calculates thresholds separately within Developing vs Developed groups.
        
    Returns:
        DataFrame with additional boolean columns named '{col}_is_anomaly'.
    """
    res = df.copy()
    if indicators is None:
        indicators = ['Life_expectancy', 'Adult_Mortality', 'GDP', 'Schooling', 'HIV/AIDS', 'BMI']

    detector = detect_iqr_anomalies if method.lower() == "iqr" else detect_zscore_anomalies

    for col in indicators:
        if col not in df.columns:
            continue
        flag_col = f"{col}_is_anomaly"
        if by_status and 'Status' in df.columns:
            res[flag_col] = False
            for status_val in df['Status'].unique():
                idx = df['Status'] == status_val
                res.loc[idx, flag_col] = detector(df.loc[idx, col])
        else:
            res[flag_col] = detector(df[col])

    # Summary flag: Any anomaly flagged across selected indicators
    flag_cols = [f"{col}_is_anomaly" for col in indicators if f"{col}_is_anomaly" in res.columns]
    res['has_any_anomaly'] = res[flag_cols].any(axis=1) if flag_cols else False

    return res


def get_anomaly_summary(df_flagged: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
    """
    Returns a summary table of anomaly counts and percentages per indicator.
    """
    summary = []
    total_rows = len(df_flagged)

    for col in indicators:
        flag_col = f"{col}_is_anomaly"
        if flag_col in df_flagged.columns:
            count = int(df_flagged[flag_col].sum())
            pct = (count / total_rows) * 100 if total_rows > 0 else 0
            summary.append({
                'Indicator': col,
                'Anomaly Count': count,
                'Percentage (%)': round(pct, 2)
            })

    return pd.DataFrame(summary)
