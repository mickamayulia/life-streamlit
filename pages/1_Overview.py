"""
Overview & Global Trends Page
Displays headline KPIs, global time-series trajectory, and life expectancy distribution.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.data.loader import load_cleaned_data
from src.components.ui import apply_custom_css, render_hero, render_metric_card
from src.components.sidebar import render_sidebar_filters
from src.analytics.metrics import compute_global_kpis, compute_yearly_trends

# Page Config
st.set_page_config(page_title="Overview & Global Trends", page_icon="📈", layout="wide")
apply_custom_css()

# Data & Sidebar
df = load_cleaned_data()
filters = render_sidebar_filters(df, default_year=2014)

render_hero(
    title="Overview & Global Trends",
    subtitle="Pantau dinamika agregat angka harapan hidup global periode 2000–2015, evaluasi kesenjangan antar kelompok negara, dan telaah distribusi capaian kesehatan makro.",
    badge="MODUL 1 — RINGKASAN GLOBAL"
)

# 1. Headline KPIs for Snapshot Year
st.markdown(f"### 📌 Ringkasan Global Snapshot (Tahun {filters['year']})")
kpis = compute_global_kpis(df, year=filters['year'])

if kpis:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card(
            label="Rata-rata Harapan Hidup",
            value=f"{kpis['mean_life_expectancy']} Thn",
            sub=f"Median: {kpis['median_life_expectancy']} Thn (Std: ±{kpis['std_life_expectancy']})",
            accent="blue"
        )
    with c2:
        render_metric_card(
            label="Kesenjangan Disparitas",
            value=f"{kpis['disparity_gap']} Thn",
            sub="Selisih Maju vs Berkembang",
            accent="amber"
        )
    with c3:
        render_metric_card(
            label="Rentang Capaian Terendah - Tertinggi",
            value=f"{kpis['min_life_expectancy']} – {kpis['max_life_expectancy']}",
            sub=f"Rentang Sebaran: {round(kpis['max_life_expectancy'] - kpis['min_life_expectancy'], 1)} Thn",
            accent="rose"
        )
    with c4:
        sub_text = f"{kpis['total_countries']} negara tercatat di {filters['year']} ({kpis['developed_countries']} Maju | {kpis['developing_countries']} Berkembang)" if kpis['total_countries'] < kpis['overall_countries'] else f"{kpis['developed_countries']} Maju | {kpis['developing_countries']} Berkembang"
        render_metric_card(
            label="Total Negara Terpetakan",
            value=f"{kpis['overall_countries']} Negara",
            sub=sub_text,
            accent="emerald"
        )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# 2. Global Yearly Trends Chart
st.markdown("### 📈 Trajektori Tren Global (2000–2015)")

t_col1, t_col2 = st.columns([3, 1])
with t_col2:
    st.markdown("##### ⚙️ Opsi Agregasi")
    use_weighting = st.toggle("Bobotkan Populasi (Weighted)", value=False, help="Memperhitungkan proporsi jumlah penduduk negara terhadap rata-rata.")
    show_min_max = st.checkbox("Tampilkan Pita Rentang Min - Max", value=True)
    show_median = st.checkbox("Tampilkan Garis Median", value=True)

trends_df = compute_yearly_trends(df, indicator='Life_expectancy', weighted=use_weighting)

fig_trend = go.Figure()

# Min-Max Shaded Band
if show_min_max:
    fig_trend.add_trace(go.Scatter(
        x=trends_df['Year'].tolist() + trends_df['Year'].tolist()[::-1],
        y=trends_df['Max'].tolist() + trends_df['Min'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(2, 132, 199, 0.1)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Rentang Min - Max'
    ))

# Mean Line
fig_trend.add_trace(go.Scatter(
    x=trends_df['Year'],
    y=trends_df['Mean'],
    mode='lines+markers',
    name='Rata-Rata (Mean)' if not use_weighting else 'Rata-Rata Terbobot (Weighted Mean)',
    line=dict(color='#0284c7', width=3),
    marker=dict(size=7, color='#38bdf8'),
    hovertemplate="<b>Tahun %{x}</b><br>Rata-Rata: %{y:.2f} Tahun<extra></extra>"
))

# Median Line
if show_median:
    fig_trend.add_trace(go.Scatter(
        x=trends_df['Year'],
        y=trends_df['Median'],
        mode='lines+markers',
        name='Median',
        line=dict(color='#10b981', width=2, dash='dot'),
        marker=dict(size=5, color='#34d399'),
        hovertemplate="<b>Tahun %{x}</b><br>Median: %{y:.2f} Tahun<extra></extra>"
    ))

fig_trend.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(17, 24, 39, 0.7)",
    paper_bgcolor="rgba(11, 15, 25, 0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
    margin=dict(l=40, r=40, t=30, b=40),
    height=420,
    hovermode="x unified",
    xaxis=dict(
        title="Tahun",
        tickmode='linear',
        tick0=2000,
        dtick=1,
        gridcolor="rgba(255, 255, 255, 0.05)"
    ),
    yaxis=dict(
        title="Angka Harapan Hidup (Tahun)",
        gridcolor="rgba(255, 255, 255, 0.08)"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

with t_col1:
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# 3. Distribution & Status Comparison
st.markdown(f"### 📊 Sebaran & Distribusi Harapan Hidup (Tahun {filters['year']})")
dist_col1, dist_col2 = st.columns(2)

sub_df = df[df['Year'] == filters['year']].copy()
if filters['status'] != "Semua Status":
    sub_df = sub_df[sub_df['Status'] == filters['status']]

# Histogram / KDE
fig_hist = px.histogram(
    sub_df,
    x="Life_expectancy",
    color="Status",
    nbins=25,
    marginal="box",
    opacity=0.75,
    color_discrete_map={"Developing": "#f59e0b", "Developed": "#10b981"},
    labels={"Life_expectancy": "Angka Harapan Hidup (Tahun)", "count": "Jumlah Negara"},
    title=f"Distribusi Harapan Hidup (Tahun {filters['year']})"
)
fig_hist.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(17, 24, 39, 0.7)",
    paper_bgcolor="rgba(11, 15, 25, 0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
    height=400,
    margin=dict(l=30, r=30, t=50, b=30),
    xaxis=dict(gridcolor="rgba(255, 255, 255, 0.05)"),
    yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Boxplot Comparison
fig_box = px.box(
    df[df['Year'] == filters['year']],
    x="Status",
    y="Life_expectancy",
    color="Status",
    points="all",
    hover_data=["Country"],
    color_discrete_map={"Developing": "#f59e0b", "Developed": "#10b981"},
    labels={"Life_expectancy": "Angka Harapan Hidup (Tahun)", "Status": "Status Pembangunan"},
    title=f"Disparitas Sebaran: Developing vs Developed ({filters['year']})"
)
fig_box.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(17, 24, 39, 0.7)",
    paper_bgcolor="rgba(11, 15, 25, 0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#e5e7eb"),
    height=400,
    margin=dict(l=30, r=30, t=50, b=30),
    yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)"),
    showlegend=False
)

with dist_col1:
    st.plotly_chart(fig_hist, use_container_width=True)

with dist_col2:
    st.plotly_chart(fig_box, use_container_width=True)
