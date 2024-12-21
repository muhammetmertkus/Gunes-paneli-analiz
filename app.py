# -*- coding: utf-8 -*-

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

from finansal_hesaplamalar import FinansalAnalizler
finansal_analizler = FinansalAnalizler()

from building_energy_analysis import calculate_building_energy
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
        'About': """Bu uygulama Güneş Paneli ve Bina Enerji Tüketimi Analizi için 
                   geliştirilmiş kapsamlı bir araçtır. Güneş paneli performansı, 
                   enerji üretimi ve finansal analizler dahil olmak üzere detaylı 
                   hesaplamalar sunar."""
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
image_path = r"images/muhammet_mert_kus.jpg"

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
            <h2 style='color: white; text-align: center; margin-bottom: 10px'>💰 Detaylı Finansal Analiz Merkezi</h2>
            <p style='color: white; text-align: center'>
                Güneş enerjisi sisteminizin kapsamlı finansal ve teknik analizini gerçekleştirin.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Sekme oluşturma
    fin_tab1, fin_tab2, fin_tab3, fin_tab4, fin_tab5 = st.tabs([
        "Maliyet Analizi",
        "Kredi ve Finansman",
        "Üretim ve Verimlilik",
        "Finansal Metrikler",
        "Risk ve Çevresel Analiz"
    ])

    # Maliyet Analizi Sekmesi
    with fin_tab1:
        st.markdown("### 📊 Sistem Maliyet Analizi")
        
        col1, col2 = st.columns(2)
        with col1:
            panel_sayisi = st.number_input("Panel Sayısı", value=10, step=1)
            panel_birim_fiyat = st.number_input("Panel Birim Fiyatı (TL)", value=5000.0, step=100.0)
            iscilik_birim_fiyat = st.number_input("İşçilik Birim Fiyatı (TL/panel)", value=1000.0, step=100.0)
        
        with col2:
            ekipman_maliyeti = st.number_input("Ekipman Maliyeti (TL)", value=20000.0, step=1000.0)
            tasima_montaj = st.number_input("Taşıma ve Montaj Maliyeti (TL)", value=5000.0, step=500.0)
            kdv_orani = st.slider("KDV Oranı (%)", min_value=1, max_value=20, value=20)

        # Maliyet hesaplamaları
        maliyet_sonuclari = finansal_analizler.panel_maliyeti_hesapla(
            panel_sayisi=panel_sayisi,
            panel_birim_fiyat=panel_birim_fiyat,
            kdv_orani=kdv_orani/100
        )
        
        kurulum_sonuclari = finansal_analizler.kurulum_maliyeti_hesapla(
            panel_sayisi=panel_sayisi,
            iscilik_birim_fiyat=iscilik_birim_fiyat,
            ekipman_maliyeti=ekipman_maliyeti,
            tasima_montaj_maliyeti=tasima_montaj
        )

        # Sonuçları göster
        st.markdown("#### 💡 Maliyet Özeti")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Panel Maliyeti", f"{maliyet_sonuclari['panel_maliyeti']:,.2f} TL")
            st.metric("KDV Tutarı", f"{maliyet_sonuclari['kdv_tutari']:,.2f} TL")
        with col2:
            st.metric("İşçilik Maliyeti", f"{kurulum_sonuclari['iscilik_maliyeti']:,.2f} TL")
            st.metric("Ekipman Maliyeti", f"{kurulum_sonuclari['ekipman_maliyeti']:,.2f} TL")
        with col3:
            st.metric("Taşıma ve Montaj", f"{kurulum_sonuclari['tasima_montaj']:,.2f} TL")
            st.metric("Toplam Maliyet", 
                     f"{(maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum']):,.2f} TL")

    # Kredi ve Finansman Sekmesi
    with fin_tab2:
        st.markdown("### 💳 Kredi ve Finansman Analizi")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            kredi_tutari = st.number_input(
                "Kredi Tutarı (TL)", 
                value=float(maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum']),
                step=1000.0
            )
        with col2:
            vade_yil = st.number_input("Vade (Yıl)", value=5, min_value=1, max_value=10)
        with col3:
            faiz_orani = st.number_input("Yıllık Faiz Oranı (%)", value=35.0, step=0.1)

        # Kredi hesaplamaları
        kredi_plani = finansal_analizler.kredi_hesapla(kredi_tutari, vade_yil, faiz_orani)
        
        # Kredi özeti
        st.markdown("#### 📈 Kredi Özeti")
        ozet_col1, ozet_col2, ozet_col3 = st.columns(3)
        with ozet_col1:
            aylik_taksit = kredi_plani['Taksit Tutarı'].iloc[0]
            st.metric("Aylık Taksit", f"{aylik_taksit:,.2f} TL")
        with ozet_col2:
            toplam_odeme = kredi_plani['Taksit Tutarı'].sum()
            st.metric("Toplam Ödeme", f"{toplam_odeme:,.2f} TL")
        with ozet_col3:
            toplam_faiz = toplam_odeme - kredi_tutari
            st.metric("Toplam Faiz", f"{toplam_faiz:,.2f} TL")

        # Kredi planı grafiği
        st.markdown("#### 📊 Kredi Geri Ödeme Planı")
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
            yaxis_title='Tutar (TL)'
        )
        st.plotly_chart(fig_kredi, use_container_width=True)

    # Üretim ve Verimlilik Sekmesi
    with fin_tab3:
        st.markdown("""
            ### ⚡ Üretim ve Verimlilik Analizi
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px'>
                <p style='margin: 0'>Bu bölümde sistemin üretim kapasitesi, verimlilik parametreleri ve kayıp faktörleri analiz edilmektedir.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Ana parametreler
        col1, col2 = st.columns(2)
        with col1:
            yillik_uretim = st.number_input("Yıllık Üretim Tahmini (kWh)", value=10000.0, step=1000.0)
            yillik_tuketim = st.number_input("Yıllık Tüketim Tahmini (kWh)", value=12000.0, step=1000.0)
            elektrik_birim_fiyat = st.number_input("Elektrik Birim Fiyatı (TL/kWh)", value=1.5, step=0.1)
        
        with col2:
            oz_tuketim_orani = st.slider("Öz Tüketim Oranı (%)", min_value=0, max_value=100, value=70)
            sebeke_bagimliligi = st.slider("Şebeke Bağımlılık Oranı (%)", min_value=0, max_value=100, value=30)

        # Verimlilik Parametreleri
        st.markdown("#### 🔧 Verimlilik Parametreleri")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            panel_verimi = st.slider("Panel Verimi (%)", min_value=15, max_value=25, value=20)
            golgelenme_kaybi = st.slider("Gölgelenme Kaybı (%)", min_value=0, max_value=15, value=5)
        
        with col4:
            sistem_kayiplari = st.slider("Sistem Kayıpları (%)", min_value=5, max_value=25, value=15)
            sicaklik_kaybi = st.slider("Sıcaklık Kaybı (%)", min_value=0, max_value=10, value=3)
        
        with col5:
            kablo_kaybi = st.slider("Kablo Kaybı (%)", min_value=0, max_value=10, value=2)
            inverter_verimi = st.slider("İnverter Verimi (%)", min_value=90, max_value=99, value=96)

        # Mevsimsel Dağılım
        st.markdown("#### 🌞 Mevsimsel Üretim Dağılımı")
        col6, col7 = st.columns(2)
        
        with col6:
            kis_orani = st.slider("Kış Üretim Oranı (%)", min_value=10, max_value=40, value=15)
            ilkbahar_orani = st.slider("İlkbahar Üretim Oranı (%)", min_value=20, max_value=40, value=30)
        
        with col7:
            yaz_orani = st.slider("Yaz Üretim Oranı (%)", min_value=20, max_value=50, value=35)
            sonbahar_orani = st.slider("Sonbahar Üretim Oranı (%)", min_value=10, max_value=40, value=20)

        # Üretim analizi hesaplamaları
        uretim_analizi, amortisman_yili = finansal_analizler.detayli_elektrik_analizi(
            yillik_uretim=yillik_uretim,
            elektrik_birim_fiyat=elektrik_birim_fiyat,
            panel_verim=panel_verimi/100,
            sistem_kayip=sistem_kayiplari/100,
            sistem_maliyeti=maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum'],
            yillik_tuketim=yillik_tuketim,
            golgelenme_kayip=golgelenme_kaybi/100,
            sicaklik_kayip=sicaklik_kaybi/100,
            kablo_kayip=kablo_kaybi/100,
            inverter_verim=inverter_verimi/100
        )

        # Performans metrikleri
        performans = finansal_analizler.hesapla_performans_metrikleri(
            uretim_analizi,
            maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum']
        )

        # Sonuçları göster
        st.markdown("#### 📊 Temel Performans Göstergeleri")
        
        # Üretim ve tüketim metrikleri
        col8, col9, col10 = st.columns(3)
        with col8:
            st.metric("Net Yıllık Üretim", f"{performans['Toplam Üretim (kWh)']:,.0f} kWh")
            st.metric("Öz Tüketim Miktarı", f"{yillik_uretim * oz_tuketim_orani/100:,.0f} kWh")
        with col9:
            st.metric("Şebekeye Satılan", f"{yillik_uretim * (1-oz_tuketim_orani/100):,.0f} kWh")
            st.metric("Şebekeden Alınan", f"{yillik_tuketim * sebeke_bagimliligi/100:,.0f} kWh")
        with col10:
            st.metric("Toplam Kayıplar", f"{(sistem_kayiplari + golgelenme_kaybi + sicaklik_kaybi + kablo_kaybi):,.1f}%")
            st.metric("Sistem Verimi", f"{(100 - sistem_kayiplari - golgelenme_kaybi - sicaklik_kaybi - kablo_kaybi):,.1f}%")

        # Finansal metrikler
        st.markdown("#### 💰 Finansal Performans Göstergeleri")
        col11, col12, col13 = st.columns(3)
        with col11:
            st.metric("ROI (Yatırım Getirisi)", f"%{performans['ROI (%)']:.2f}")
            st.metric("Amortisman Süresi", f"{amortisman_yili} Yıl")
        with col12:
            st.metric("LCOE", f"{performans['LCOE (TL/kWh)']:.2f} TL/kWh")
            st.metric("Net Kazanç", f"{performans['Net Kazanç (TL)']:,.2f} TL")
        with col13:
            st.metric("Toplam Gelir", f"{performans['Toplam Gelir (TL)']:,.2f} TL")
            st.metric("Toplam Gider", f"{performans['Toplam Gider (TL)']:,.2f} TL")

        # Mevsimsel üretim grafiği
        st.markdown("#### 📈 Mevsimsel Üretim Dağılımı")
        mevsimsel_data = {
            'Mevsim': ['Kış', 'İlkbahar', 'Yaz', 'Sonbahar'],
            'Üretim Oranı': [kis_orani, ilkbahar_orani, yaz_orani, sonbahar_orani],
            'Üretim Miktarı': [
                yillik_uretim * kis_orani/100,
                yillik_uretim * ilkbahar_orani/100,
                yillik_uretim * yaz_orani/100,
                yillik_uretim * sonbahar_orani/100
            ]
        }
        
        fig_mevsimsel = go.Figure()
        fig_mevsimsel.add_trace(go.Bar(
            x=mevsimsel_data['Mevsim'],
            y=mevsimsel_data['Üretim Miktarı'],
            text=[f'{x:,.0f} kWh' for x in mevsimsel_data['Üretim Miktarı']],
            textposition='auto',
        ))
        fig_mevsimsel.update_layout(
            title='Mevsimsel Üretim Dağılımı',
            xaxis_title='Mevsim',
            yaxis_title='Üretim (kWh)',
            showlegend=False
        )
        st.plotly_chart(fig_mevsimsel, use_container_width=True)

        # Kayıp analizi pasta grafiği
        st.markdown("#### 📉 Sistem Kayıpları Analizi")
        kayip_labels = ['Panel Verimi', 'Gölgelenme Kaybı', 'Sistem Kayıpları', 
                        'Sıcaklık Kaybı', 'Kablo Kaybı', 'İnverter Kaybı']
        kayip_values = [panel_verimi, golgelenme_kaybi, sistem_kayiplari, 
                        sicaklik_kaybi, kablo_kaybi, 100-inverter_verimi]

        fig_kayiplar = go.Figure(data=[go.Pie(
            labels=kayip_labels,
            values=kayip_values,
            hole=.3,
            textinfo='label+percent',
            marker_colors=['#2ecc71', '#e74c3c', '#3498db', '#f1c40f', '#9b59b6', '#95a5a6']
        )])
        fig_kayiplar.update_layout(title='Sistem Kayıpları Dağılımı')
        st.plotly_chart(fig_kayiplar, use_container_width=True)

        # Yıllık üretim ve tüketim karşılaştırma grafiği
        st.markdown("#### 📊 Üretim-Tüketim Dengesi")
        fig_denge = go.Figure()
        fig_denge.add_trace(go.Bar(
            name='Üretim',
            x=['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 
               'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
            y=[yillik_uretim/12 * x for x in [0.6, 0.7, 0.9, 1.1, 1.2, 1.3, 
                                             1.3, 1.2, 1.1, 0.9, 0.7, 0.6]],
            marker_color='#2ecc71'
        ))
        fig_denge.add_trace(go.Bar(
            name='Tüketim',
            x=['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 
               'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
            y=[yillik_tuketim/12] * 12,
            marker_color='#e74c3c'
        ))
        fig_denge.update_layout(
            title='Aylık Üretim-Tüketim Karşılaştırması',
            barmode='group',
            xaxis_title='Ay',
            yaxis_title='Enerji (kWh)'
        )
        st.plotly_chart(fig_denge, use_container_width=True)

        # Detaylı analiz tablosu
        st.markdown("#### 📋 Detaylı Analiz Tablosu")
        detayli_tablo = pd.DataFrame({
            'Parametre': [
                'Toplam Üretim Kapasitesi',
                'Net Üretim',
                'Yıllık Tüketim',
                'Öz Tüketim',
                'Şebekeye Satılan',
                'Şebekeden Alınan',
                'Toplam Kayıplar',
                'Sistem Verimi',
                'Panel Verimi',
                'İnverter Verimi'
            ],
            'Değer': [
                f"{yillik_uretim:,.0f} kWh",
                f"{performans['Toplam Üretim (kWh)']:,.0f} kWh",
                f"{yillik_tuketim:,.0f} kWh",
                f"{yillik_uretim * oz_tuketim_orani/100:,.0f} kWh",
                f"{yillik_uretim * (1-oz_tuketim_orani/100):,.0f} kWh",
                f"{yillik_tuketim * sebeke_bagimliligi/100:,.0f} kWh",
                f"%{(sistem_kayiplari + golgelenme_kaybi + sicaklik_kaybi + kablo_kaybi):,.1f}",
                f"%{(100 - sistem_kayiplari - golgelenme_kaybi - sicaklik_kaybi - kablo_kaybi):,.1f}",
                f"%{panel_verimi:,.1f}",
                f"%{inverter_verimi:,.1f}"
            ]
        })

        st.dataframe(
            detayli_tablo.style.set_properties(**{
                'background-color': '#f8f9fa',
                'border-color': '#dee2e6'
            })
        )

    # Finansal Metrikler Sekmesi
    with fin_tab4:
        st.markdown("""
            ### 📈 Finansal Metrikler ve Projeksiyonlar
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px'>
                <p style='margin: 0'>Bu bölümde sistemin finansal performansı, yatırım getirisi ve uzun vadeli projeksiyonlar analiz edilmektedir.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Temel Finansal Göstergeler
        st.markdown("#### 💰 Temel Finansal Göstergeler")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Toplam Yatırım Maliyeti", 
                f"{(maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum']):,.2f} TL"
            )
            st.metric(
                "Yıllık Ortalama Gelir",
                f"{performans['Toplam Gelir (TL)']/25:,.2f} TL/yıl"
            )
        with col2:
            st.metric(
                "Net Bugünkü Değer (NPV)",
                f"{performans['Net Kazanç (TL)']:,.2f} TL",
                delta=f"%{performans['ROI (%)']:.1f} ROI"
            )
            st.metric(
                "Geri Ödeme Süresi",
                f"{amortisman_yili} Yıl"
            )
        with col3:
            st.metric(
                "LCOE",
                f"{performans['LCOE (TL/kWh)']:.2f} TL/kWh",
                delta="Şebeke Tarifesine Göre"
            )
            st.metric(
                "Yıllık Ortalama Gider",
                f"{performans['Toplam Gider (TL)']/25:,.2f} TL/yıl"
            )

        # ROI değerlerini hesapla
        roi_values = [
            (tasarruf / (maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum'])) * 100 
            for tasarruf in uretim_analizi['Kümülatif Tasarruf (TL)']
        ]

        # Grafik seçimi
        grafik_secimi = st.selectbox(
            "Grafik Türü",
            ["Kümülatif Nakit Akışı", "Yıllık Gelir-Gider Analizi", "ROI Gelişimi"]
        )
        
        if grafik_secimi == "Kümülatif Nakit Akışı":
            fig_projeksiyon = go.Figure()
            fig_projeksiyon.add_trace(go.Scatter(
                x=uretim_analizi['Yıl'],
                y=uretim_analizi['Kümülatif Tasarruf (TL)'],
                mode='lines+markers',
                name='Kümülatif Tasarruf',
                line=dict(color='#2ecc71', width=3)
            ))
            fig_projeksiyon.add_trace(go.Scatter(
                x=uretim_analizi['Yıl'],
                y=[maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum']] * len(uretim_analizi),
                mode='lines',
                name='Başlangıç Yatırımı',
                line=dict(dash='dash', color='#e74c3c')
            ))
            fig_projeksiyon.update_layout(
                title='Kümülatif Nakit Akışı ve Yatırım Karşılaştırması',
                xaxis_title='Yıl',
                yaxis_title='TL',
                hovermode='x unified'
            )
        
        elif grafik_secimi == "Yıllık Gelir-Gider Analizi":
            fig_projeksiyon = go.Figure()
            fig_projeksiyon.add_trace(go.Bar(
                x=uretim_analizi['Yıl'],
                y=uretim_analizi['Toplam Gelir (TL)'],
                name='Gelir',
                marker_color='#2ecc71'
            ))
            fig_projeksiyon.add_trace(go.Bar(
                x=uretim_analizi['Yıl'],
                y=uretim_analizi['Toplam Gider (TL)'],
                name='Gider',
                marker_color='#e74c3c'
            ))
            fig_projeksiyon.update_layout(
                title='Yıllık Gelir-Gider Analizi',
                barmode='group',
                xaxis_title='Yıl',
                yaxis_title='TL',
                hovermode='x unified'
            )
        
        else:  # ROI Gelişimi
            fig_projeksiyon = go.Figure()
            fig_projeksiyon.add_trace(go.Scatter(
                x=uretim_analizi['Yıl'],
                y=roi_values,  # Önceden hesaplanan değerleri kullan
                mode='lines+markers',
                name='ROI (%)',
                line=dict(color='#3498db', width=3)
            ))
            fig_projeksiyon.update_layout(
                title='Yatırım Getirisi (ROI) Gelişimi',
                xaxis_title='Yıl',
                yaxis_title='ROI (%)',
                hovermode='x unified'
            )
        
        st.plotly_chart(fig_projeksiyon, use_container_width=True)

        # Finansal tablo oluşturma
        finansal_tablo = pd.DataFrame({
            'Yıl': uretim_analizi['Yıl'],
            'Gelir (TL)': uretim_analizi['Toplam Gelir (TL)'],
            'Gider (TL)': uretim_analizi['Toplam Gider (TL)'],
            'Net Kazanç (TL)': uretim_analizi['Net Kazanç (TL)'],
            'Kümülatif Tasarruf (TL)': uretim_analizi['Kümülatif Tasarruf (TL)'],
            'ROI (%)': roi_values  # Önceden hesaplanan değerleri kullan
        })
        
        st.dataframe(
            finansal_tablo.style.format({
                'Gelir (TL)': '{:,.2f}',
                'Gider (TL)': '{:,.2f}',
                'Net Kazanç (TL)': '{:,.2f}',
                'Kümülatif Tasarruf (TL)': '{:,.2f}',
                'ROI (%)': '{:.1f}%'
            }).background_gradient(
                subset=['Kümülatif Tasarruf (TL)'],
                cmap='Greens'
            ).background_gradient(
                subset=['ROI (%)'],
                cmap='Blues'
            )
        )

        # Finansal Özet Kartı
        st.markdown("#### 📑 Finansal Özet")
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px'>
                <h5 style='color: #2c3e50; margin-bottom: 15px'>Yatırım Değerlendirmesi</h5>
                <ul style='list-style-type: none; padding: 0'>
                    <li style='margin-bottom: 10px'>💰 <strong>Toplam Yatırım:</strong> {maliyet_sonuclari['toplam_maliyet'] + kurulum_sonuclari['toplam_kurulum']:,.2f} TL</li>
                    <li style='margin-bottom: 10px'>📈 <strong>25 Yıllık Net Kazanç:</strong> {performans['Net Kazanç (TL)']:,.2f} TL</li>
                    <li style='margin-bottom: 10px'>⚡ <strong>Birim Enerji Maliyeti:</strong> {performans['LCOE (TL/kWh)']:.2f} TL/kWh</li>
                    <li style='margin-bottom: 10px'>🔄 <strong>Geri Ödeme Süresi:</strong> {amortisman_yili} Yıl</li>
                    <li style='margin-bottom: 10px'>📊 <strong>Yatırım Getirisi (ROI):</strong> %{performans['ROI (%)']:.1f}</li>
                    <li style='margin-bottom: 10px'>💵 <strong>Yıllık Ortalama Net Kazanç:</strong> {performans['Net Kazanç (TL)']/25:,.2f} TL</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

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
                Maksimum verim için hesaplanan yıllık optimum panel eğim aç���sı değeri.
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
            'Toplam Reaktif Gü�� (VAR)': "{:.2f}"
        }).background_gradient(
            cmap='Purples', 
            subset=['Toplam Günlük Enerji (kWh)']
        )
    )  # Eksik parantez eklendi
    
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

