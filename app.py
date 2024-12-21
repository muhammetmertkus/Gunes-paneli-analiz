# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64

from solar_panel_analysis import (
    calculate_declination,
    calculate_annual_optimum_angle,
    calculate_average_daily_irradiance_hourly,
    calculate_panel_temperature,
    adjust_parameters,
    calculate_max_power,
    generate_hourly_irradiance,
    calculate_panel_voltage_and_current
)





from building_energy_analysis import calculate_building_energy

# Finansal Hesaplamalar Modülünü İçe Aktarma
from finansal_hesaplamalar import FinansalAnalizler

# "Program Nasıl Çalışır" Modülünü İçe Aktarma
from calisir import program_nasil_calisir

# ==========================================
# Sabit Veriler
# ==========================================
months = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]
days_of_year = [15, 45, 75, 105, 135, 165, 195, 225, 255, 285, 315, 345]
global_radiation_default = [
    1.74, 2.33, 3.74, 4.83, 6.03, 6.38,
    6.31, 5.68, 4.67, 3.25, 1.98, 1.47
]
daylight_hours_default = [
    3.23, 4.74, 4.37, 6.18, 8.78, 10.16,
    10.75, 10.10, 8.85, 6.25, 4.73, 3.37
]
average_temperatures_default = [
    0.0,    # Ocak
    1.6,    # Şubat
    5.2,    # Mart
    9.9,    # Nisan
    14.9,   # Mayıs
    18.9,   # Haziran
    21.9,   # Temmuz
    22.0,   # Ağustos
    17.5,   # Eylül
    12.1,   # Ekim
    6.0,    # Kasım
    2.0     # Aralık
]

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# ==========================================
# Streamlit Başlığı ve Açıklama
# ==========================================
st.set_page_config(
    page_title="Güneş Paneli ve Bina Enerji Analizi",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Bu uygulama Güneş Paneli ve Bina Enerji Tüketimi Analizi için geliştirilmiştir."
    }
)

