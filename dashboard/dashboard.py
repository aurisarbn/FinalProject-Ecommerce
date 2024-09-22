import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load the dataset
all_df = pd.read_csv("all_data.csv")

# Convert relevant columns to datetime
datetime_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date"
]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Calculate delivery time
all_df['delivery_time'] = (all_df['order_delivered_customer_date'] - all_df['order_purchase_timestamp']).dt.days

# Calculate late deliveries
all_df['late_delivery'] = all_df['order_delivered_customer_date'] > all_df['order_estimated_delivery_date']

# Start Streamlit app
st.sidebar.image("logo.png", use_column_width=True)

st.header('Dashboard Penjualan')

# Visualisasi metode pembayaran
st.subheader('Metode Pembayaran')
payment_counts = all_df['payment_type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette="Blues", ax=ax)
ax.set_title("Jumlah Transaksi per Metode Pembayaran", fontsize=12)
ax.set_xlabel("Metode Pembayaran", fontsize=10)
ax.set_ylabel("Jumlah Transaksi", fontsize=10)
plt.subplots_adjust(bottom=0.15)
st.pyplot(fig)

# Visualisasi rata-rata pengiriman per wilayah
st.subheader('Rata-rata Waktu Pengiriman per Wilayah')
average_delivery_time = all_df.groupby('customer_state')['delivery_time'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='customer_state', y='delivery_time', data=average_delivery_time, color='skyblue', ax=ax, width=0.5)
ax.set_title("Rata-rata Waktu Pengiriman per Wilayah", fontsize=12)
ax.set_xlabel("Wilayah", fontsize=10)
ax.set_ylabel("Waktu Pengiriman (hari)", fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.subplots_adjust(bottom=0.15)
st.pyplot(fig)

# Visualisasi rata-rata nilai pembayaran per wilayah
st.subheader('Rata-rata Nilai Pembayaran per Wilayah')
average_payment_value = all_df.groupby('customer_state')['payment_value'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='customer_state', y='payment_value', data=average_payment_value, color='lightgreen', ax=ax, width=0.5)
ax.set_title("Rata-rata Nilai Pembayaran per Wilayah", fontsize=12)
ax.set_xlabel("Wilayah", fontsize=10)
ax.set_ylabel("Nilai Pembayaran Rata-rata", fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.subplots_adjust(bottom=0.15)
st.pyplot(fig)

# Visualisasi skor ulasan
st.subheader('Skor Ulasan')
review_scores = all_df['review_score'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=review_scores.index, y=review_scores.values, palette="Blues", ax=ax)
ax.set_title("Jumlah Ulasan per Skor", fontsize=12)
ax.set_xlabel("Skor Ulasan", fontsize=10)
ax.set_ylabel("Jumlah Ulasan", fontsize=10)
plt.subplots_adjust(bottom=0.15)
st.pyplot(fig)

# Visualisasi pengiriman yang telat
st.subheader('Pengiriman yang Telat')
late_deliveries = all_df[all_df['late_delivery']]
late_counts = late_deliveries['customer_state'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=late_counts.index, y=late_counts.values, color='red', ax=ax, width=0.5)
ax.set_title("Jumlah Pengiriman yang Telat per Wilayah", fontsize=12)
ax.set_xlabel("Wilayah", fontsize=10)
ax.set_ylabel("Jumlah Pengiriman yang Telat", fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.subplots_adjust(bottom=0.15)
st.pyplot(fig)

st.caption('Copyright (c) Aurisa Rabina 2024')
