# Life Expectancy Global Analytics Dashboard 🌐

> **IS Capstone — Analisis Data dan Kecerdasan Bisnis**  
> Program Studi Sistem Informasi, Institut Teknologi Kalimantan (ITK), 2026  
> **Kelompok 7:** Micka Mayulia Utama (10231053), Ade Ayu Kholifah Putri (10231004), Riska Fadlun Khairiyah Purba (10231083)  
> **Dosen Pembimbing:** Hendy Indrawan Sunardi S.Kom, M.Eng.

---

## 📌 Ringkasan Proyek

**Life Expectancy Global Analytics Dashboard** adalah platform *Business Intelligence* (BI) dan *Exploratory Data Analysis* (EDA) berbasis web interaktif untuk menganalisis angka harapan hidup (*Life Expectancy*) di 133 negara dunia sepanjang periode 2000–2015.

Aplikasi ini menyajikan wawasan multidimensi yang mengintegrasikan determinan kesehatan, sosio-ekonomi, pendidikan, demografi, serta disparitas makro antar kelompok negara maju (*Developed*) dan negara berkembang (*Developing*).

---

## ✨ Fitur Utama Dashboard

Aplikasi dibangun menggunakan arsitektur **Multipage Streamlit** dengan 5 modul penjelajahan:

1. **📈 1_Overview & Global Trends:**
   - Headline KPI snapshot global: Rata-rata, median, standar deviasi, dan rentang disparitas *Developed vs Developing*.
   - Trajektori tren deret waktu 2000–2015 dengan pita rentang *Min-Max* dan opsi pembobotan populasi (*Population-Weighted Average*).
   - Visualisasi distribusi histogram & boxplot sebaran harapan hidup per kelompok status.

2. **⚖️ 2_Country_Comparison:**
   - Multi-country selector dinamis untuk membandingkan trajektori antarnegara terpilih.
   - Grafik deret waktu multi-line interaktif dengan tooltip terpadu.
   - Tabel performa pertumbuhan otomatis (*Start Value*, *End Value*, *Net Change*, dan *Growth %*).
   - Profil komparasi multidimensi indikator kesehatan dan sosio-ekonomi.

3. **🗺️ 3_Geospatial_Explorer:**
   - Peta koroplet dunia interaktif berbasis kode standar **ISO-3 Alpha** (133/133 negara terpetakan 100%).
   - Dukungan zoom, pan, rotasi bola dunia 3D (*Orthographic Globe*), dan seleksi gradien warna (*Viridis, Plasma, Sunset, dll*).
   - Tooltip kustom detail dan penanganan transparan negara tanpa data (*No Data Available*).
   - Tabel peringkat Top 10 Tertinggi dan Bottom 10 Terendah per indikator.

4. **🔬 4_Correlation_and_Determinants:**
   - Matriks korelasi heatmap interaktif dengan metode **Pearson (Linier)** dan **Spearman (Monotonik / Robust)**.
   - Scatter plot bivariat dengan garis tren regresi OLS (*Ordinary Least Squares*) dan opsi skala logaritmik sumbu X.
   - Mesin inspeksi anomali (*Outlier Detection*) non-destruktif berbasis metode IQR 1.5x dan Z-Score.

5. **📋 5_Data_Audit_and_Methodology:**
   - Transparansi komparasi data mentah Kaggle (2.938 baris) vs data yang digunakan (1.649 baris).
   - Kamus data lengkap (*Data Dictionary*) 22 atribut.
   - Dokumentasi batasan metodologis CRISP-DM dan penegasan prinsip non-kausalitas (*correlation does not imply causation*).

---

## 🚀 Panduan Menjalankan Aplikasi Secara Lokal

### 1. Prasyarat Sistem
- Python 3.10, 3.11, atau 3.12 terinstal di komputer.
- Koneksi internet (untuk mengunduh pustaka saat instalasi awal).

### 2. Kloning atau Buka Direktori Proyek
Buka terminal (Command Prompt / PowerShell / Bash) di folder proyek:
```bash
cd "d:/Kuliah/Semester 7/CAPSTONE/PROJECT"
```

