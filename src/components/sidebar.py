"""
Sidebar and Filter Components for Streamlit Dashboard
Provides uniform filters for year selection, status, and custom multipage navigation.
"""

from typing import Tuple, List, Optional
import streamlit as st
import pandas as pd

from src.data.loader import NUMERIC_INDICATORS, INDICATOR_METADATA


def render_sidebar_filters(df: pd.DataFrame, default_year: int = 2014) -> dict:
    """
    Renders standard sidebar layout:
    1. Title & Branding header
    2. Filter Global (Year snapshot, Status Pembangunan)
    3. Navigation Menu (Custom page links placed below Status Pembangunan)
    4. Project Footer
    """
    # 1. Branding Header
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

    # 2. Filter Global
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

    # 3. Custom Navigation Tabs (Placed strictly below Status Pembangunan)
    st.sidebar.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("### 🧭 Menu Navigasi")
    
    st.sidebar.page_link("app.py", label="Home (Beranda)", icon="🏠")
    st.sidebar.page_link("pages/1_Overview.py", label="1. Overview & Trends", icon="📈")
    st.sidebar.page_link("pages/2_Country_Comparison.py", label="2. Country Comparison", icon="⚖️")
    st.sidebar.page_link("pages/3_Geospatial_Explorer.py", label="3. Geospatial Explorer", icon="🗺️")
    st.sidebar.page_link("pages/4_Correlation_and_Determinants.py", label="4. Correlation & Determinants", icon="🔬")
    st.sidebar.page_link("pages/5_Data_Audit_and_Methodology.py", label="5. Data Audit & Methodology", icon="📋")

    # Default countries selection
    all_countries = sorted(df['Country'].unique())
    default_countries = [c for c in ['Indonesia', 'Australia', 'Japan', 'United States of America', 'Germany', 'Nigeria'] if c in all_countries]
    if not default_countries and len(all_countries) >= 3:
        default_countries = all_countries[:3]

    # 4. Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="font-size: 0.74rem; color: #64748b; line-height: 1.4;">
            <b>Capstone Kelompok 7</b><br>
            Sistem Informasi — ITK 2026<br>
            Cakupan: 193 Negara (2000–2015)
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
