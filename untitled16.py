# dashboard_bike_sharing.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st  # Import library Streamlit

# Set tema seaborn
sns.set(style='whitegrid')

# Judul halaman
st.title("🚲 Bike Sharing Analysis Dashboard")
st.subheader("Analisis Pengaruh Cuaca dan Musim terhadap Jumlah Peminjaman Sepeda")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")  # Pastikan file ini ada di folder yang sama
    df['dteday'] = pd.to_datetime(df['dteday'])

    # Mapping label kategori
    season_dict = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weekday_dict = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
    weathersit_dict = {
        1: 'Clear/Few clouds',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    }

    df['season'] = df['season'].map(season_dict)
    df['weekday'] = df['weekday'].map(weekday_dict)
    df['weathersit'] = df['weathersit'].map(weathersit_dict)
    df['year'] = df['dteday'].dt.year
    df['month'] = df['dteday'].dt.month

    return df

# Panggil data
data = load_data()

# Sidebar filter
st.sidebar.header("🔍 Filter Data")
year_filter = st.sidebar.multiselect("Pilih Tahun", options=data['year'].unique(), default=data['year'].unique())
season_filter = st.sidebar.multiselect("Pilih Musim", options=data['season'].unique(), default=data['season'].unique())

# Filter data
filtered_data = data[(data['year'].isin(year_filter)) & (data['season'].isin(season_filter))]

# Tampilkan data
st.write("### 📅 Data yang Ditampilkan (5 Baris Teratas)")
st.dataframe(filtered_data[['dteday', 'season', 'weathersit', 'cnt']].head())

# Visualisasi 1: Rata-rata peminjaman per musim
st.write("## 🔸 Rata-rata Peminjaman Sepeda per Musim")
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=filtered_data, x='season', y='cnt', estimator='mean', ci=None, palette='coolwarm', ax=ax1)
ax1.set_ylabel("Jumlah Peminjaman")
ax1.set_xlabel("Musim")
st.pyplot(fig1)

# Visualisasi 2: Rata-rata peminjaman per kondisi cuaca
st.write("## 🔸 Rata-rata Peminjaman Sepeda per Kondisi Cuaca")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_data, x='weathersit', y='cnt', estimator='mean', ci=None, palette='viridis', ax=ax2)
ax2.set_ylabel("Jumlah Peminjaman")
ax2.set_xlabel("Kondisi Cuaca")
ax2.tick_params(axis='x', rotation=15)
st.pyplot(fig2)

# Insight
st.markdown("""
### 💡 Insight
- Musim **Fall** menunjukkan jumlah peminjaman tertinggi.
- Cuaca **cerah** memiliki korelasi kuat dengan tingginya aktivitas bersepeda.
""")
