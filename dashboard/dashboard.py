import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import millify

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

df = pd.read_csv('hour.csv')

st.title('🚲 Bike Sharing Dashboard 2011 dan 2012 🚲')

# Metric Section
metric_style = """
    <style>
    .stMetric{
        background-color: gainsboro;
        border-radius: 30px;
        padding: 20px;
    }
    .stMetric p {
        font-size: 15px;
        font-weight: bold;
    }
    </style>
"""
st.markdown(metric_style,unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Penyewaan Sepeda 2011-2012", value= millify.millify(df['cnt'].sum(),precision=2))

with col2:
    st.metric(label="Jumlah Penyewaan Sepeda oleh *casual user*", value=millify.millify(df['casual'].sum(),precision=2))
    
with col3:
    st.metric(label="Jumlah Penyewaan Sepeda oleh *registered user*", value=millify.millify(df['registered'].sum(),precision=2))

# Pertanyaan Bisnis 1
# Total jumlah penyewaan sepeda per musim untuk tahun 2011 dan 2012
total_counts = df.groupby(['season', 'yr'])['cnt'].sum().unstack()
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
year_mapping = {0: 2011, 1: 2012}
total_counts = total_counts.rename(index=season_mapping, columns=year_mapping)

# Plot Total Jumlah Penyewaan Sepeda per Musim 2011 vs 2012
fig, ax = plt.subplots()
x = range(len(total_counts.index))
ax.bar([pos - 0.2 for pos in x], total_counts[2011], width=0.4, label='2011', color='skyblue')
ax.bar([pos + 0.2 for pos in x], total_counts[2012], width=0.4, label='2012', color='salmon')
ax.set_title("Total Penyewaan Sepeda per Musim (2011 vs 2012)", size=15)
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xlabel("Musim")
ax.set_xticks(x)
ax.set_xticklabels(total_counts.index)
ax.legend(title="Tahun")

with st.container():
    st.header('Total Jumlah Penyewaan Sepeda per Musim')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Tahun 2011')
        st.bar_chart(total_counts[2011])
    with col2:
        st.subheader('Tahun 2012')
        st.bar_chart(total_counts[2012])
    with col3:
        st.subheader('Perbandingan Jumlah Penyewaan Sepeda Tahun 2011 dan 2012')
        st.pyplot(fig)
        
    st.info('''
            **Insight**: \n
            - Terjadi **peningkatan jumlah penyewaan** sepeda dari tahun 2011 ke 2012 **di setiap musimnya**. \n
            - Tingkat penyewaan sepeda **tertinggi selalu terjadi di musim** `Fall` tiap tahunnya.
            '''
            )

# Pertanyaan Bisnis 2
with st.container():
    st.header('Total Jumlah Penyewaan Sepeda *Weekdays* vs *Holiday* pada Tahun 2011 dan 2012')
    # Total jumlah penyewaan sepeda Weekend dan Weekdays untuk tahun 2011 dan 2012
    total_counts_weekday_weekend = df.groupby(['workingday', 'yr'])['cnt'].sum().unstack()
    workingday_mapping = {0: 'Weekend', 1: 'Weekday'}
    total_counts_weekday_weekend = total_counts_weekday_weekend.rename(index=workingday_mapping, columns=year_mapping)
    
    # Persentase total jumlah penyewaan sepeda weekend dan weekday di tahun 2011
    total_counts_2011_weekday_weekend = total_counts_weekday_weekend[2011].sum()
    percentage_weekday_weekend_2011 = total_counts_weekday_weekend[2011] / total_counts_2011_weekday_weekend * 100

    # Persentase total jumlah penyewaan sepeda weekend dan weekday di tahun 2012
    total_counts_2012_weekday_weekend = total_counts_weekday_weekend[2012].sum()
    percentage_weekday_weekend_2012 = total_counts_weekday_weekend[2012] / total_counts_2012_weekday_weekend * 100

    # Plot Diagram Pie
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.pie(percentage_weekday_weekend_2011, labels=total_counts_weekday_weekend.index, autopct='%1.2f%%', startangle=140, colors=['lightcoral', 'skyblue'])
    ax1.set_title("Persentase Penyewaan Sepeda Weekend vs Weekday\n di Tahun 2011")
    ax2.pie(percentage_weekday_weekend_2012, labels=total_counts_weekday_weekend.index, autopct='%1.2f%%', startangle=140, colors=['lightcoral', 'skyblue'])
    ax2.set_title("Persentase Penyewaan Sepeda Weekend vs Weekday\n di Tahun 2012")
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.dataframe(total_counts_weekday_weekend, width=450)
    with col2:
        st.pyplot(fig)
        
    st.info('''
            **Insight**: \n
            Tren penyewaan sepeda pada **hari kerja (weekdays) jauh lebih tinggi daripada saat hari libur**, baik di tahun 2011 maupun di tahun 2012.
            '''
            )
    
# Pertanyaan Bisnis 3
with st.container():
    st.header('Total Jumlah Penyewaan Sepeda pada Hari Kerja (Weekdays) dengan Cuaca Baik vs Cuaca Buruk pada Tahun 2011 dan 2012')
    # Buat Kategori 1 dan 2 sebagai Cuaca Baik, dan Kategori 3 dan 4 sebagai Cuaca Buruk
    hour_dataset_new = df.copy()
    hour_dataset_new['weathersit'] = hour_dataset_new['weathersit'].replace({1: 0, 2: 0, 3: 1, 4: 1})
    weathersit_mapping = {0: 'Good Weather', 1: 'Bad Weather'}
    
    # Hitung total jumlah penyewaan sepeda untuk cuaca baik dan cuaca buruk pada hari kerja untuk tahun 2011 dan 2012
    total_counts_by_weather = hour_dataset_new.where(hour_dataset_new['workingday'] == 1).groupby(['weathersit', 'yr'])['cnt'].sum().unstack()
    total_counts_by_weather = total_counts_by_weather.rename(index=weathersit_mapping, columns=year_mapping)

    x = range(len(total_counts_by_weather.index))

    fig1, ax1 = plt.subplots()
    ax1.bar([pos - 0.2 for pos in x], total_counts_by_weather[2011], width=0.4, label='2011', color='skyblue')
    ax1.bar([pos + 0.2 for pos in x], total_counts_by_weather[2012], width=0.4, label='2012', color='lightcoral')

    ax1.set_title("Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca\nTahun 2011 dan 2012 Selama Hari Kerja", size=13)
    ax1.set_ylabel("Jumlah Penyewaan")
    ax1.set_xlabel("Kondisi Cuaca")
    ax1.set_xticks(x)
    ax1.set_xticklabels(total_counts_by_weather.index)
    ax1.legend(title="Tahun")
    
    # Persentase total jumlah penyewaan sepeda weekend dan weekday di tahun 2011
    total_counts_by_weather_2011 = total_counts_by_weather[2011].sum()
    percentage_weather_2011 = total_counts_by_weather[2011] / total_counts_by_weather_2011 * 100

    # Persentase total jumlah penyewaan sepeda weekend dan weekday di tahun 2012
    total_counts_by_weather_2012 = total_counts_by_weather[2012].sum()
    percentage_weather_2012 = total_counts_by_weather[2012] / total_counts_by_weather_2012 * 100

    # Plot Diagram Pie
    fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 6))
    ax2.pie(percentage_weather_2011, labels=total_counts_by_weather.index, autopct='%1.2f%%', startangle=140, colors=['lightcoral', 'skyblue'])
    ax2.set_title("Persentase Penyewaan Sepeda\n Cuaca Baik vs Cuaca Buruk di Tahun 2011")
    ax3.pie(percentage_weather_2012, labels=total_counts_by_weather.index, autopct='%1.2f%%', startangle=140, colors=['lightcoral', 'skyblue'])
    ax3.set_title("Persentase Penyewaan Sepeda\n Cuaca Baik vs Cuaca Buruk di Tahun 2012")
    
    col1, col2 = st.columns([0.4,0.6])
    with col1:
        st.pyplot(fig1)
    with col2:
        st.pyplot(fig2)
        
    st.info('''
            **Insight**: \n
            **Cuaca buruk pada hari kerja (weekdays) sangat berdampak pada tingkat penyewaan sepeda**. Dapat dilihat bahwa jumlah penyewaan sepeda, baik pada tahun 2011 maupun 2012, memiliki selisih yang sangat jauh berbeda antara saat **Cuaca Baik** dan **Cuaca Buruk** pada hari kerja.
            '''
            )
    
