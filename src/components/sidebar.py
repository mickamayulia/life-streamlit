"""
Sidebar and Filter Components for Streamlit Dashboard
Provides uniform filters for year selection, country selection, indicators, and status.
"""

from typing import Tuple, List, Optional
import streamlit as st
import pandas as pd

from src.data.loader import NUMERIC_INDICATORS, INDICATOR_METADATA


def render_sidebar_filters(df: pd.DataFrame, default_year: int = 2014) -> dict:
    """
    Renders standard sidebar filters and returns active filter state dictionary.
    """
    st.sidebar.markdown(
        """
        <div style="padding: 12px 0 16px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 16px;">
            <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;">
                🌐 Life Expectancy BI
            </div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">
                Global Analytics Dashboard
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("### ⚙️ Filter Global")

    # Available years
    years = sorted(df['Year'].unique())
    selected_year = st.sidebar.select_slider(
        "Tahun Observasi (Snapshot)",
        options=years,
        value=default_year if default_year in years else years[-2]
    )

    # Status filter
    status_options = ["Semua Status"] + sorted(df['Status'].unique().tolist())
    selected_status = st.sidebar.selectbox("Status Pembangunan", status_options, index=0)

    # Default countries selection
    all_countries = sorted(df['Country'].unique())
    default_countries = [c for c in ['Indonesia', 'Australia', 'Japan', 'United States of America', 'Germany', 'Nigeria'] if c in all_countries]
    if not default_countries and len(all_countries) >= 3:
        default_countries = all_countries[:3]

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="font-size: 0.74rem; color: #64748b; line-height: 1.4;">
            <b>Capstone Kelompok 7</b><br>
            Sistem Informasi — ITK 2026<br>
            Unit Analisis: Country-Year (2000–2015)
        </div>
        """,
        unsafe_allow_html=True
    )

    return {
        'year': selected_year,
        'status': selected_status,
        'all_countries': all_countries,
        'default_countries': default_countries
    }