# Ana başlık ve açıklama bölümü
st.markdown("""
    <div style="background: linear-gradient(to right, #1a5276, #2980b9); padding: 30px; border-radius: 15px; margin-bottom: 30px">
        <h1 style="color: white; text-align: center; font-size: 2.5em; margin-bottom: 15px">
            🌟 Güneş Paneli ve Bina Enerji Analizi Sistemi 🌟
        </h1>
        <p style="color: white; text-align: center; font-size: 1.2em; margin-bottom: 20px">
            Yenilenebilir Enerji ve Sürdürülebilir Çözümler
        </p>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px">
            <p style="color: white; text-align: center; margin: 0">
                Bu program, güneş enerjisi sistemlerinin optimizasyonu ve bina enerji tüketiminin analizi için 
                geliştirilmiş kapsamlı bir araçtır. Güneş paneli performansı, enerji üretimi ve finansal analizler 
                dahil olmak üzere detaylı hesaplamalar sunar.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Profil resmi dosya yolu
image_path = r"C:\Users\mert1\OneDrive\Masaüstü\dist\images\muhammet_mert_kus.jpg"

# Resmi Base64 formatına çevirme fonksiyonu
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Resmi Base64 formatına çevir
base64_image = get_base64_image(image_path)

# Geliştirici bilgileri
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; padding: 20px; 
         background-color: #f8f9fa; border-radius: 15px; margin-bottom: 30px">
        <img src="data:image/jpeg;base64,{base64_image}" alt="Profile Picture" 
             style="border-radius: 50%; width: 120px; height: 120px; margin-right: 20px; border: 3px solid #4CAF50">
        <div style="text-align: left;">
            <h2 style="font-family: Arial, sans-serif; color: #4CAF50; margin: 0;">Muhammet Mert Kuş</h2>
            <p style="font-size: 18px; color: #555; margin: 5px 0;">Enerji Sistemleri Mühendisi</p>
            <p style="font-size: 16px; color: #666; margin: 5px 0;">
                🎓 Eskişehir Osmangazi Üniversitesi
                <br>
                📧 muhammetmertkus@gmail.com
            </p>
            <div style="margin-top: 10px;">
                <span style="background-color: #e8f5e9; padding: 5px 10px; border-radius: 15px; margin-right: 10px;">
                    🌞 Güneş Enerjisi
                </span>
                <span style="background-color: #e8f5e9; padding: 5px 10px; border-radius: 15px; margin-right: 10px;">
                    ⚡ Enerji Verimliliği
                </span>
                <span style="background-color: #e8f5e9; padding: 5px 10px; border-radius: 15px;">
                    🏢 Bina Enerji Sistemleri
                </span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# Sidebar ile Kullanıcı Girdileri
# ==========================================
st.sidebar.header("Girdi Parametreleri")

# Güneş Paneli Analizi Parametreleri
st.sidebar.subheader("Güneş Paneli Analizi")
latitude = st.sidebar.number_input("Enlem (°)", value=39.72, step=0.01, format="%.2f")
T_ref = st.sidebar.number_input("Referans Sıcaklık (°C)", value=25, step=1)
G_ref = st.sidebar.number_input("Referans Işınım (W/m²)", value=1000, step=100)
n_parallel = st.sidebar.number_input("Paralel Bağlı Modül Sayısı", value=88, step=1)
n_series = st.sidebar.number_input("Seri Bağlı Modül Sayısı", value=7, step=1)

# Panel Parametreleri
st.sidebar.subheader("Panel Parametreleri (STC)")
Isc_ref = st.sidebar.number_input("Kısa Devre Akımı (Isc_ref) [A]", value=6.09, step=0.01)
Voc_ref = st.sidebar.number_input("Açık Devre Gerilimi (Voc_ref) [V]", value=85.3, step=0.1)
Vmp_ref = st.sidebar.number_input("Maksimum Güç Noktasındaki Gerilim (Vmp_ref) [V]", value=72.9, step=0.1)
Imp_ref = st.sidebar.number_input("Maksimum Güç Noktasındaki Akım (Imp_ref) [A]", value=5.69, step=0.01)
Ki = st.sidebar.number_input("Akım Sıcaklık Katsayısı (Ki) [A/°C]", value=0.003, step=0.001)
Kv = st.sidebar.number_input("Gerilim Sıcaklık Katsayısı (Kv) [V/°C]", value=-0.229, step=0.001)

# Bina Enerji Tüketimi Analizi Parametreleri
st.sidebar.subheader("Bina Enerji Tüketimi Analizi")
power_factor = st.sidebar.number_input("Güç Faktörü", value=0.9, step=0.01, min_value=0.0, max_value=1.0)

# Interaktif Ay Seçimi
st.sidebar.subheader("Analiz İçin Ayları Seçin")
selected_months = st.sidebar.multiselect(
    'Analiz Etmek İstediğiniz Ayları Seçin',
    options=months,
    default=months  # Varsayılan olarak tüm ayları seçili tut
)

# ==========================================
# Aylara Göre Gün Işıklama Süreleri (saat) Girdileri
# ==========================================
st.sidebar.subheader("Aylara Göre Gün Işıklama Süreleri (saat)")
daylight_hours = []
for i, month in enumerate(months):
    dh = st.sidebar.number_input(
        f"{month}: ",
        min_value=0.0,
        max_value=24.0,
        value=daylight_hours_default[i],
        step=0.1,
        format="%.2f"
    )
    daylight_hours.append(dh)

# ==========================================
# Aylara Göre Ortalama Hava Sıcaklıkları (°C) Girdileri
# ==========================================
st.sidebar.subheader("Aylara Göre Ortalama Hava Sıcaklıkları (°C)")
average_temperatures = []
for i, month in enumerate(months):
    at = st.sidebar.number_input(
        f"{month}: ",
        min_value=-50.0,
        max_value=50.0,
        value=average_temperatures_default[i],
        step=0.1,
        format="%.2f"
    )
    average_temperatures.append(at)

# ==========================================
# Aylara Göre Global Işınım (W/m²) Girdileri
# ==========================================
st.sidebar.subheader("Aylara Göre Global Işınım (W/m²)")
global_radiation = []
for i, month in enumerate(months):
    gr = st.sidebar.number_input(
        f"{month}: ",
        min_value=0.0,
        max_value=10000.0,
        value=global_radiation_default[i],
        step=0.1,
        format="%.2f"
    )
    global_radiation.append(gr)

# ==========================================
# Güneş Paneli Analizi ve Bina Enerji Tüketimi Analizi
# ==========================================
# Panel Parametreleri
panel_parameters = {
    'Voc_ref': Voc_ref,
    'Isc_ref': Isc_ref,
    'Vmp_ref': Vmp_ref,
    'Imp_ref': Imp_ref,
    'Ki': Ki,
    'Kv': Kv,
    'T_ref': T_ref,
    'G_ref': G_ref,
    'parallel_strings': n_parallel,
    'series_modules': n_series
}

# Hesaplamalar
yearly_optimum_angle = calculate_annual_optimum_angle(latitude)

solar_data = {
    'Ay': [],
    'Gun Sayisi (J)': [],
    'Gunes Sapma Acisi (°)': [],
    'Optimum Panel Acisi (°)': [],
    'Ortalama Gunluk Isinim (W/m²)': [],
    'Ortalama Hava Sicakligi (°C)': [],
    'Panel Sicakligi (°C)': []
}

panel_data = {
    'Ay': [],
    'Toplam Gerilim (V)': [],
    'Toplam Akım (A)': [],
    'Maksimum Güç (W)': []
}

for i in range(len(months)):
    month = months[i]
    if month not in selected_months:
        continue  # Sadece seçili aylarda hesaplama yap
    day = days_of_year[i]
    G_radiation = global_radiation[i]
    daylight = daylight_hours[i]
    Ta = average_temperatures[i]

    # Saatlik ışınım verilerini oluştur
    hourly_irradiance = generate_hourly_irradiance(daylight, G_radiation)

    # Ortalama günlük ışınımı hesapla
    Gg = calculate_average_daily_irradiance_hourly(hourly_irradiance)

    # Güneş sapma açısı
    declination = calculate_declination(day)

    # Optimum panel açısı
    optimum_angle = latitude - declination

    # Panel sıcaklığı
    Tc = calculate_panel_temperature(Gg, Ta)

    # Sıcaklık farkı
    delta_T = Ta - T_ref

    # Gerilim ve akım değerlerini sıcaklığa göre ayarla
    Vmp, Imp = adjust_parameters(panel_parameters['Vmp_ref'], panel_parameters['Imp_ref'], panel_parameters['Kv'], panel_parameters['Ki'], delta_T)
    Voc, Isc = adjust_parameters(panel_parameters['Voc_ref'], panel_parameters['Isc_ref'], panel_parameters['Kv'], panel_parameters['Ki'], delta_T)

    # Panel verilerini hazırlama
    panel_info = {
        'Voc': Voc,
        'Isc': Isc,
        'Vmp': Vmp,
        'Imp': Imp,
        'parallel_strings': panel_parameters['parallel_strings'],
        'series_modules': panel_parameters['series_modules']
    }

    # Hesaplama
    V_total, I_total = calculate_panel_voltage_and_current(
        panel_data=panel_info,
        irradiance=Gg,      # Ortalama günlük ışınım (W/m²)
        temperature=Tc      # Panel sıcaklığı (°C)
    )

    # Maksimum güç
    P_total = calculate_max_power(V_total, I_total)

    # Solar Data'ya ekle
    solar_data['Ay'].append(month)
    solar_data['Gun Sayisi (J)'].append(day)
    solar_data['Gunes Sapma Acisi (°)'].append(round(declination, 2))
    solar_data['Optimum Panel Acisi (°)'].append(round(optimum_angle, 2))
    solar_data['Ortalama Gunluk Isinim (W/m²)'].append(round(Gg, 2))
    solar_data['Ortalama Hava Sicakligi (°C)'].append(Ta)
    solar_data['Panel Sicakligi (°C)'].append(round(Tc, 2))

    # Panel Data'ya ekle
    panel_data['Ay'].append(month)
    panel_data['Toplam Gerilim (V)'].append(round(V_total, 2))
    panel_data['Toplam Akım (A)'].append(round(I_total, 2))
    panel_data['Maksimum Güç (W)'].append(round(P_total, 2))

# DataFrame oluştur
df_solar = pd.DataFrame(solar_data)
df_panel = pd.DataFrame(panel_data)

# Yıllık optimum panel açısı için ayrı DataFrame
df_yearly = pd.DataFrame({
    'Yıllık Optimum Panel Açısı (°)': [round(yearly_optimum_angle, 2)]
})

# ==========================================
# Bina Enerji Tüketimi Analizi
# ==========================================
# Veri Tanımlamaları
data_with_counts = {
    "Bina Tipi": [
        "Fakülteler",
        "Kültürel ve Sosyal Alanlar",
        "Sağlık Tesisleri",
        "Araştırma ve Uygulama Merkezleri",
        "Spor Alanları",
        "Yemek ve Konaklama",
        "Park ve Açık Alanlar",
        "Helikopter Pisti"
    ],
    "Adet": [9, 10, 3, 7, 4, 2, 2, 1],
    "Yıllık Ortalama Enerji (kWh)": [400.0, 395.0, 385.0, 335.0, 260.0, 150.0, 30, 7.5]
}

# Hesaplamalar
results_with_counts_df = calculate_building_energy(data_with_counts, power_factor=power_factor)

# ==========================================
# Tabs
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Güneş Paneli Analizi",
    "Bina Enerji Tüketimi Analizi",
    "Finansal Hesaplamalar",
    "Tablolar ve Veri İndirme",
    "Program Nasıl Çalışır"
    
])

# ==========================================
# Güneş Paneli Analizi Sekmesi
# ==========================================
with tab1:
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px'>
        <h2 style='text-align: center; color: #1f77b4; margin-bottom: 10px'>🌞 Güneş Paneli Analizi Grafikleri</h2>
        <p style='text-align: center'>Aşağıdaki grafikler güneş paneli sisteminin detaylı performans analizini göstermektedir.</p>
    </div>
    """, unsafe_allow_html=True)

    # Aylara Göre Güneş Sapma Açısı ve Optimum Panel Açısı
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_solar['Ay'],
        y=df_solar['Gunes Sapma Acisi (°)'],
        mode='lines+markers',
        name='Güneş Sapma Açısı (°)',
        marker=dict(symbol='circle', size=8, color='#1f77b4'),
        line=dict(width=3)
    ))
    fig1.add_trace(go.Scatter(
        x=df_solar['Ay'],
        y=df_solar['Optimum Panel Acisi (°)'],
        mode='lines+markers',
        name='Optimum Panel Açısı (°)',
        marker=dict(symbol='square', size=8, color='#2ca02c'),
        line=dict(width=3)
    ))
    fig1.add_trace(go.Scatter(
        x=df_solar['Ay'],
        y=[yearly_optimum_angle]*len(df_solar),
        mode='lines',
        name=f'Yıllık Optimum Açı ({yearly_optimum_angle}°)',
        line=dict(color='#d62728', dash='dash', width=2)
    ))
    fig1.update_layout(
        title=dict(
            text='Aylara Göre Güneş Sapma ve Optimum Panel Açıları',
            font=dict(size=20)
        ),
        xaxis_title='Ay',
        yaxis_title='Açı (°)',
        legend=dict(x=0, y=1.2, orientation='h'),
        xaxis=dict(tickangle=45),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14)
    )
    fig1.update_xaxes(gridcolor='#f0f0f0')
    fig1.update_yaxes(gridcolor='#f0f0f0')

    # Ortalama Günlük Işınım
    fig3 = px.bar(
        df_solar,
        x='Ay',
        y='Ortalama Gunluk Isinim (W/m²)',
        title='Aylara Göre Ortalama Günlük Işınım',
        labels={'Ortalama Gunluk Isinim (W/m²)': 'Işınım (W/m²)'},
        color='Ortalama Gunluk Isinim (W/m²)',
        color_continuous_scale='Viridis',
        template='plotly_white'
    )
    fig3.update_layout(
        title_font_size=20,
        xaxis_tickangle=-45,
        font=dict(size=14)
    )

    # Ortalama Günlük Işınım ve Gün Işıklama Süreleri Grafiği
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=df_solar['Ay'],
        y=df_solar['Ortalama Gunluk Isinim (W/m²)'],
        name='Ortalama Gunluk Isinim (W/m²)',
        marker_color='#1f77b4',
        opacity=0.7
    ))
    fig4.add_trace(go.Scatter(
        x=df_solar['Ay'],
        y=daylight_hours,
        name='Gün Işıklama Süreleri (saat)',
        mode='lines+markers',
        marker=dict(color='#ff7f0e', size=10),
        line=dict(width=3)
    ))
    fig4.update_layout(
        title=dict(
            text='Aylara Göre Ortalama Günlük Işınım ve Gün Işıklama Süreleri',
            font=dict(size=20)
        ),
        xaxis_title='Ay',
        yaxis_title='Değerler',
        legend=dict(x=0, y=1.2, orientation='h'),
        xaxis=dict(tickangle=45),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14)
    )
    fig4.update_xaxes(gridcolor='#f0f0f0')
    fig4.update_yaxes(gridcolor='#f0f0f0')

    # Panel Sıcaklığı
    fig5 = px.line(
        df_solar,
        x='Ay',
        y='Panel Sicakligi (°C)',
        title='Aylara Gore Panel Sicakligi',
        labels={'Panel Sicakligi (°C)': 'Panel Sicakligi (°C)'},
        markers=True,
        line_shape='linear',
        template='plotly_white'
    )
    fig5.update_traces(line=dict(color='#e377c2', width=3), marker=dict(size=10))
    fig5.update_layout(
        title_font_size=20,
        xaxis_tickangle=-45,
        font=dict(size=14)
    )

    # Toplam Sistem Gerilimi ve Akımı
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=df_panel['Ay'],
        y=df_panel['Toplam Gerilim (V)'],
        mode='lines+markers',
        name='Toplam Gerilim (V)',
        marker=dict(symbol='square', size=10, color='#2ca02c'),
        line=dict(width=3)
    ))
    fig6.add_trace(go.Scatter(
        x=df_panel['Ay'],
        y=df_panel['Toplam Akım (A)'],
        mode='lines+markers',
        name='Toplam Akım (A)',
        marker=dict(symbol='diamond', size=10, color='#d62728'),
        line=dict(width=3)
    ))
    fig6.update_layout(
        title=dict(
            text='Aylara Göre Toplam Sistem Gerilimi ve Akımı',
            font=dict(size=20)
        ),
        xaxis_title='Ay',
        yaxis_title='Değerler',
        legend=dict(x=0, y=1.2, orientation='h'),
        xaxis=dict(tickangle=45),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14)
    )
    fig6.update_xaxes(gridcolor='#f0f0f0')
    fig6.update_yaxes(gridcolor='#f0f0f0')

    # Maksimum Güç
    fig7 = px.line(
        df_panel,
        x='Ay',
        y='Maksimum Güç (W)',
        title='Aylara Göre Maksimum Güç',
        labels={'Maksimum Güç (W)': 'Maksimum Güç (W)'},
        markers=True,
        line_shape='linear',
        template='plotly_white'
    )
    fig7.update_traces(line=dict(color='#17becf', width=3), marker=dict(size=10))
    fig7.update_layout(
        title_font_size=20,
        xaxis_tickangle=-45,
        font=dict(size=14)
    )

    # Görsellerin Yerleşimi
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.plotly_chart(fig7, use_container_width=True)