# Analisis Lanjutan
with st.container():
    st.header('*Clustering* dengan Teknik Binning')
    st.write('Pada bagian ini, teknik *binning* akan digunakan untuk melakukan segmentasi pada dataset berdasarkan data pada kolom `cnt` ke dalam beberapa kategori, yaitu `Rendah`, `Menengah`, dan `Tinggi`.')
    
    # Informasi total jumlah penywaaan sepeda tiap jam
    counts = df['cnt'].describe()
    # Menentukan batas untuk pengelompokan
    cnt_bins = [0, counts['25%'], counts['75%'], counts['max']] 

    # Menentukan label untuk setiap kelompok
    cnt_labels = ['Rendah', 'Menengah', 'Tinggi']

    # Binning berdasarkan jumlah penyewaan (cnt) untuk mengelompokkan menjadi Rendah, Menengah, Tinggi
    df['Tingkat Penyewaan'] = pd.cut(df['cnt'], bins=cnt_bins, labels=cnt_labels)
    
    binned_df = df[['dteday','hr','cnt', 'Tingkat Penyewaan']]
    # Hitung jumlah untuk setiap kategori Tingkat Penyewaan
    category_counts = df['Tingkat Penyewaan'].value_counts()

    # Plot Diagram Pie
    plt.figure(figsize=(8, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.2f%%', startangle=140, colors=['lightcoral', 'skyblue', 'lightgreen'])
    plt.title('Persentase Penyewaan Sepeda berdasarkan Kategori')
    plt.axis('equal')
    
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.subheader('Dataset Hasil Binning')
        st.dataframe(binned_df, width=500, height=600)
    with col2:
        st.subheader('Presentase data antara Tingkat Penyewaan `Rendah`, `Menengah`, dan `Tinggi`')
        st.pyplot(plt)
    
# Footer Section
st.subheader('Dataset Overview')
st.dataframe(df)
st.warning('''
**Dataset Source**: \n
*Dataset*: [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data) \n
*Credit to*: [Lakshmipathi N](https://www.kaggle.com/lakshmi25npathi)
''')

footer="""<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: black;
    color: white;
    text-align: center;
    padding-top: 10px;
}
</style>
<div class="footer">
<p>&copy 2024 Christian Herdiyanto Prasetia. All rights reserved.</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)