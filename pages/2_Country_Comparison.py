"""
Country Comparison & Benchmarking Page
Allows dynamic multi-country selection, comparative time series, net change calculations, and radar/profile tables.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.data.loader import load_cleaned_data, NUMERIC_INDICATORS, INDICATOR_METADATA
from src.components.ui import apply_custom_css, render_hero, render_metric_card
from src.components.sidebar import render_sidebar_filters
from src.analytics.metrics import compute_country_comparison_data

# Page Config
st.set_page_config(page_title="Country Comparison", page_icon="⚖️", layout="wide")
apply_custom_css()

# Data & Filters
df = load_cleaned_data()
filters = render_sidebar_filters(df, default_year=2014)

render_hero(
    title="Country Explorer & Multi-Country Benchmarking",
    subtitle="Bandingkan trajektori angka harapan hidup dan indikator determinan antar-negara secara interaktif. Evaluasi disparitas absolut dan persentase perubahan sepanjang periode observasi.",
    badge="MODUL 2 — KOMPARASI NEGARA"
)

# 1. Country Selection Controls
st.markdown("### 🔍 Pemilihan Negara & Indikator Komparasi")

ctrl_col1, ctrl_col2 = st.columns([2, 1])

with ctrl_col1:
    selected_countries = st.multiselect(
        "Pilih Negara untuk Dikomparasi (Maksimal Disarankan 6-8 Negara):",
        options=filters['all_countries'],
        default=filters['default_countries']
    )

with ctrl_col2:
    indicator_options = list(INDICATOR_METADATA.keys())
    indicator_labels = {k: f"{v['label']} ({v['unit']})" for k, v in INDICATOR_METADATA.items()}
    selected_indicator = st.selectbox(
        "Pilih Indikator yang Dianalisis:",
        options=indicator_options,
        format_func=lambda x: indicator_labels.get(x, x),
        index=0
    )

if not selected_countries:
    st.warning("Silakan pilih minimal 1 negara pada kotak di atas untuk melihat perbandingan.")
    st.stop()

# 2. Comparative Time-Series Chart
meta = INDICATOR_METADATA.get(selected_indicator, {'label': selected_indicator, 'unit': ''})
st.markdown(f"### 📈 Perbandingan Tren: {meta['label']}")

sub_df, summary_df = compute_country_comparison_data(
    df,
    countries=selected_countries,
    indicator=selected_indicator
)

if not sub_df.empty:
    fig_comp = px.line(
        sub_df,
        x="Year",
        y=selected_indicator,
        color="Country",
        markers=True,
        labels={"Year": "Tahun", selected_indicator: f"{meta['label']} ({meta['unit']})"},
        title=f"Pergerakan {meta['label']} ({sub_df['Year'].min()} – {sub_df['Year'].max()})"
    )

    fig_comp.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(17, 24, 39, 0.7)",
        paper_bgcolor="rgba(11, 15, 25, 0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
        height=450,
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        xaxis=dict(
            tickmode='linear',
            tick0=2000,
            dtick=1,
            gridcolor="rgba(255, 255, 255, 0.05)"
        ),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# 3. Growth & Net Change Performance Table
st.markdown("### 📊 Ringkasan Pertumbuhan & Perubahan Bersih")
st.markdown(
    "Tabel di bawah mengukur capaian awal, akhir, kenaikan absolut (*Net Change*), dan tingkat pertumbuhan relatif (*Growth %*) untuk negara terpilih:"
)

if not summary_df.empty:
    # Stylized formatting for data frame
    styled_df = summary_df.copy()
    styled_df['Net Change'] = styled_df['Net Change'].apply(lambda x: f"{'+' if x > 0 else ''}{x:.2f}")
    styled_df['Change (%)'] = styled_df['Change (%)'].apply(lambda x: f"{'+' if x > 0 else ''}{x:.2f}%")

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# 4. Multi-Indicator Country Profile Snapshot
st.markdown(f"### 📋 Profil Multidimensi Negara Terpilih (Tahun {filters['year']})")

profile_cols = [
    'Country', 'Status', 'Life_expectancy', 'Adult_Mortality',
    'GDP', 'Schooling', 'BMI', 'HIV/AIDS', 'Income_composition_of_resources'
]
snapshot_df = df[(df['Year'] == filters['year']) & (df['Country'].isin(selected_countries))][profile_cols].copy()

if not snapshot_df.empty:
    st.dataframe(
        snapshot_df.rename(columns={
            'Life_expectancy': 'Harapan Hidup (Thn)',
            'Adult_Mortality': 'Mortalitas Dewasa (/1000)',
            'GDP': 'PDB per Kapita ($)',
            'Schooling': 'Lama Sekolah (Thn)',
            'BMI': 'BMI Rata-rata',
            'HIV/AIDS': 'Kematian HIV/AIDS',
            'Income_composition_of_resources': 'Indeks HDI'
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info(f"Tidak ada catatan observasi lengkap untuk negara terpilih pada tahun {filters['year']}.")
