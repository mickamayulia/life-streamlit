"""
Geospatial Explorer Page
Interactive World Choropleth Map using Plotly Express with ISO-3 code alignment,
custom tooltips, indicator selection, country rankings, and graceful handling of missing regions.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.data.loader import load_cleaned_data, INDICATOR_METADATA
from src.components.ui import apply_custom_css, render_hero, render_metric_card
from src.components.sidebar import render_sidebar_filters
from src.analytics.metrics import get_country_rankings
from src.analytics.anomaly import compute_anomaly_flags

# Page Config
st.set_page_config(page_title="Geospatial Explorer", page_icon="🗺️", layout="wide")
apply_custom_css()

# Data & Sidebar
df = load_cleaned_data()
filters = render_sidebar_filters(df, default_year=2014)

# Flag anomalies for tooltip integration
df_flagged = compute_anomaly_flags(df, indicators=['Life_expectancy', 'GDP', 'Adult_Mortality', 'Schooling'])

render_hero(
    title="Geospatial Explorer — World Health Distribution",
    subtitle="Eksplorasi disparitas geografis angka harapan hidup dan indikator sosio-ekonomi global melalui peta koroplet interaktif berbasis kode ISO-3 Alpha. Analisis pola spasial dan ketimpangan lintas benua.",
    badge="MODUL 3 — ANALISIS GEOSPASIAL"
)

# 1. Indicator & Map Controls
st.markdown("### ⚙️ Pengaturan Peta Geospasial")

c_col1, c_col2, c_col3 = st.columns([2, 1, 1])

with c_col1:
    indicator_options = list(INDICATOR_METADATA.keys())
    indicator_labels = {k: f"{v['label']} ({v['unit']})" for k, v in INDICATOR_METADATA.items()}
    selected_indicator = st.selectbox(
        "Pilih Indikator yang Dipetakan:",
        options=indicator_options,
        format_func=lambda x: indicator_labels.get(x, x),
        index=0
    )

with c_col2:
    color_scale_options = {
        "Viridis (Default)": "Viridis",
        "Plasma (Kontras Tinggi)": "Plasma",
        "Teal & Biru (Muted)": "Blues",
        "Sunset (Hangat)": "Sunset",
        "Spectral (Divergen)": "Spectral"
    }
    selected_color_scale = st.selectbox(
        "Skala Gradien Warna:",
        options=list(color_scale_options.keys()),
        index=0
    )

with c_col3:
    map_projection_options = {
        "Natural Earth (Datar)": "natural earth",
        "Equirectangular": "equirectangular",
        "Mercator": "mercator",
        "Orthographic (Globe 3D)": "orthographic"
    }
    selected_projection = st.selectbox(
        "Proyeksi Peta:",
        options=list(map_projection_options.keys()),
        index=0
    )

meta = INDICATOR_METADATA.get(selected_indicator, {'label': selected_indicator, 'unit': ''})

# Filter data for active snapshot year
map_data = df_flagged[df_flagged['Year'] == filters['year']].copy()
if filters['status'] != "Semua Status":
    map_data = map_data[map_data['Status'] == filters['status']]

# Anomaly flag string for nice tooltip display
flag_col = f"{selected_indicator}_is_anomaly"
if flag_col in map_data.columns:
    map_data['Anomaly_Status'] = map_data[flag_col].apply(lambda x: "⚠️ Ya (Nilai Ekstrem)" if x else "Normal")
else:
    map_data['Anomaly_Status'] = "Normal"

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# 2. Interactive World Choropleth Map
st.markdown(f"### 🗺️ Peta Distribusi Global: {meta['label']} (Tahun {filters['year']})")

if not map_data.empty and selected_indicator in map_data.columns:
    fig_map = px.choropleth(
        map_data,
        locations="iso_alpha",
        color=selected_indicator,
        hover_name="Country",
        hover_data={
            "iso_alpha": False,
            "Status": True,
            "Year": True,
            selected_indicator: ":.2f",
            "Anomaly_Status": True,
            "Population": ":,.0f" if "Population" in map_data.columns else False
        },
        color_continuous_scale=color_scale_options[selected_color_scale],
        projection=map_projection_options[selected_projection],
        labels={
            selected_indicator: f"{meta['label']} ({meta['unit']})",
            "Anomaly_Status": "Status Anomali"
        }
    )

    # Clean Dark UI Styling for Map
    fig_map.update_geos(
        showcoastlines=True,
        coastlinecolor="rgba(255, 255, 255, 0.2)",
        showocean=True,
        oceancolor="rgba(11, 15, 25, 0.9)",
        showland=True,
        landcolor="rgba(31, 41, 55, 0.6)", # Base color for countries without data
        showlakes=True,
        lakecolor="rgba(11, 15, 25, 0.9)",
        showcountries=True,
        countrycolor="rgba(255, 255, 255, 0.15)",
        bgcolor="rgba(11, 15, 25, 0)"
    )

    fig_map.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(11, 15, 25, 0)",
        plot_bgcolor="rgba(11, 15, 25, 0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=540,
        coloraxis_colorbar=dict(
            title=f"{meta['label']}<br><span style='font-size: 10px;'>({meta['unit']})</span>",
            thicknessmode="pixels",
            thickness=14,
            lenmode="fraction",
            len=0.75,
            yanchor="middle",
            y=0.5,
            ticks="outside"
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.caption(
        "💡 **Keterangan:** Wilayah abu-abu gelap menandakan negara yang tidak tercakup dalam observasi dataset tahun ini (*No Data Available*). "
        "Arahkan kursor (*hover*) pada negara untuk memeriksa detail angka dan status anomali. Gunakan tombol zoom dan pan di pojok kanan atas grafik."
    )
else:
    st.warning(f"Tidak ada data geospasial yang tersedia untuk indikator {selected_indicator} pada tahun {filters['year']}.")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# 3. Spatial Extremes & Country Rankings
st.markdown(f"### 🏆 Peringkat Negara Berdasarkan {meta['label']} (Tahun {filters['year']})")

r_col1, r_col2 = st.columns(2)

with r_col1:
    st.markdown(f"##### 🟢 Top 10 Tertinggi ({meta['label']})")
    top_df = get_country_rankings(
        df,
        year=filters['year'],
        indicator=selected_indicator,
        top_n=10,
        ascending=False
    )
    if not top_df.empty:
        st.dataframe(
            top_df.rename(columns={
                'iso_alpha': 'ISO-3',
                selected_indicator: f"{meta['label']} ({meta['unit']})"
            }),
            use_container_width=True
        )
    else:
        st.info("Data ranking tidak tersedia.")

with r_col2:
    st.markdown(f"##### 🔴 Bottom 10 Terendah ({meta['label']})")
    bot_df = get_country_rankings(
        df,
        year=filters['year'],
        indicator=selected_indicator,
        top_n=10,
        ascending=True
    )
    if not bot_df.empty:
        st.dataframe(
            bot_df.rename(columns={
                'iso_alpha': 'ISO-3',
                selected_indicator: f"{meta['label']} ({meta['unit']})"
            }),
            use_container_width=True
        )
    else:
        st.info("Data ranking tidak tersedia.")
