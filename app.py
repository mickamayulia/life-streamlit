"""
Life Expectancy Global Analytics Dashboard
Main Entry Point - Multipage Streamlit Application
"""

import streamlit as st
import pandas as pd

from src.data.loader import load_cleaned_data, get_dataset_summary
from src.components.ui import apply_custom_css, render_hero, render_metric_card
from src.components.sidebar import render_sidebar_filters
from src.analytics.metrics import compute_global_kpis

# Page Config
st.set_page_config(
    page_title="Global Life Expectancy Analytics",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styling
apply_custom_css()

# Load Data
df = load_cleaned_data()
filters = render_sidebar_filters(df, default_year=2014)

# Hero Header
render_hero(
    title="Life Expectancy Global Analytics Dashboard",
    subtitle="Platform analitik interaktif untuk eksplorasi angka harapan hidup global, disparitas sosio-ekonomi, dan faktor determinan kesehatan lintas negara (2000–2015).",
    badge="IS CAPSTONE KELOMPOK 7 — ITK 2026"
)

# Navigation Cards / Quick Overview
st.markdown("### 🧭 Modul Eksplorasi")
st.markdown("Pilih modul analitik melalui menu **Sidebar** di sebelah kiri atau navigasi cepat di bawah ini:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="metric-card accent-blue">
            <div style="font-size: 1.4rem; margin-bottom: 8px;">📈</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #f9fafb; margin-bottom: 6px;">
                1. Overview & Trends
            </div>
            <div style="font-size: 0.84rem; color: #94a3b8; line-height: 1.45;">
                Ringkasan KPI global, tren aggregate tahunan 2000–2015, dan visualisasi distribusi harapan hidup antar status negara.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric-card accent-emerald">
            <div style="font-size: 1.4rem; margin-bottom: 8px;">⚖️</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #f9fafb; margin-bottom: 6px;">
                2. Country Comparison
            </div>
            <div style="font-size: 0.84rem; color: #94a3b8; line-height: 1.45;">
                Komparasi multi-negara dinamis, analisis pertumbuhan harapan hidup (Net Change & Growth %), dan tabel profil komparatif.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="metric-card accent-indigo">
            <div style="font-size: 1.4rem; margin-bottom: 8px;">🗺️</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #f9fafb; margin-bottom: 6px;">
                3. Geospatial Explorer
            </div>
            <div style="font-size: 0.84rem; color: #94a3b8; line-height: 1.45;">
                Peta choropleth dunia interaktif dengan pewarnaan gradien indikator, zoom, pan, tooltip detail, dan penanganan data kosong.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
col4, col5 = st.columns(2)

with col4:
    st.markdown(
        """
        <div class="metric-card accent-amber">
            <div style="font-size: 1.4rem; margin-bottom: 8px;">🔬</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #f9fafb; margin-bottom: 6px;">
                4. Correlation & Determinants
            </div>
            <div style="font-size: 0.84rem; color: #94a3b8; line-height: 1.45;">
                Analisis matriks korelasi Pearson/Spearman, scatter plot hubungan multivariat, dan deteksi anomali non-destruktif.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        """
        <div class="metric-card accent-rose">
            <div style="font-size: 1.4rem; margin-bottom: 8px;">📋</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #f9fafb; margin-bottom: 6px;">
                5. Data Audit & Methodology
            </div>
            <div style="font-size: 0.84rem; color: #94a3b8; line-height: 1.45;">
                Metodologi Two-Step Median Imputation (2.938 baris & 193 negara utuh), kamus data 22 atribut, dan batasan analisis CRISP-DM.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Quick Global Snapshot
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
st.markdown(f"### 📊 Snapshot Global Terpilih (Tahun {filters['year']})")

kpis = compute_global_kpis(df, year=filters['year'])
if kpis:
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        render_metric_card(
            label="Rata-rata Harapan Hidup",
            value=f"{kpis['mean_life_expectancy']} Thn",
            sub=f"Median: {kpis['median_life_expectancy']} Thn",
            accent="blue"
        )
    with mcol2:
        render_metric_card(
            label="Kesenjangan Disparitas",
            value=f"{kpis['disparity_gap']} Thn",
            sub="Selisih Developed vs Developing",
            accent="amber"
        )
    with mcol3:
        render_metric_card(
            label="Negara Maju (Avg LE)",
            value=f"{kpis['developed_avg_le']} Thn",
            sub=f"{kpis['developed_countries']} negara tercatat",
            accent="emerald"
        )
    with mcol4:
        render_metric_card(
            label="Negara Berkembang (Avg LE)",
            value=f"{kpis['developing_avg_le']} Thn",
            sub=f"{kpis['developing_countries']} negara tercatat",
            accent="rose"
        )
else:
    st.info("Tidak ada data untuk tahun terpilih.")
