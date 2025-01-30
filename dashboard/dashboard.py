import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
print("Current Working Directory:", os.getcwd())
from babel.numbers import format_currency
sns.set(style='dark')


days_df = pd.read_csv("dashboard/days.csv")
days_df.head()

days_df['weekday'] = pd.Categorical(days_df['weekday'], categories=
    ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'],ordered=True)

def create_use_df(df):
    daily_use_df = df.groupby(by='Date_Day').agg({
        'count': 'sum'
    }).reset_index()
    return daily_use_df

def create_register_df(df):
    daily_register_df = df.groupby(by='Date_Day').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_register_df

def create_casual_df(df):
    daily_casual_df = df.groupby(by='Date_Day').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_df

def create_season_df(df):
    daily_season_df = df.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()
    return daily_season_df

def create_weekday_df(df):
    daily_weekday_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_weekday_df



datetime_columns = ["Date_Day"]
days_df.sort_values(by="Date_Day", inplace=True)
days_df.reset_index(inplace=True)
 
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])


min_date = days_df["Date_Day"].min()
max_date = days_df["Date_Day"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("dashboard/images.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Periode Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = days_df[(days_df["Date_Day"] >= str(start_date)) & (days_df["Date_Day"] <= str(end_date))]

daily_use_df = create_use_df(main_df)
daily_season_df = create_season_df(main_df)
daily_weekday_df = create_weekday_df(main_df)
daily_register_df = create_register_df(main_df)
daily_casual_df = create_casual_df(main_df)



st.header('📊 Statistik Penggunaan Sepeda ✨')

st.subheader('📝 Laporan Singkat')
st.write('Berikut adalah analisis tren penggunaan sepeda berdasarkan data yang tersedia.')

col1, col2, col3 = st.columns(3)

with col1:
    total_register = daily_register_df['registered'].sum()  
    st.metric("Total Berlangganan", value=total_register)

with col2:
    total_casual = daily_casual_df['casual'].sum()
    st.metric("Total Tidak Berlangganan", value=total_casual)

with col3:
    total_sepeda = daily_use_df['count'].sum()
    st.metric("Total Sepeda Terpakai", value=total_sepeda)



st.subheader("🚲 Tren Penggunaan Sepeda di Berbagai Musim")
 
fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    y="count", 
    x="season",
    data=daily_season_df.sort_values(by="count", ascending=False),
    palette="Blues_r"  
)

ax.set_title("📊 Jumlah Pengguna Sepeda Berdasarkan Musim", loc="center", fontsize=15)
ax.set_ylabel('Jumlah Pengguna')
ax.set_xlabel('Musim')
ax.tick_params(axis='x', labelsize=12)


for index, value in enumerate(daily_season_df['count']):
    ax.text(index, value, str(value), ha='center', va='bottom', fontsize=10, fontweight='bold')

st.pyplot(fig)


st.subheader("📅 Tren Penggunaan Sepeda pada Hari Kerja dan Akhir Pekan")

fig, ax = plt.subplots()

sns.lineplot(
    data=daily_weekday_df,
    x="weekday",
    y="count",
    color="mediumblue",  
    marker="o",
    ax=ax
)

ax.set_title("📈 Pola Penggunaan Sepeda Berdasarkan Hari", loc="center", fontsize=20)
plt.xlabel("Hari", fontsize=12)
ax.set_ylabel("Jumlah Penggunaan", fontsize=12)

st.pyplot(fig)

st.subheader("👥 Persentase Pengguna Berlangganan vs Tidak Berlangganan")

total_registered = days_df['registered'].sum()
total_causal = days_df['casual'].sum()

label = ['Berlangganan', 'Tidak Berlangganan']
ukuran = [total_registered, total_causal]
colors = ['#1F77B4', '#FF7F0E'] 
explode = (0.1, 0)

fig, ax = plt.subplots()
ax.pie(
    x=ukuran,
    labels=label,
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    startangle=140,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)

ax.set_title("📊 Distribusi Pengguna Berlangganan dan Tidak Berlangganan", fontsize=15)
st.pyplot(fig)