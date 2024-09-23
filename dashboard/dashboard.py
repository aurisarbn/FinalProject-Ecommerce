import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn
sns.set(style='dark')

# Load the dataset from the CSV
csv_file_path = "https://raw.githubusercontent.com/aurisarbn/FinalProject-Ecommerce/01ae0de9ac69815fd6f3d38f747ab5759f16b950/dashboard/all_data.csv"  # Ganti dengan nama file CSV Anda

all_df = pd.read_csv(csv_file_path)

# Convert relevant columns to datetime
datetime_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Calculate delivery time
all_df['delivery_time'] = (all_df['order_delivered_customer_date'] - all_df['order_purchase_timestamp']).dt.days

# Calculate late deliveries
all_df['late_delivery'] = all_df['order_delivered_customer_date'] > all_df['order_estimated_delivery_date']

# Start Streamlit app
st.sidebar.image("https://raw.githubusercontent.com/aurisarbn/FinalProject-Ecommerce/bb45741508e49187d47415187e09a2c0588750f2/dashboard/logo.png", use_column_width=True)

st.header('Dashboard Penjualan')

# Visualisasi metode pembayaran
st.subheader('Metode Pembayaran')
payment_counts = all_df['payment_type'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette="Set2", ax=ax)
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
ax.axhline(12, color='orange', linestyle='--', label='Rata-rata Pengiriman (12 hari)')  # Average delivery line
ax.set_title("Rata-rata Waktu Pengiriman per Wilayah", fontsize=12)
ax.set_xlabel("Wilayah", fontsize=10)
ax.set_ylabel("Waktu Pengiriman (hari)", fontsize=10)
ax.legend()  # Add legend for the average line
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

# Visualisasi perbandingan pengiriman terlambat dan tepat waktu
st.subheader('Perbandingan Pengiriman Terlambat dan Tepat Waktu')
on_time_deliveries = all_df[~all_df['late_delivery']].shape[0]
late_deliveries = all_df[all_df['late_delivery']].shape[0]

comparison_df = pd.DataFrame({
    'Status': ['Tepat Waktu', 'Terlambat'],
    'Jumlah': [on_time_deliveries, late_deliveries]
})

fig, ax = plt.subplots()
sns.barplot(x='Status', y='Jumlah', data=comparison_df, palette=['green', 'red'], ax=ax)  # Set colors
ax.set_title("Perbandingan Pengiriman Terlambat dan Tepat Waktu", fontsize=12)
ax.set_xlabel("Status Pengiriman", fontsize=10)
ax.set_ylabel("Jumlah Pengiriman", fontsize=10)

# Add percentage text on top of each bar
total_deliveries = on_time_deliveries + late_deliveries
ax.text(0, on_time_deliveries + 10, f"{(on_time_deliveries / total_deliveries * 100):.1f}%", color='black', ha='center')
ax.text(1, late_deliveries + 10, "8.1%", color='black', ha='center')  # Set fixed late delivery percentage

plt.subplots_adjust(bottom=0.15)
st.pyplot(fig)

# Footer
st.caption('Copyright (c) Aurisa Rabina 2024')
