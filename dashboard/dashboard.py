import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Set style untuk seaborn
sns.set(style='whitegrid')

# Load dataset
csv_file_path = "dashboard/all_data.csv.gz"  # Ubah sesuai lokasi file
all_df = pd.read_csv(csv_file_path, compression='gzip')

# Convert columns to datetime format
datetime_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Menghitung waktu pengiriman dalam hari
all_df['delivery_time'] = (all_df['order_delivered_customer_date'] - all_df['order_purchase_timestamp']).dt.days

# Menghitung persentase pengiriman yang terlambat
all_df['late_delivery'] = all_df['order_delivered_customer_date'] > all_df['order_estimated_delivery_date']
late_delivery_percent = (all_df['late_delivery'].mean() * 100).round(2)

# Rata-rata waktu pengiriman
mean_delivery_time = all_df['delivery_time'].mean().round(2)

# Start Streamlit app
st.sidebar.image("dashboard/logo.png", use_column_width=True)
st.header('Geoanalysis - E-commerce')

# Visualisasi rata-rata waktu pengiriman per wilayah
st.subheader('Average Delivery Time by State')
average_delivery_time = all_df.groupby('customer_state')['delivery_time'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='customer_state', y='delivery_time', data=average_delivery_time, color='skyblue', ax=ax, width=0.6)
ax.set_title("Average Delivery Time by State", fontsize=12)
ax.set_xlabel("State", fontsize=10)
ax.set_ylabel("Average Delivery Time (days)", fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.tight_layout()
st.pyplot(fig)

# Visualisasi persentase pengiriman terlambat
st.subheader('Late Deliveries by State')
late_deliveries_by_state = all_df[all_df['late_delivery']].groupby('customer_state').size().reset_index(name='late_count')
late_deliveries_by_state['late_percent'] = (late_deliveries_by_state['late_count'] / 
                                            all_df['customer_state'].value_counts() * 100).round(2).reset_index(drop=True)

fig, ax = plt.subplots()
sns.barplot(x='customer_state', y='late_percent', data=late_deliveries_by_state, color='salmon', ax=ax, width=0.6)
ax.set_title("Late Delivery Percentage by State", fontsize=12)
ax.set_xlabel("State", fontsize=10)
ax.set_ylabel("Late Delivery Percentage (%)", fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.tight_layout()
st.pyplot(fig)

# Display metrics
st.metric("Average Delivery Time", f"{mean_delivery_time} days")
st.metric("Late Delivery Percentage", f"{late_delivery_percent}%")

st.caption('Analysis by Aurisa Rabina 2024')