# ==========================================
# Bina Enerji Tüketimi Analizi Sekmesi
# ==========================================
with tab2:
    # Başlık ve açıklama
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px'>
        <h2 style='text-align: center; color: #1f77b4; margin-bottom: 10px'>🏢 Bina Enerji Tüketimi Analizi</h2>
        <p style='text-align: center'>Bu bölümde farklı bina tiplerinin enerji tüketim analizlerini inceleyebilirsiniz.</p>
    </div>
    """, unsafe_allow_html=True)

    # Toplam Günlük Enerji Tüketimi
    st.markdown("""
    ### 📊 Toplam Günlük Enerji Tüketimi
    Bu grafik, her bir bina tipinin günlük toplam enerji tüketimini göstermektedir. 
    Renk skalası, tüketim miktarına göre değişmektedir.
    """)
    
    fig8 = px.bar(
        results_with_counts_df,
        x='Bina Tipi',
        y='Toplam Günlük Enerji (kWh)',
        title='Bina Tiplerine Göre Toplam Günlük Enerji Tüketimi',
        labels={'Toplam Günlük Enerji (kWh)': 'Toplam Günlük Enerji (kWh)'},
        color='Toplam Günlük Enerji (kWh)',
        color_continuous_scale='Viridis'
    )
    fig8.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        margin=dict(t=50, b=50)
    )
    fig8.update_xaxes(gridcolor='#f0f0f0')
    fig8.update_yaxes(gridcolor='#f0f0f0')
    
    st.plotly_chart(fig8, use_container_width=True)
    
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

    # Aktif ve Reaktif Güç Grafikleri
    st.markdown("""
    ### ⚡ Güç Analizi
    Aşağıdaki grafikler, bina tiplerinin aktif ve reaktif güç değerlerini göstermektedir.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### Aktif Güç Analizi
        Binaların tükettiği gerçek güç miktarını gösterir.
        """)
        
        fig_active = px.bar(
            results_with_counts_df,
            x='Bina Tipi',
            y='Toplam Aktif Güç (W)',
            title='Bina Tiplerine Göre Toplam Aktif Güç',
            color='Toplam Aktif Güç (W)',
            color_continuous_scale='Blues'
        )
        fig_active.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            showlegend=False
        )
        fig_active.update_xaxes(gridcolor='#f0f0f0')
        fig_active.update_yaxes(gridcolor='#f0f0f0')
        
        st.plotly_chart(fig_active, use_container_width=True)

    with col2:
        st.markdown("""
        #### Reaktif Güç Analizi
        Sistemdeki reaktif güç tüketimini gösterir.
        """)
        
        fig_reactive = px.line(
            results_with_counts_df,
            x='Bina Tipi',
            y='Toplam Reaktif Güç (VAR)',
            title='Bina Tiplerine Göre Toplam Reaktif Güç',
            markers=True
        )
        fig_reactive.update_traces(
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        )
        fig_reactive.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12)
        )
        fig_reactive.update_xaxes(gridcolor='#f0f0f0')
        fig_reactive.update_yaxes(gridcolor='#f0f0f0')
        
        st.plotly_chart(fig_reactive, use_container_width=True)

    # Açıklama kutusu
    st.markdown("""
    <div style='background-color: #e1f5fe; padding: 15px; border-radius: 5px; margin-top: 20px'>
        <h4 style='color: #0277bd; margin-bottom: 10px'>📝 Önemli Bilgiler</h4>
        <ul>
            <li><strong>Aktif Güç:</strong> Gerçek iş yapan, faydalı güç bileşenidir.</li>
            <li><strong>Reaktif Güç:</strong> Sistemde dolaşan ancak iş yapmayan güç bileşenidir.</li>
            <li><strong>Güç Faktörü:</strong> {:.2f} değeri ile çalışılmaktadır.</li>
        </ul>
    </div>
    """.format(power_factor), unsafe_allow_html=True)
    
# ==========================================
# Finansal Hesaplamalar Sekmesi
# ==========================================
with tab3:
    # Ana başlık ve açıklama
    st.markdown("""
        <div style='background: linear-gradient(to right, #2e7d32, #4caf50); padding: 20px; border-radius: 10px; margin-bottom: 30px'>
            <h2 style='color: white; text-align: center; margin-bottom: 10px'>💰 Finansal Analiz Merkezi</h2>
            <p style='color: white; text-align: center'>
                Güneş enerjisi sisteminizin detaylı finansal analizini yapın.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Finansal analizler nesnesini oluştur
    finansal_analizler = FinansalAnalizler()

    # Panel ve Kurulum Maliyetleri
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32; margin-bottom: 20px'>
            <h3 style='color: #2c3e50; margin-bottom: 10px'>📊 Panel ve Kurulum Maliyetleri</h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        panel_sayisi = st.number_input(
            "Panel Sayısı",
            value=10,
            step=1,
            help="Kurulacak toplam panel sayısı"
        )
        panel_birim_fiyat = st.number_input(
            "Panel Birim Fiyatı (TL)",
            value=5000.0,
            step=100.0,
            help="Tek panelin maliyeti"
        )

    with col2:
        iscilik_birim_fiyat = st.number_input(
            "İşçilik Birim Fiyatı (TL/panel)",
            value=1000.0,
            step=100.0
        )
        ekipman_maliyeti = st.number_input(
            "Ekipman Maliyeti (TL)",
            value=20000.0,
            step=1000.0
        )
        tasima_montaj = st.number_input(
            "Taşıma ve Montaj Maliyeti (TL)",
            value=5000.0,
            step=500.0
        )

    # Panel maliyeti hesaplama
    panel_maliyet = finansal_analizler.panel_maliyeti_hesapla(panel_sayisi, panel_birim_fiyat)
    kurulum_maliyet = finansal_analizler.kurulum_maliyeti_hesapla(
        panel_sayisi, iscilik_birim_fiyat, ekipman_maliyeti, tasima_montaj
    )

    # Sistem Gücü ve Bakım
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #1976d2; margin: 30px 0'>
            <h3 style='color: #2c3e50; margin-bottom: 10px'>⚡ Sistem Gücü ve Bakım</h3>
        </div>
    """, unsafe_allow_html=True)

    sistem_gucu = st.number_input(
        "Sistem Gücü (kW)",
        value=10.0,
        step=0.5,
        help="Toplam sistem gücü (kW)"
    )

    bakim_maliyet = finansal_analizler.bakim_maliyeti_hesapla(sistem_gucu)

    # Sonuçları kartlar halinde göster
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; height: 100%'>
                <h4 style='color: #2e7d32; margin-bottom: 15px'>💵 Panel ve Kurulum Maliyetleri</h4>
                <ul style='list-style-type: none; padding: 0'>
                    <li style='margin-bottom: 10px'>Panel Maliyeti: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>KDV Tutarı: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>Toplam Panel Maliyeti: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>İşçilik Maliyeti: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>Ekipman Maliyeti: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>Taşıma ve Montaj: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>Toplam Kurulum: <strong>{:,.2f} TL</strong></li>
                </ul>
            </div>
        """.format(
            panel_maliyet['panel_maliyeti'],
            panel_maliyet['kdv_tutari'],
            panel_maliyet['toplam_maliyet'],
            kurulum_maliyet['iscilik_maliyeti'],
            kurulum_maliyet['ekipman_maliyeti'],
            kurulum_maliyet['tasima_montaj'],
            kurulum_maliyet['toplam_kurulum']
        ), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; height: 100%'>
                <h4 style='color: #1976d2; margin-bottom: 15px'>🔧 Bakım Maliyetleri</h4>
                <ul style='list-style-type: none; padding: 0'>
                    <li style='margin-bottom: 10px'>Yıllık Bakım: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>5 Yıllık Bakım: <strong>{:,.2f} TL</strong></li>
                    <li style='margin-bottom: 10px'>10 Yıllık Bakım: <strong>{:,.2f} TL</strong></li>
                </ul>
            </div>
        """.format(
            bakim_maliyet['yillik_bakim'],
            bakim_maliyet['5_yillik_bakim'],
            bakim_maliyet['10_yillik_bakim']
        ), unsafe_allow_html=True)

    # Kredi Hesaplama Bölümü
    st.markdown("""
        <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px; margin-top: 30px'>
            <h4 style='color: #e65100; margin-bottom: 15px'>🕒 Kredi Hesaplama</h4>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        kredi_tutari = st.number_input(
            "Kredi Tutarı (TL)",
            value=float(panel_maliyet['toplam_maliyet'] + kurulum_maliyet['toplam_kurulum']),
            step=1000.0,
            help="Kullanmak istediğiniz kredi tutarını giriniz"
        )
    
    with col2:
        vade_yil = st.number_input(
            "Vade (Yıl)",
            value=5,
            step=1,
            min_value=1,
            max_value=10,
            help="1-10 yıl arası vade seçebilirsiniz"
        )
    
    with col3:
        faiz_orani = st.number_input(
            "Yıllık Faiz Oranı (%)",
            value=35.0,
            step=0.1,
            min_value=0.0,
            max_value=100.0,
            help="Yıllık faiz oranını giriniz"
        )

    # Kredi özet bilgileri
    aylik_faiz = faiz_orani / 12 / 100
    vade_ay = vade_yil * 12
    aylik_taksit = (kredi_tutari * aylik_faiz * (1 + aylik_faiz)**vade_ay) / ((1 + aylik_faiz)**vade_ay - 1)
    toplam_geri_odeme = aylik_taksit * vade_ay
    toplam_faiz = toplam_geri_odeme - kredi_tutari

    # Kredi özet kartları
    ozet_col1, ozet_col2, ozet_col3, ozet_col4 = st.columns(4)
    
    with ozet_col1:
        st.metric(
            "Aylık Taksit",
            f"{aylik_taksit:,.2f} TL",
            help="Her ay ödenecek sabit taksit tutarı"
        )
    
    with ozet_col2:
        st.metric(
            "Toplam Geri Ödeme",
            f"{toplam_geri_odeme:,.2f} TL",
            f"{toplam_geri_odeme - kredi_tutari:,.2f} TL Fark",
            help="Toplam ödenecek tutar"
        )
    
    with ozet_col3:
        st.metric(
            "Toplam Faiz",
            f"{toplam_faiz:,.2f} TL",
            help="Ödenecek toplam faiz tutarı"
        )
    
    with ozet_col4:
        st.metric(
            "Faiz/Anapara Oranı",
            f"%{(toplam_faiz/kredi_tutari)*100:.1f}",
            help="Toplam faizin anaparaya oranı"
        )

    # Kredi ödeme planı (açılır-kapanır)
    with st.expander("💰 Detaylı Kredi Ödeme Planını Görüntüle", expanded=False):
        kredi_plani = finansal_analizler.kredi_hesapla(kredi_tutari, vade_yil, faiz_orani)
        
        # Ödeme planı tablosu
        st.dataframe(
            kredi_plani.style.format({
                'Taksit No': '{:.0f}',
                'Taksit Tutarı': '{:,.2f} TL',
                'Anapara': '{:,.2f} TL',
                'Faiz': '{:,.2f} TL',
                'Kalan Anapara': '{:,.2f} TL'
            }).background_gradient(
                subset=['Faiz'],
                cmap='Oranges'
            ).background_gradient(
                subset=['Anapara'],
                cmap='Greens'
            )
        )

        # Kredi planı grafiği
        fig_kredi = go.Figure()
        fig_kredi.add_trace(go.Bar(
            name='Anapara',
            x=kredi_plani['Taksit No'],
            y=kredi_plani['Anapara'],
            marker_color='#2e7d32'
        ))
        fig_kredi.add_trace(go.Bar(
            name='Faiz',
            x=kredi_plani['Taksit No'],
            y=kredi_plani['Faiz'],
            marker_color='#ef6c00'
        ))

        fig_kredi.update_layout(
            title='Aylık Anapara ve Faiz Dağılımı',
            barmode='stack',
            xaxis_title='Taksit No',
            yaxis_title='Tutar (TL)',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_kredi, use_container_width=True)

        # Kredi bilgi kutusu
        st.info("""
            💡 **Kredi Hesaplama Bilgileri:**
            - Hesaplamalar eşit taksitli (annüite) kredi sistemine göre yapılmıştır
            - Taksit tutarları her ay sabittir
            - KKDF, BSMV gibi ek masraflar dahil değildir
            - Erken ödeme ve kredi yapılandırma senaryoları hesaplanmamıştır
        """)

    # Enerji Dengesi Analizi bölümünde
    st.markdown("### ⚡ Enerji Dengesi ve Verim Analizi")

    col1, col2 = st.columns(2)
    with col1:
        panel_uretimi = st.number_input(
            "Yıllık Panel Üretimi (kWh)",
            value=10000.0,
            step=1000.0,
            help="Panelin yıllık teorik üretim miktarı"
        )
        
        elektrik_satis_fiyati = st.number_input(
            "Elektrik Satış Fiyatı (TL/kWh)",
            value=1.5,
            step=0.1,
            help="Şebekeye satış birim fiyatı"
        )

    with col2:
        bina_tuketimi = st.number_input(
            "Yıllık Bina Tüketimi (kWh)",
            value=12000.0,
            step=1000.0,
            help="Binanın yıllık elektrik tüketimi"
        )
        
        elektrik_alis_fiyati = st.number_input(
            "Elektrik Alış Fiyatı (TL/kWh)",
            value=1.8,
            step=0.1,
            help="Şebekeden alış birim fiyatı"
        )

    # Gelişmiş parametreler
    with st.expander("🔧 Gelişmiş Sistem Parametreleri", expanded=False):
        col3, col4 = st.columns(2)
        with col3:
            panel_efficiency = st.slider(
                "Panel Verimi (%)",
                min_value=15.0,
                max_value=25.0,
                value=20.0,
                step=0.1,
                help="Panel verim oranı"
            ) / 100
            
            satis_carpani = st.slider(
                "Satış Fiyat Çarpanı",
                min_value=0.5,
                max_value=1.0,
                value=0.85,
                step=0.05,
                help="Şebekeye satış fiyat çarpanı"
            )
        
        with col4:
            kayip_faktoru = st.slider(
                "Sistem Kayıpları (%)",
                min_value=5.0,
                max_value=25.0,
                value=15.0,
                step=1.0,
                help="Toplam sistem kayıpları"
            ) / 100

    # Parametreleri güncelle
    yeni_parametreler = {
        'panel_efficiency': panel_efficiency,
        'satis_carpani': satis_carpani,
        'kayip_faktoru': kayip_faktoru,
        'elektrik_satis_fiyati': elektrik_satis_fiyati,
        'elektrik_alis_fiyati': elektrik_alis_fiyati
    }

    varsayilan_parametreler = finansal_analizler.guncelle_varsayilan_parametreler(yeni_parametreler)

    # Analiz sonuçlarını al
    enerji_analizi = finansal_analizler.enerji_dengesi_analizi(
        panel_uretimi=panel_uretimi,
        bina_tuketimi=bina_tuketimi,
        elektrik_satis_fiyati=elektrik_satis_fiyati,
        elektrik_alis_fiyati=elektrik_alis_fiyati,
        panel_efficiency=panel_efficiency,
        varsayilan_parametreler=varsayilan_parametreler
    )

    # Sonuçları göster
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "Net Üretim",
            f"{enerji_analizi['Enerji Dengesi']['Net Panel Üretimi (kWh)']:,.0f} kWh",
            f"Kayıp: {enerji_analizi['Verim Analizi']['Kayıplar (%)']:.1f}%"
        )

    with col6:
        st.metric(
            "Öz Tüketim Oranı",
            f"{enerji_analizi['Verim Analizi']['Öz Tüketim Oranı (%)']:.1f}%",
            f"Şebeke Bağımlılığı: {enerji_analizi['Verim Analizi']['Şebeke Bağımlılığı (%)']:.1f}%"
        )

    with col7:
        st.metric(
            "Satış Geliri",
            f"{enerji_analizi['Finansal Analiz']['Şebekeye Satış Geliri (TL)']:,.2f} TL",
            f"Fazla Enerji: {enerji_analizi['Enerji Dengesi']['Fazla Enerji (kWh)']:,.0f} kWh"
        )

    with col8:
        st.metric(
            "Alış Maliyeti",
            f"{enerji_analizi['Finansal Analiz']['Şebekeden Alış Maliyeti (TL)']:,.2f} TL",
            f"Eksik Enerji: {enerji_analizi['Enerji Dengesi']['Eksik Enerji (kWh)']:,.0f} kWh"
        )

