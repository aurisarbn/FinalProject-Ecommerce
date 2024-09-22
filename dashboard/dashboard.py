import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set seaborn style
sns.set(style='dark')

# Load the dataset
csv_file_path = "dashboard/all_data.csv.gz"  # Ganti dengan path file CSV kamu
all_df = pd.read_csv(csv_file_path, compression='gzip')

# Convert relevant columns to datetime
datetime_columns = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date',
    'review_creation_date',
    'review_answer_timestamp'
]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column], errors='coerce')

# Calculate delivery time
all_df['delivery_time'] = (all_df['order_delivered_customer_date'] - all_df['order_purchase_timestamp']).dt.days

# Calculate late deliveries
all_df['late_delivery'] = all_df['order_delivered_customer_date'] > all_df['order_estimated_delivery_date']

# Start Streamlit app
st.sidebar.image("dashboard/logo.png", use_column_width=True)

st.header('Geoanalysis E-Commerce Dashboard')

# 1. Distribusi Pelanggan Berdasarkan Wilayah
st.subheader('Distribusi Pelanggan Berdasarkan Wilayah')
customer_distribution = all_df['customer_state'].value_counts().reset_index()
customer_distribution.columns = ['State', 'Number of Customers']
fig, ax = plt.subplots()
sns.barplot(x='State', y='Number of Customers', data=customer_distribution, ax=ax, palette='coolwarm')
ax.set_title('Distribusi Pelanggan Berdasarkan Wilayah', fontsize=12)
ax.set_xlabel('Wilayah', fontsize=10)
ax.set_ylabel('Jumlah Pelanggan', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.tight_layout()
st.pyplot(fig)

# 2. Rata-rata Nilai Pembayaran per Wilayah
st.subheader('Rata-rata Nilai Pembayaran per Wilayah')
average_payment_value = all_df.groupby('customer_state')['payment_value'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='customer_state', y='payment_value', data=average_payment_value, palette='viridis', ax=ax)
ax.set_title('Rata-rata Nilai Pembayaran per Wilayah', fontsize=12)
ax.set_xlabel('Wilayah', fontsize=10)
ax.set_ylabel('Nilai Pembayaran Rata-rata (Rp)', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.tight_layout()
st.pyplot(fig)

# 3. Rata-rata Waktu Pengiriman per Wilayah
st.subheader('Rata-rata Waktu Pengiriman per Wilayah')
average_delivery_time = all_df.groupby('customer_state')['delivery_time'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='customer_state', y='delivery_time', data=average_delivery_time, palette='Blues', ax=ax)
ax.set_title('Rata-rata Waktu Pengiriman per Wilayah', fontsize=12)
ax.set_xlabel('Wilayah', fontsize=10)
ax.set_ylabel('Waktu Pengiriman (hari)', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.tight_layout()
st.pyplot(fig)

# 4. Jumlah Pengiriman yang Telat per Wilayah
st.subheader('Jumlah Pengiriman yang Telat per Wilayah')
late_deliveries = all_df[all_df['late_delivery']]
late_counts = late_deliveries['customer_state'].value_counts().reset_index()
late_counts.columns = ['State', 'Late Deliveries']
fig, ax = plt.subplots()
sns.barplot(x='State', y='Late Deliveries', data=late_counts, palette='Reds', ax=ax)
ax.set_title('Jumlah Pengiriman yang Telat per Wilayah', fontsize=12)
ax.set_xlabel('Wilayah', fontsize=10)
ax.set_ylabel('Jumlah Pengiriman yang Telat', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=9)
plt.tight_layout()
st.pyplot(fig)

# Tambahkan analisis RFM
st.subheader('Analisis RFM')

# Recency: Number of days since the last purchase
latest_order_date = all_df['order_purchase_timestamp'].max()
rfm_recency = all_df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (latest_order_date - x.max()).days
}).reset_index()
rfm_recency.columns = ['customer_unique_id', 'recency']

# Frequency: Number of orders per customer
rfm_frequency = all_df.groupby('customer_unique_id').agg({
    'order_id': 'count'
}).reset_index()
rfm_frequency.columns = ['customer_unique_id', 'frequency']

# Monetary: Total value spent per customer
rfm_monetary = all_df.groupby('customer_unique_id').agg({
    'payment_value': 'sum'
}).reset_index()
rfm_monetary.columns = ['customer_unique_id', 'monetary']

# Merge the three RFM metrics into one DataFrame
rfm_df = rfm_recency.merge(rfm_frequency, on='customer_unique_id')
rfm_df = rfm_df.merge(rfm_monetary, on='customer_unique_id')

# Visualisasi RFM
# 1. Distribusi Recency
st.subheader('Distribusi Recency')
fig, ax = plt.subplots()
sns.histplot(rfm_df['recency'], bins=20, kde=False, color='skyblue', ax=ax)
ax.set_title('Distribusi Recency (Jumlah Hari Sejak Pembelian Terakhir)', fontsize=12)
ax.set_xlabel('Recency (Hari)', fontsize=10)
ax.set_ylabel('Jumlah Pelanggan', fontsize=10)
plt.tight_layout()
st.pyplot(fig)

# 2. Distribusi Frequency
st.subheader('Distribusi Frequency')
fig, ax = plt.subplots()
sns.histplot(rfm_df['frequency'], bins=20, kde=False, color='green', ax=ax)
ax.set_title('Distribusi Frequency (Jumlah Transaksi per Pelanggan)', fontsize=12)
ax.set_xlabel('Frequency', fontsize=10)
ax.set_ylabel('Jumlah Pelanggan', fontsize=10)
plt.tight_layout()
st.pyplot(fig)

# 3. Distribusi Monetary
st.subheader('Distribusi Monetary')
fig, ax = plt.subplots()
sns.histplot(rfm_df['monetary'], bins=20, kde=False, color='orange', ax=ax)
ax.set_title('Distribusi Monetary (Total Nilai Transaksi per Pelanggan)', fontsize=12)
ax.set_xlabel('Monetary (Rp)', fontsize=10)
ax.set_ylabel('Jumlah Pelanggan', fontsize=10)
plt.tight_layout()
st.pyplot(fig)

# Footer
st.caption('Copyright (c) Aurisa Rabina 2024')