### 3. Instalasi Dependensi
Jalankan perintah instalasi dependensi dari file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard
Jalankan aplikasi menggunakan Streamlit:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser default Anda pada alamat:
👉 **`http://localhost:8501`**

---

## ☁️ Panduan Deployment ke Streamlit Community Cloud (Gratis)

Aplikasi ini sudah dirancang **100% cloud-ready** untuk di-deploy ke **Streamlit Community Cloud**:

1. **Inisialisasi Git & Push ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "feat: complete life expectancy global analytics dashboard"
   git branch -M main
   git remote add origin https://github.com/<username-anda>/<nama-repo-anda>.git
   git push -u origin main
   ```
2. **Koneksikan ke Streamlit Cloud:**
   - Kunjungi [share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub Anda.
   - Klik tombol **"New app"**.
   - Pilih repositori GitHub Anda, Branch: `main`, Main file path: `app.py`.
   - Klik **"Deploy"**.
3. **Selesai!** Dashboard analitik Anda akan langsung aktif secara publik dengan URL gratis (misal: `https://life-expectancy-dashboard.streamlit.app`).

---

## 📂 Struktur Direktori Proyek

```text
PROJECT/
├── .streamlit/
│   └── config.toml                  # Konfigurasi tema dark mode & UI Streamlit
├── doc/
│   ├── IS CAPSTONE KELOMPOK 7.md    # Proposal Laporan Akademik Resmi
│   ├── prd.md                       # Product Requirements Document
│   └── stage0.md                    # Panduan Stage 0 Discovery
├── excel/
│   ├── Life Expectancy Data.csv     # Dataset mentah asli Kaggle WHO (2.938 baris)
│   └── life_expectancy_cleaned_dataset.xlsx # Dataset terverifikasi (1.649 baris)
├── pages/
│   ├── 1_Overview.py                # Modul 1: Ringkasan Global & Tren Deret Waktu
│   ├── 2_Country_Comparison.py      # Modul 2: Komparasi Antar-Negara & Pertumbuhan
│   ├── 3_Geospatial_Explorer.py     # Modul 3: Peta Koroplet Dunia Interaktif
│   ├── 4_Correlation_and_Determinants.py # Modul 4: Korelasi, Determinan & Anomali
│   └── 5_Data_Audit_and_Methodology.py   # Modul 5: Audit Integritas Data & Metodologi
├── src/
│   ├── analytics/
│   │   ├── anomaly.py               # Mesin deteksi outlier non-destruktif (IQR & Z-Score)
│   │   └── metrics.py               # Mesin komputasi statistik, tren, dan korelasi
│   ├── components/
│   │   ├── sidebar.py               # Komponen filter global sidebar
│   │   └── ui.py                    # Styling CSS, kartu metrik glassmorphism, dan badge
│   └── data/
│       └── loader.py                # Pipeline ingestion data, caching @st.cache_data & metadata
├── tests/
│   └── test_qa_suite.py             # Skrip uji otomatis integritas data & QA
├── app.py                           # Root Entrypoint Navigasi Dashboard
├── requirements.txt                 # Dependensi Python aplikasi
├── DATA_AUDIT.md                    # Laporan audit mendalam raw vs cleaned dataset
├── DECISIONS.md                     # Catatan keputusan teknis arsitektur
├── PROJECT_CONTEXT.md               # Ringkasan konteks akademik & aset proyek
├── TASKS.md                         # Roadmap backlog pengerjaan Stage 0 s.d. Stage 8
└── README.md                        # Dokumentasi utama proyek & panduan deployment
```

---

## 🧪 Pengujian Kualitas (QA Test Suite)

Untuk memvalidasi integritas data dan kalkulasi numerik secara otomatis, jalankan:
```bash
python tests/test_qa_suite.py
```
Semua 4 suite uji (Ingestion, KPI Consistency, Correlation Engine, dan Edge Case Fallback) telah terverifikasi dengan status **100% Passed**.

---
*Dibuat dengan dedikasi untuk mendukung penelitian kesehatan global dan pencapaian target SDGs.*