# ==========================================
# Program Nasıl Çalışır Sekmesi
# ==========================================
with tab5:
    program_nasil_calisir()

# ==========================================
# Tablolar ve Veri İndirme Sekmesi
# ==========================================
with tab4:
    # Ana başlık ve açıklama
    st.markdown("""
        <div style='background: linear-gradient(to right, #1a5276, #2980b9); padding: 20px; border-radius: 10px; margin-bottom: 30px'>
            <h2 style='color: white; text-align: center; margin-bottom: 10px'>📊 Veri Analizi ve İndirme Merkezi</h2>
            <p style='color: white; text-align: center'>
                Bu bölümde tüm analiz verilerini detaylı olarak inceleyebilir ve CSV formatında indirebilirsiniz.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Güneş Paneli Verileri
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #2ecc71; margin-bottom: 20px'>
            <h3 style='color: #2c3e50; margin-bottom: 10px'>🌞 Güneş Paneli Verileri</h3>
            <p style='color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px'>
                Panel açıları, ışınım değerleri ve sıcaklık ölçümleri gibi temel güneş enerjisi parametrelerini içerir.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df_solar.style.format({
            'Gunes Sapma Acisi (°)': "{:.2f}",
            'Optimum Panel Acisi (°)': "{:.2f}",
            'Ortalama Gunluk Isinim (W/m²)': "{:.2f}",
            'Panel Sicakligi (°C)': "{:.2f}"
        }).background_gradient(
            cmap='YlOrRd', 
            subset=['Ortalama Gunluk Isinim (W/m²)']
        ).background_gradient(
            cmap='YlOrRd', 
            subset=['Panel Sicakligi (°C)']
        )
    )
    
    st.download_button(
        label="📥 Güneş Paneli Verilerini İndir (CSV)",
        data=df_solar.to_csv(index=False).encode('utf-8'),
        file_name='solar_panel_data.csv',
        mime='text/csv',
        help="Tüm güneş paneli verilerini CSV formatında indirin"
    )

    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

    # Panel Parametreleri
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db; margin-bottom: 20px'>
            <h3 style='color: #2c3e50; margin-bottom: 10px'>⚡ Panel Parametreleri</h3>
            <p style='color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px'>
                Sistemin elektriksel parametrelerini, gerilim, akım ve güç değerlerini gösterir.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df_panel.style.format({
            'Toplam Gerilim (V)': "{:.2f}",
            'Toplam Akım (A)': "{:.2f}",
            'Maksimum Güç (W)': "{:.2f}"
        }).background_gradient(cmap='Blues', subset=['Maksimum Güç (W)'])
    )
    
    st.download_button(
        label="📥 Panel Parametrelerini İndir (CSV)",
        data=df_panel.to_csv(index=False).encode('utf-8'),
        file_name='panel_parameters.csv',
        mime='text/csv',
        help="Panel parametrelerini CSV formatında indirin"
    )

    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

    # Yıllık Optimum Panel Açısı
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #e74c3c; margin-bottom: 20px'>
            <h3 style='color: #2c3e50; margin-bottom: 10px'>📐 Yıllık Optimum Panel Açısı</h3>
            <p style='color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px'>
                Maksimum verim için hesaplanan yıllık optimum panel eğim açısı değeri.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df_yearly.style.format({
            'Yıllık Optimum Panel Açısı (°)': "{:.2f}"
        }).background_gradient(cmap='Oranges')
    )
    
    st.download_button(
        label="📥 Optimum Açı Verilerini İndir (CSV)",
        data=df_yearly.to_csv(index=False).encode('utf-8'),
        file_name='yearly_optimum_angle.csv',
        mime='text/csv',
        help="Yıllık optimum panel açısı verilerini CSV formatında indirin"
    )

    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)

    # Bina Enerji Tüketimi
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #9b59b6; margin-bottom: 20px'>
            <h3 style='color: #2c3e50; margin-bottom: 10px'>🏢 Bina Enerji Tüketimi</h3>
            <p style='color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px'>
                Binaların günlük enerji tüketimi, aktif ve reaktif güç değerleri.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        results_with_counts_df.style.format({
            'Toplam Günlük Enerji (kWh)': "{:.2f}",
            'Toplam Aktif Güç (W)': "{:.2f}",
            'Toplam Reaktif Güç (VAR)': "{:.2f}"
        }).background_gradient(cmap='Purples', subset=['Toplam Günlük Enerji (kWh)'])
    )
    
    st.download_button(
        label="📥 Bina Enerji Verilerini İndir (CSV)",
        data=results_with_counts_df.to_csv(index=False).encode('utf-8'),
        file_name='building_energy_consumption.csv',
        mime='text/csv',
        help="Bina enerji tüketimi verilerini CSV formatında indirin"
    )

    # Bilgi Kutusu
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; margin-top: 20px'>
            <h4 style='color: #2c3e50; margin-bottom: 10px'>ℹ️ Veri Kullanımı Hakkında</h4>
            <ul style='color: #34495e; margin-bottom: 0'>
                <li>Tüm veriler CSV formatında indirilir ve yaygın kullanılan tablo programlarıyla açılabilir.</li>
                <li>Tablolardaki renkli gradyanlar, değerlerin görsel karşılaştırmasını kolaylaştırır.</li>
                <li>İndirilen dosyalar UTF-8 kodlaması kullanır, Türkçe karakterler doğru görüntülenir.</li>
                <li>Veriler üzerinde daha detaylı analiz yapmak için Excel veya benzeri programları kullanabilirsiniz.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

