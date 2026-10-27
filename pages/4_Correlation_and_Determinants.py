"""
Correlation, Determinants & Anomaly Explorer Page
Analyzes multivariate relationships (health, economic, educational) with Life Expectancy,
interactive Pearson & Spearman correlation heatmaps, regression trendlines, and non-destructive anomaly inspection.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from src.data.loader import load_cleaned_data, INDICATOR_METADATA
from src.components.ui import apply_custom_css, render_hero, render_metric_card
from src.components.sidebar import render_sidebar_filters
from src.analytics.metrics import compute_correlation_matrix
from src.analytics.anomaly import compute_anomaly_flags, get_anomaly_summary

# Page Config
st.set_page_config(page_title="Correlation & Determinants", page_icon="🔬", layout="wide")
apply_custom_css()

# Data & Sidebar
df = load_cleaned_data()
filters = render_sidebar_filters(df, default_year=2014)

render_hero(
    title="Correlation, Determinants & Anomaly Explorer",
    subtitle="Eksplorasi hubungan multivariat antara indikator kesehatan, ekonomi, dan pendidikan terhadap angka harapan hidup. Telaah matriks korelasi dan inspeksi observasi anomali secara non-destruktif.",
    badge="MODUL 4 — ANALISIS MULTIVARIAT & ANOMALI"
)

# Disclaimer Alert
st.info(
    "⚠️ **Prinsip Metodologis (Non-Kausalitas):** Seluruh visualisasi korelasi dan garis tren di bawah ini bersifat **eksploratif dan deskriptif**. "
    "Korelasi yang kuat tidak membuktikan hubungan sebab-akibat deterministik (*correlation does not imply causation*)."
)

# Tabs for Organized Navigation
tab_corr, tab_scatter, tab_anomaly = st.tabs([
    "📊 Matriks Korelasi (Heatmap)",
    "📈 Bivariat & Determinan (Scatter)",
    "⚠️ Inspeksi Anomali & Disparitas"
])

# ==========================================
# TAB 1: CORRELATION HEATMAP
# ==========================================
with tab_corr:
    st.markdown("### 📊 Matriks Korelasi Multivariat")
    
    h_col1, h_col2 = st.columns([3, 1])
    with h_col2:
        corr_method = st.radio(
            "Metode Korelasi:",
            options=["pearson", "spearman"],
            format_func=lambda x: "Pearson (Linier)" if x == "pearson" else "Spearman (Monotonik / Robust)",
            index=0
        )
        use_year_filter = st.checkbox("Batasi pada Tahun Snapshot Aktif", value=False)
        corr_year = filters['year'] if use_year_filter else None

    # Compute correlation
    corr_df = compute_correlation_matrix(df, method=corr_method, year=corr_year)

    fig_corr = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1.0,
        zmax=1.0,
        labels=dict(color="Koefisien Korelasi (r)"),
        title=f"Matriks Korelasi Indikator ({corr_method.capitalize()}) — {'Semua Tahun' if corr_year is None else f'Tahun {corr_year}'}"
    )

    fig_corr.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(17, 24, 39, 0.7)",
        paper_bgcolor="rgba(11, 15, 25, 0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
        height=620,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    with h_col1:
        st.plotly_chart(fig_corr, use_container_width=True)

    # Ranking Correlation with Life Expectancy
    st.markdown("##### 📌 Korelasi Terhadap Angka Harapan Hidup (*Life Expectancy*)")
    le_corr = corr_df['Life_expectancy'].drop('Life_expectancy').sort_values(ascending=False).reset_index()
    le_corr.columns = ['Indikator', 'Koefisien Korelasi (r)']
    le_corr['Arah Hubungan'] = le_corr['Koefisien Korelasi (r)'].apply(
        lambda x: "🟢 Positif Kuat" if x >= 0.6 else ("🟢 Positif Sedang" if x >= 0.3 else ("🔴 Negatif Kuat" if x <= -0.6 else ("🔴 Negatif Sedang" if x <= -0.3 else "⚪ Lemah / Netral")))
    )
    
    st.dataframe(le_corr, use_container_width=True, hide_index=True)


# ==========================================
# TAB 2: SCATTER PLOT & DETERMINANTS
# ==========================================
with tab_scatter:
    st.markdown("### 📈 Hubungan Bivariat dengan Angka Harapan Hidup")

    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        det_options = [c for c in list(INDICATOR_METADATA.keys()) if c != 'Life_expectancy']
        selected_x = st.selectbox(
            "Pilih Variabel Independen (Sumbu X):",
            options=det_options,
            format_func=lambda x: f"{INDICATOR_METADATA[x]['label']} ({INDICATOR_METADATA[x]['unit']})",
            index=det_options.index('Schooling') if 'Schooling' in det_options else 0
        )
    with s_col2:
        color_by = st.selectbox(
            "Warnai Titik Berdasarkan:",
            options=["Status", "Tahun", "Region"],
            format_func=lambda x: "Status Pembangunan (Maju / Berkembang)" if x == "Status" else ("Tahun Observasi" if x == "Tahun" else "Satu Warna"),
            index=0
        )
    with s_col3:
        apply_log = st.checkbox("Gunakan Skala Logaritmik Sumbu X (Cocok untuk GDP/Populitas)", value=(selected_x in ['GDP', 'Population', 'percentage_expenditure']))

    meta_x = INDICATOR_METADATA.get(selected_x, {'label': selected_x, 'unit': ''})
    
    scatter_data = df.copy()
    if filters['status'] != "Semua Status":
        scatter_data = scatter_data[scatter_data['Status'] == filters['status']]

    fig_scatter = px.scatter(
        scatter_data,
        x=selected_x,
        y="Life_expectancy",
        color="Status" if color_by == "Status" else ("Year" if color_by == "Tahun" else None),
        color_discrete_map={"Developing": "#f59e0b", "Developed": "#10b981"},
        trendline="ols",
        log_x=apply_log,
        hover_name="Country",
        hover_data={"Year": True, "Life_expectancy": ":.2f", selected_x: ":.2f", "Status": True},
        labels={
            selected_x: f"{meta_x['label']} ({meta_x['unit']})",
            "Life_expectancy": "Angka Harapan Hidup (Tahun)"
        },
        title=f"Hubungan antara {meta_x['label']} vs Angka Harapan Hidup"
    )

    fig_scatter.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(17, 24, 39, 0.7)",
        paper_bgcolor="rgba(11, 15, 25, 0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
        height=500,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.05)"),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


# ==========================================
# TAB 3: ANOMALY INSPECTION
# ==========================================
with tab_anomaly:
    st.markdown("### ⚠️ Inspeksi Anomali & Disparitas Non-Destruktif")
    st.markdown(
        "Sesuai kaidah audit data, observasi ekstrem **tidak dihapus**, melainkan ditandai (*flagged*) "
        "agar peneliti dapat mengidentifikasi kemungkinan kesalahan pencatatan atau kondisi khusus wilayah."
    )

    a_col1, a_col2 = st.columns([1, 1])
    with a_col1:
        anom_method = st.radio("Metode Deteksi Anomali:", options=["iqr", "zscore"], format_func=lambda x: "IQR (Interquartile Range 1.5x)" if x == "iqr" else "Z-Score (|z| > 3.0)")
    with a_col2:
        by_status = st.checkbox("Hitung Ambang Batas Terpisah per Kelompok Status (Developing vs Developed)", value=False)

    flagged_df = compute_anomaly_flags(
        df,
        indicators=['Life_expectancy', 'Adult_Mortality', 'GDP', 'Schooling', 'HIV/AIDS', 'BMI'],
        method=anom_method,
        by_status=by_status
    )

    summary_anom = get_anomaly_summary(
        flagged_df,
        indicators=['Life_expectancy', 'Adult_Mortality', 'GDP', 'Schooling', 'HIV/AIDS', 'BMI']
    )

    st.markdown("##### 📋 Ringkasan Jumlah Anomali Terdeteksi")
    st.dataframe(summary_anom, use_container_width=True, hide_index=True)

    # Filter to show flagged rows
    st.markdown("##### 🔍 Observasi yang Ditandai Memiliki Anomali")
    inspect_ind = st.selectbox(
        "Pilih Indikator untuk Melihat Daftar Observasi Anomali:",
        options=['Life_expectancy', 'Adult_Mortality', 'GDP', 'Schooling', 'HIV/AIDS']
    )
    flag_col_name = f"{inspect_ind}_is_anomaly"
    display_cols = ['Country', 'Year', 'Status', inspect_ind]
    if 'Life_expectancy' not in display_cols:
        display_cols.append('Life_expectancy')

    anom_rows = flagged_df[flagged_df[flag_col_name]][display_cols].sort_values(by=inspect_ind, ascending=False)
    
    st.write(f"Menampilkan **{len(anom_rows)} baris** yang memiliki nilai anomali pada `{inspect_ind}`:")
    st.dataframe(anom_rows, use_container_width=True, hide_index=True)
