"""
Analytics Engine for Global Metrics, Trends, Correlations, and Disparity Rankings
Handles statistical computations, aggregations, country trend metrics, and correlation matrices.
"""

from typing import List, Dict, Optional, Tuple, Literal
import numpy as np
import pandas as pd


def compute_global_kpis(df: pd.DataFrame, year: Optional[int] = None) -> Dict[str, float]:
    """
    Computes global headline KPIs for a specific year or across the entire dataset.
    Returns:
        dict: {
            'mean_life_expectancy': float,
            'median_life_expectancy': float,
            'std_life_expectancy': float,
            'min_life_expectancy': float,
            'max_life_expectancy': float,
            'total_countries': int,
            'developing_countries': int,
            'developed_countries': int,
            'developing_avg_le': float,
            'developed_avg_le': float,
            'disparity_gap': float
        }
    """
    sub_df = df if year is None else df[df['Year'] == year]
    if sub_df.empty:
        return {}

    le = sub_df['Life_expectancy'].dropna()
    status_grp = sub_df.groupby('Status')['Life_expectancy'].mean().to_dict()
    dev_le = status_grp.get('Developing', np.nan)
    dev_ed_le = status_grp.get('Developed', np.nan)
    gap = dev_ed_le - dev_le if (not np.isnan(dev_ed_le) and not np.isnan(dev_le)) else np.nan

    status_counts = sub_df['Status'].value_counts().to_dict()

    return {
        'mean_life_expectancy': round(float(le.mean()), 2),
        'median_life_expectancy': round(float(le.median()), 2),
        'std_life_expectancy': round(float(le.std()), 2) if len(le) > 1 else 0.0,
        'min_life_expectancy': round(float(le.min()), 2),
        'max_life_expectancy': round(float(le.max()), 2),
        'total_countries': int(sub_df['Country'].nunique()),
        'overall_countries': int(df['Country'].nunique()),
        'developing_countries': int(status_counts.get('Developing', 0)),
        'developed_countries': int(status_counts.get('Developed', 0)),
        'developing_avg_le': round(float(dev_le), 2) if not np.isnan(dev_le) else 0.0,
        'developed_avg_le': round(float(dev_ed_le), 2) if not np.isnan(dev_ed_le) else 0.0,
        'disparity_gap': round(float(gap), 2) if not np.isnan(gap) else 0.0
    }


def compute_yearly_trends(
    df: pd.DataFrame,
    indicator: str = 'Life_expectancy',
    weighted: bool = False
) -> pd.DataFrame:
    """
    Computes global yearly trend for a selected indicator (2000-2015).
    Optionally weights by Population if weighted=True and indicator allows.
    
    Returns:
        DataFrame with columns: ['Year', 'Mean', 'Median', 'Std', 'Min', 'Max', 'Country_Count']
    """
    if indicator not in df.columns:
        raise ValueError(f"Indicator '{indicator}' not in dataframe columns.")

    records = []
    for yr, group in df.groupby('Year'):
        valid = group.dropna(subset=[indicator])
        if valid.empty:
            continue

        if weighted and 'Population' in valid.columns and (valid['Population'] > 0).any():
            # Filter non-zero population
            w_valid = valid[valid['Population'] > 0]
            if not w_valid.empty:
                w_mean = np.average(w_valid[indicator], weights=w_valid['Population'])
            else:
                w_mean = valid[indicator].mean()
            mean_val = w_mean
        else:
            mean_val = valid[indicator].mean()

        records.append({
            'Year': int(yr),
            'Mean': round(float(mean_val), 2),
            'Median': round(float(valid[indicator].median()), 2),
            'Std': round(float(valid[indicator].std()), 2) if len(valid) > 1 else 0.0,
            'Min': round(float(valid[indicator].min()), 2),
            'Max': round(float(valid[indicator].max()), 2),
            'Country_Count': int(valid['Country'].nunique())
        })

    trend_df = pd.DataFrame(records).sort_values('Year').reset_index(drop=True)
    if not trend_df.empty:
        trend_df['Annual_Change'] = trend_df['Mean'].diff().round(2)
    return trend_df


def compute_country_comparison_data(
    df: pd.DataFrame,
    countries: List[str],
    indicator: str = 'Life_expectancy'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extracts time series and calculates overall delta/growth for a list of selected countries.
    
    Returns:
        trend_data: Long-form DataFrame filtered to selected countries.
        summary_stats: DataFrame comparing Start Value, End Value, Absolute Delta, and CAGR/Growth %.
    """
    sub_df = df[df['Country'].isin(countries)].copy()
    if sub_df.empty or indicator not in sub_df.columns:
        return pd.DataFrame(), pd.DataFrame()

    sub_df = sub_df.sort_values(['Country', 'Year'])

    # Summary table
    summaries = []
    for country in countries:
        c_df = sub_df[sub_df['Country'] == country].dropna(subset=[indicator])
        if c_df.empty:
            continue

        min_year = c_df['Year'].min()
        max_year = c_df['Year'].max()
        start_val = c_df[c_df['Year'] == min_year][indicator].values[0]
        end_val = c_df[c_df['Year'] == max_year][indicator].values[0]
        delta = end_val - start_val
        pct_change = (delta / start_val * 100) if start_val != 0 else np.nan
        status = c_df['Status'].iloc[0] if 'Status' in c_df.columns else 'Unknown'

        summaries.append({
            'Country': country,
            'Status': status,
            'Start Year': int(min_year),
            'Start Value': round(float(start_val), 2),
            'End Year': int(max_year),
            'End Value': round(float(end_val), 2),
            'Net Change': round(float(delta), 2),
            'Change (%)': round(float(pct_change), 2)
        })

    summary_df = pd.DataFrame(summaries)
    return sub_df, summary_df


def compute_correlation_matrix(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: Literal['pearson', 'spearman'] = 'pearson',
    year: Optional[int] = None
) -> pd.DataFrame:
    """
    Computes correlation matrix between specified numeric columns.
    Allows choosing Pearson or Spearman correlation.
    """
    sub_df = df if year is None else df[df['Year'] == year]
    if columns is None:
        columns = [
            'Life_expectancy', 'Adult_Mortality', 'infant_deaths', 'Alcohol',
            'percentage_expenditure', 'Hepatitis_B', 'BMI', 'under-five_deaths',
            'Polio', 'Total_expenditure', 'Diphtheria', 'HIV/AIDS', 'GDP',
            'thinness__1-19_years', 'Income_composition_of_resources', 'Schooling'
        ]

    valid_cols = [c for c in columns if c in sub_df.columns and pd.api.types.is_numeric_dtype(sub_df[c])]
    corr = sub_df[valid_cols].corr(method=method)
    return corr.round(3)


def get_country_rankings(
    df: pd.DataFrame,
    year: int,
    indicator: str = 'Life_expectancy',
    top_n: int = 10,
    ascending: bool = False
) -> pd.DataFrame:
    """
    Returns top or bottom N countries for a given year and indicator.
    """
    sub_df = df[df['Year'] == year].dropna(subset=[indicator])
    if sub_df.empty:
        return pd.DataFrame()

    ranked = sub_df.sort_values(by=indicator, ascending=ascending).head(top_n)
    cols = ['Country', 'Status', indicator, 'iso_alpha']
    if 'Population' in ranked.columns:
        cols.append('Population')
    available_cols = [c for c in cols if c in ranked.columns]
    
    res = ranked[available_cols].reset_index(drop=True)
    res.index = res.index + 1
    res.index.name = 'Rank'
    return res
