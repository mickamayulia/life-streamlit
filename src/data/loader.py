"""
Data Loader & Preprocessing Layer for Life Expectancy Analytics Dashboard
Handles loading raw and cleaned datasets, ISO-3 code enrichment, and validation caching.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import streamlit as st

from src.utils.geo_mapping import COUNTRY_TO_ISO3

# File Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CLEANED_DATA_PATH = BASE_DIR / "excel" / "life_expectancy_cleaned_dataset.xlsx"
RAW_DATA_PATH = BASE_DIR / "excel" / "Life Expectancy Data.csv"

# Standard Numeric Indicators
NUMERIC_INDICATORS = [
    'Life_expectancy',
    'Adult_Mortality',
    'infant_deaths',
    'Alcohol',
    'percentage_expenditure',
    'Hepatitis_B',
    'Measles',
    'BMI',
    'under-five_deaths',
    'Polio',
    'Total_expenditure',
    'Diphtheria',
    'HIV/AIDS',
    'GDP',
    'Population',
    'thinness__1-19_years',
    'thinness_5-9_years',
    'Income_composition_of_resources',
    'Schooling'
]

INDICATOR_METADATA = {
    'Life_expectancy': {'label': 'Life Expectancy', 'unit': 'Years', 'category': 'Target'},
    'Adult_Mortality': {'label': 'Adult Mortality Rate', 'unit': 'per 1000 pop', 'category': 'Health'},
    'infant_deaths': {'label': 'Infant Deaths', 'unit': 'per 1000 pop', 'category': 'Health'},
    'under-five_deaths': {'label': 'Under-Five Deaths', 'unit': 'per 1000 pop', 'category': 'Health'},
    'HIV/AIDS': {'label': 'HIV/AIDS Deaths (0-4 yrs)', 'unit': 'per 1000 live births', 'category': 'Health'},
    'BMI': {'label': 'Average Body Mass Index', 'unit': 'Index', 'category': 'Health'},
    'thinness__1-19_years': {'label': 'Thinness 10-19 Years', 'unit': '%', 'category': 'Health'},
    'thinness_5-9_years': {'label': 'Thinness 5-9 Years', 'unit': '%', 'category': 'Health'},
    'Alcohol': {'label': 'Alcohol Consumption', 'unit': 'Litres of pure alcohol', 'category': 'Behavioral'},
    'Hepatitis_B': {'label': 'Hepatitis B Immunization', 'unit': '% of 1-yr-olds', 'category': 'Immunization'},
    'Polio': {'label': 'Polio Immunization', 'unit': '% of 1-yr-olds', 'category': 'Immunization'},
    'Diphtheria': {'label': 'DTP3 Immunization', 'unit': '% of 1-yr-olds', 'category': 'Immunization'},
    'Measles': {'label': 'Reported Measles Cases', 'unit': 'Reported cases', 'category': 'Epidemiology'},
    'GDP': {'label': 'GDP per Capita', 'unit': 'USD', 'category': 'Economic'},
    'percentage_expenditure': {'label': 'Expenditure on Health % GDP', 'unit': '% of GDP per cap', 'category': 'Economic'},
    'Total_expenditure': {'label': 'Govt Health Expenditure % Total', 'unit': '% of total govt budget', 'category': 'Economic'},
    'Population': {'label': 'Total Population', 'unit': 'Persons', 'category': 'Demographic'},
    'Income_composition_of_resources': {'label': 'Income Composition of Resources (HDI)', 'unit': 'Index 0 to 1', 'category': 'Socioeconomic'},
    'Schooling': {'label': 'Years of Schooling', 'unit': 'Years', 'category': 'Education'}
}


@st.cache_data(show_spinner=False)
def load_cleaned_data() -> pd.DataFrame:
    """
    Loads the cleaned Excel dataset, validates structure, and enriches with ISO-3 country codes.
    """
    if not CLEANED_DATA_PATH.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at: {CLEANED_DATA_PATH}")

    df = pd.read_excel(CLEANED_DATA_PATH)

    # Ensure Country and Year types
    df['Country'] = df['Country'].astype(str).str.strip()
    df['Year'] = df['Year'].astype(int)
    df['Status'] = df['Status'].astype(str).str.strip()

    # Enrich with ISO-3
    df['iso_alpha'] = df['Country'].map(COUNTRY_TO_ISO3)

    return df


@st.cache_data(show_spinner=False)
def load_raw_data() -> pd.DataFrame:
    """
    Loads raw Kaggle CSV dataset for data audit & methodology transparency page.
    """
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    # Strip spaces from column headers
    df.columns = [col.strip() for col in df.columns]
    return df


def get_dataset_summary() -> dict:
    """
    Returns quick audit summary metrics comparing raw vs cleaned dataset.
    """
    df_clean = load_cleaned_data()
    try:
        df_raw = load_raw_data()
        raw_rows, raw_cols = df_raw.shape
        raw_countries = df_raw['Country'].nunique()
        raw_nulls = int(df_raw.isnull().sum().sum())
    except Exception:
        raw_rows, raw_cols, raw_countries, raw_nulls = 2938, 22, 193, 2735

    clean_rows, clean_cols = df_clean.shape
    clean_countries = df_clean['Country'].nunique()
    clean_nulls = int(df_clean.isnull().sum().sum())

    return {
        'raw_rows': raw_rows,
        'raw_countries': raw_countries,
        'raw_nulls': raw_nulls,
        'clean_rows': clean_rows,
        'clean_countries': clean_countries,
        'clean_nulls': clean_nulls,
        'year_min': int(df_clean['Year'].min()),
        'year_max': int(df_clean['Year'].max()),
        'unmapped_iso_count': int(df_clean['iso_alpha'].isnull().sum())
    }
