import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
sns.set(style='dark')

#persiapan data
df = pd.read_csv("day.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

df['season'] = df['season'].replace([1,2,3,4],['Spring','Summer','Fall','Winter'])
df['weathersit'] = df['weathersit'].replace([1,2,3,4],['Clear','Mist','Light Rain','Heavy Rain'])

min_date = df['dteday'].min()
max_date = df['dteday'].max()

#header
st.header("Bike Sharing 2011-2012 Data Dashboard")
#sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png",width=200)
    st.write("Halo, selamat datang di Dashboard Visualisasi Data Peminjaman Sepeda PT. XXX! Silahkan pilih rentang waktu untuk menunjukan hasil visualisasi")
    start,end = st.date_input(
        label = 'Pilih Rentang Waktu', min_value = min_date, max_value = max_date, value=[min_date,max_date]
    )
main_df = df[(df['dteday'] >= str(start)) & (df['dteday'] <= str(end))]

st.subheader("Pergerakan Jumlah Peminjam Sepeda")
fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(x="dteday",y="cnt",data=main_df,label="Total Users")
sns.lineplot(x="dteday",y="registered",data=main_df,label="Registered Users")
sns.lineplot(x="dteday",y="casual",data=main_df,label="Casual Users")
plt.title("Fluktuasi Peminjaman Sepeda ("+str(start)+" sampai "+str(end)+")")
plt.xlabel("Tanggal")
plt.legend()
st.pyplot(fig)

st.subheader("Penyewa Sepeda dalam Angka")
col1,col2 = st.columns(2)
with col1:
    st.metric("Total renters", value=main_df["cnt"].sum())
    st.metric("Number registered renters", value=main_df["registered"].sum())
    st.metric("Number casual renters", value=main_df["casual"].sum())
with col2:
    count_data = [['Registered User',main_df["registered"].sum()],['Casual User',main_df["casual"].sum()]]
    df_count = pd.DataFrame(count_data,columns=['Type','Count'])

    fig, ax = plt.subplots(figsize=(4, 4))
    plt.pie(df_count["Count"],labels=df_count["Type"],autopct='%1.0f%%',explode=[0.1,0])
    plt.title("Proposi Jenis Peminjam Sepeda")
    st.pyplot(fig)

col1,col2,col3 = st.columns(3)
with col1:
    st.metric("Average Renters Through Period",value=main_df["cnt"].mean())
with col2:
    st.metric("Highest Renters Through Period",value=main_df["cnt"].max())
with col3:
    st.metric("Lowest Renters Through Period",value=main_df["cnt"].min())

fig, ax = plt.subplots(figsize=(16, 6))
st.subheader("Faktor Lingkungan pada Peminjaman Sepeda")
sns.lineplot(x="dteday",y="temp",data=main_df,label="Temperatur Ternormalisasi")
sns.lineplot(x="dteday",y="hum",data=main_df,label="Kelembapan Ternormalisasi")
sns.lineplot(x="dteday",y="windspeed",data=main_df,label="Kecepatan Angin Ternormalisasi")
plt.title("Fluktuasi Faktor Cuaca Sepeda ("+str(start)+" sampai "+str(end)+")")
plt.xlabel("Tanggal")
plt.legend()
st.pyplot(fig)

col1,col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.countplot(x='weathersit',data=main_df)
    plt.xlabel("Situasi cuaca")
    plt.ylabel("Jumlah hari")
    plt.title("Jumlah hari dengan situasi cuaca yang berbeda")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.histplot(x='season',data=main_df)
    plt.xlabel("Musim")
    plt.ylabel("Jumlah hari")
    plt.title("Jumlah hari dengan temperatur yang berbeda")
    st.pyplot(fig)