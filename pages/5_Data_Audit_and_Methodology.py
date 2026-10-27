"""
Data Audit, Quality Profile & Methodology Page
Presents transparent comparisons between raw CSV (2,938 rows) and cleaned dataset (1,649 rows),
data dictionary, missing value audit, and methodological constraints for academic integrity.
"""

import streamlit as st
import pandas as pd

from src.data.loader import load_cleaned_data, load_raw_data, get_dataset_summary, INDICATOR_METADATA
from src.components.ui import apply_custom_css, render_hero, render_metric_card
from src.components.sidebar import render_sidebar_filters

# Page Config
st.set_page_config(page_title="Data Audit & Methodology", page_icon="📋", layout="wide")
apply_custom_css()

# Load Data
df_clean = load_cleaned_data()
filters = render_sidebar_filters(df_clean, default_year=2014)

render_hero(
    title="Data Audit, Quality Profile & Methodology",
    subtitle="Transparansi integritas data, komparasi dataset mentah Kaggle (WHO) vs dataset yang digunakan, kamus data lengkap, serta batasan analisis berdasarkan metodologi CRISP-DM.",
    badge="MODUL 5 — AUDIT DATA & METODOLOGI"
)

summary = get_dataset_summary()

# 1. Headline Audit Comparison Cards
st.markdown("### 🔍 Komparasi Integritas Data (Raw vs Cleaned)")

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card(
        label="Dataset Mentah (Raw Kaggle)",
        value=f"{summary['raw_rows']:,} Baris",
        sub=f"{summary['raw_countries']} Negara | 22 Kolom",
        accent="amber"
    )
with c2:
    render_metric_card(
        label="Dataset Digunakan (Cleaned)",
        value=f"{summary['clean_rows']:,} Baris",
        sub=f"{summary['clean_countries']} Negara | 22 Kolom",
        accent="emerald"
    )
with c3:
    render_metric_card(
        label="Nilai Kosong (Missing Values)",
        value="0 Null",
        sub=f"Raw memiliki {summary['raw_nulls']:,} null",
        accent="blue"
    )
with c4:
    render_metric_card(
        label="Validitas Geospasial ISO-3",
        value="100% Terpetakan",
        sub="0 negara unmapped",
        accent="indigo"
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# 2. Tabs for Audit Views
tab_comp, tab_dict, tab_notes = st.tabs([
    "📊 Analisis Reduksi Data & Missing Values",
    "📖 Kamus Data (Data Dictionary)",
    "⚠️ Batasan Metodologis & CRISP-DM"
])

with tab_comp:
    st.markdown("#### Metodologi Imputasi Missing Values & Struktur Data")
    st.markdown(
        """
        Pada dataset mentah WHO dari Kaggle (`Life Expectancy Data.csv`), terdapat **2.938 observasi** pada **193 negara** dengan **2.563 total missing values** yang tersebar di berbagai indikator numerik.
        
        Untuk mempertahankan seluruh baris dan representasi negara tanpa membuang informasi (berbeda dari pemotongan baris/*listwise deletion* terdahulu), sistem menerapkan **Two-Step Median Imputation**:
        1. **Nilai kosong diisi dengan median variabel tersebut pada negara yang sama.**
        2. **Nilai yang masih kosong diisi dengan median seluruh data.**
        
        > **Justifikasi Metodologis:**  
        > *Metode median dipilih karena sebagian besar variabel memiliki distribusi miring dan mengandung pencilan, sehingga median lebih stabil terhadap nilai ekstrim. Setelah proses ini, jumlah missing value menjadi 0.*
        """
    )

    try:
        df_raw = load_raw_data()
        raw_nulls = df_raw.isnull().sum()
        clean_nulls = df_clean.isnull().sum()

        null_df = pd.DataFrame({
            'Nama Kolom': raw_nulls.index,
            'Missing Value (Raw Kaggle)': raw_nulls.values,
            'Persentase Null Raw (%)': (raw_nulls.values / len(df_raw) * 100).round(2),
            'Missing Value (Cleaned)': [clean_nulls.get(col, 0) for col in raw_nulls.index]
        })

        st.dataframe(null_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.warning(f"Gagal memuat raw CSV untuk tabel perbandingan: {e}")

with tab_dict:
    st.markdown("#### Kamus Indikator & Variabel")
    dict_records = []
    for col, meta in INDICATOR_METADATA.items():
        dict_records.append({
            'Nama Atribut (Dataset)': col,
            'Label Tampilan': meta['label'],
            'Kategori': meta['category'],
            'Satuan Pengukuran': meta['unit'],
            'Tipe Data': str(df_clean[col].dtype) if col in df_clean.columns else 'numeric'
        })
    dict_df = pd.DataFrame(dict_records)
    st.dataframe(dict_df, use_container_width=True, hide_index=True)

with tab_notes:
    st.markdown("#### Batasan Metodologis & Integritas Ilmiah")
    st.markdown(
        """
        1. **Larangan Klaim Kausalitas (*No Causality Claim*):**  
           Proyek ini dirancang sebagai platform *Exploratory Data Analysis* (EDA) deskriptif. Hubungan korelasi tinggi (seperti antara lama sekolah dan harapan hidup) tidak boleh diinterpretasikan sebagai bukti sebab-akibat deterministik tanpa eksperimen acak atau pemodelan kausal lanjutan.
        
        2. **Panel Data Lintas Waktu (*Historical Panel Observations*):**  
           Dataset mencakup rentang waktu 2000–2015 untuk 193 negara dunia (183 negara tercatat konsisten setiap tahun, dan 10 negara tercatat parsial pada tahun 2013). Tahun **2014 dipilih sebagai default snapshot komparasi global terkini** yang mencakup 183 negara secara serempak.
        
        3. **Skala Kematian Bayi & Balita (*Scale Inconsistencies*):**  
           Pada dataset publik WHO/Kaggle, nilai `infant_deaths` dan `under-five_deaths` pada negara berpenduduk sangat besar (seperti India) mencatat nilai absolut dalam ribuan jiwa, bukan rasio per 1.000 kelahiran hidup. Analis disarankan mengacu pada angka relatif per kapita untuk komparasi lintas negara.
        """
    )