# ==========================================
# Risk ve Çevresel Analiz Sekmesi
# ==========================================
with fin_tab5:
    st.markdown("""
        ### 🌍 Risk ve Çevresel Etki Analizi
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px'>
            <p style='margin: 0'>Bu bölümde sistemin risk faktörleri, çevresel etkileri ve duyarlılık analizleri incelenmektedir.</p>
        </div>
    """, unsafe_allow_html=True)

    # Risk Parametreleri
    st.markdown("#### 🎯 Risk Analizi Parametreleri")
    col1, col2 = st.columns(2)
    
    with col1:
        elektrik_zam_orani = st.slider(
            "Elektrik Zam Oranı (%)", 
            min_value=20, 
            max_value=50, 
            value=35,
            help="Yıllık ortalama elektrik zam oranı tahmini"
        )
        enflasyon_orani = st.slider(
            "Enflasyon Oranı (%)", 
            min_value=20, 
            max_value=50, 
            value=30,
            help="Yıllık ortalama enflasyon oranı tahmini"
        )
        senaryo_sayisi = st.slider(
            "Monte Carlo Senaryo Sayısı", 
            min_value=100, 
            max_value=10000, 
            value=1000,
            help="Risk analizi için üretilecek senaryo sayısı"
        )
    
    with col2:
        uretim_dalgalanma = st.slider(
            "Üretim Dalgalanma Oranı (%)", 
            min_value=5, 
            max_value=25, 
            value=10,
            help="Üretimde beklenen sapma oranı"
        )
        bakim_artis = st.slider(
            "Bakım Maliyeti Artış Oranı (%)", 
            min_value=20, 
            max_value=50, 
            value=30,
            help="Bakım maliyetlerindeki yıllık artış tahmini"
        )

    # Monte Carlo Simülasyonu
    st.markdown("#### 📊 Monte Carlo Simülasyonu Sonuçları")
    
    risk_sonuclari = finansal_analizler.risk_analizi(
        senaryo_sayisi=senaryo_sayisi,
        elektrik_zam_orani=elektrik_zam_orani/100,
        enflasyon_orani=enflasyon_orani/100,
        uretim_dalgalanma=uretim_dalgalanma/100
    )

    col3, col4 = st.columns(2)
    
    with col3:
        # Elektrik zam dağılımı grafiği
        fig_zam = go.Figure()
        fig_zam.add_trace(go.Histogram(
            x=risk_sonuclari['elektrik_zam'],
            name='Elektrik Zam Dağılımı',
            nbinsx=30,
            marker_color='#3498db'
        ))
        fig_zam.update_layout(
            title='Elektrik Zam Oranları Dağılımı',
            xaxis_title='Zam Oranı (%)',
            yaxis_title='Frekans',
            showlegend=False
        )
        st.plotly_chart(fig_zam, use_container_width=True)
    
    with col4:
        # Üretim performansı dağılımı
        fig_uretim = go.Figure()
        fig_uretim.add_trace(go.Histogram(
            x=risk_sonuclari['uretim_performansi'],
            name='Üretim Performansı',
            nbinsx=30,
            marker_color='#2ecc71'
        ))
        fig_uretim.update_layout(
            title='Üretim Performansı Dağılımı',
            xaxis_title='Performans Oranı',
            yaxis_title='Frekans',
            showlegend=False
        )
        st.plotly_chart(fig_uretim, use_container_width=True)

    # Çevresel Etki Analizi
    st.markdown("#### 🌱 Çevresel Etki Analizi")
    
    col5, col6 = st.columns(2)
    
    with col5:
        sera_gazi_faktoru = st.number_input(
            "CO₂ Emisyon Faktörü (kg/kWh)", 
            value=0.5, 
            step=0.1,
            help="Şebeke elektriği üretiminin ortalama CO₂ emisyon faktörü"
        )
    
    with col6:
        agac_esdeger_faktoru = st.number_input(
            "Ağaç Eşdeğer Faktörü (ağaç/ton CO₂)", 
            value=60.5, 
            step=0.5,
            help="1 ton CO₂'nin emilimi için gereken ağaç sayısı"
        )

    # Karbon ayak izi analizi
    karbon_analizi = finansal_analizler.karbon_ayak_izi_analizi(
        yillik_uretim=yillik_uretim,
        sera_gazi_faktoru=sera_gazi_faktoru,
        agac_esdeger_faktoru=agac_esdeger_faktoru
    )

    # Çevresel etki metrikleri
    col7, col8, col9 = st.columns(3)
    with col7:
        st.metric(
            "Yıllık CO₂ Tasarrufu",
            f"{karbon_analizi['yillik_karbon_tasarrufu']:,.2f} ton",
            help="Yıllık önlenen CO₂ emisyonu miktarı"
        )
    with col8:
        st.metric(
            "25 Yıllık CO₂ Tasarrufu",
            f"{karbon_analizi['25_yillik_tasarruf']:,.2f} ton",
            help="Sistemin ömrü boyunca önlenen toplam CO₂ emisyonu"
        )
    with col9:
        st.metric(
            "Ağaç Eşdeğeri",
            f"{karbon_analizi['agac_esdegeri']:,.0f} ağaç",
            help="CO₂ tasarrufuna eşdeğer ağaç sayısı"
        )

    # Çevresel etki grafiği
    st.markdown("#### 📊 Yıllık Çevresel Etki Projeksiyonu")
    fig_cevre = go.Figure()
    yillar = list(range(1, 26))
    karbon_tasarruf = [karbon_analizi['yillik_karbon_tasarrufu'] * (1 - i * 0.005) for i in range(25)]  # Panel yaşlanması etkisi
    
    fig_cevre.add_trace(go.Scatter(
        x=yillar,
        y=karbon_tasarruf,
        mode='lines+markers',
        name='CO₂ Tasarrufu',
        fill='tozeroy',
        line=dict(color='#27ae60')
    ))
    fig_cevre.update_layout(
        title='25 Yıllık CO₂ Tasarrufu Projeksiyonu',
        xaxis_title='Yıl',
        yaxis_title='CO₂ Tasarrufu (ton/yıl)',
        showlegend=False
    )
    st.plotly_chart(fig_cevre, use_container_width=True)

    # Risk analizi özet tablosu
    st.markdown("#### 📋 Risk Analizi Özeti")
    risk_ozet = pd.DataFrame({
        'Parametre': [
            'Ortalama Elektrik Zam Oranı',
            'Ortalama Enflasyon Oranı',
            'Üretim Performans Sapması',
            'Minimum Getiri',
            'Maksimum Getiri',
            'Risk Skoru'
        ],
        'Değer': [
            f"%{risk_sonuclari['elektrik_zam'].mean():.1f}",
            f"%{risk_sonuclari['enflasyon'].mean():.1f}",
            f"%{(risk_sonuclari['uretim_performansi'].std() * 100):.1f}",
            f"%{performans['ROI (%)'] * 0.8:.1f}",
            f"%{performans['ROI (%)'] * 1.2:.1f}",
            f"Orta-{risk_sonuclari['uretim_performansi'].std() * 100:.1f}"
        ]
    })
    
    st.dataframe(
        risk_ozet.style.set_properties(**{
            'background-color': '#f8f9fa',
            'border-color': '#dee2e6'
        })
    )
