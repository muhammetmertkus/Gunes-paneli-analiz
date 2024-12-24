import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
from time_series_analysis import show_time_series_analysis

def simulink_karsilastirma(panel_data, solar_data, panel_parameters, results_with_counts_df):
    """
    Python ve Simulink sonuçlarını karşılaştıran ana fonksiyon
    """
    st.markdown("""
        <div style='background: linear-gradient(to right, #1a5276, #2980b9); padding: 20px; border-radius: 10px; margin-bottom: 30px'>
            <h2 style='color: white; text-align: center; margin-bottom: 10px'>🔄 Python - Simulink Karşılaştırma Analizi</h2>
            <p style='color: white; text-align: center'>
                Python hesaplamaları ile Simulink modellemesi sonuçlarının detaylı karşılaştırması
            </p>
        </div>
    """, unsafe_allow_html=True)
    # Simulink modelinin görselini ekle
    st.image("images/simulink.png", caption="Simulink Modeli: Güneş enerjisi sisteminin detaylı devre şeması. Soldan sağa doğru güneş panelleri, MPPT kontrolü, DC/AC dönüştürücü, filtreler, transformatör ve şebeke bağlantıları görülmektedir.", use_container_width=True)

    st.markdown("""
        ### 🎓 Eskişehir Osmangazi Üniversitesi Güneş Enerjisi Projesi

        #### 🎯 Projenin Amacı
        Eskişehir Osmangazi Üniversitesi için yenilenebilir enerji kaynaklarını kullanarak bir güneş enerjisi tarlası kurmak, kampüsün enerji ihtiyacını karşılamak ve fazla enerjiyi satarak ekonomik fayda sağlamak temel hedeftir. Bu proje, üniversitenin enerji bağımsızlığını artırırken çevresel ve ekonomik sürdürülebilirliği hedeflemektedir.

        **Temel Hedefler:**
        - **Kampüsün Enerji İhtiyacını Karşılamak**
        - **Fazla Enerjiyi Şebekeye Satarak Gelir Elde Etmek**
        - **Karbon Ayak İzini Azaltmak ve Sürdürülebilirlik Sağlamak**
        - **Esnek ve Güvenilir Bir Enerji Sistemi Oluşturmak**
        - **Üniversiteye Eğitim ve Araştırma Katkısı Sunmak**

        #### ⚡ Devre Nasıl Çalışıyor?
        Simulink'te tasarlanan bu güneş enerjisi sistemi, güneş panellerinden enerji üretimi ile başlar. Güneş ışınımı (W/m²) ve panel sıcaklığı (°C) değerleri giriş olarak kullanılır. Paneller, doğru akım (DC) enerji üretir ve bu enerji, üç seviyeli IGBT köprüsü tarafından alternatif akıma (AC) dönüştürülür. Maksimum Güç Noktası Takibi (MPPT) algoritması, DC bağlantı voltajını optimize ederek panellerin maksimum verimlilikte çalışmasını sağlar. Dönüştürülen AC enerji, bir transformatör aracılığıyla şebeke voltajına uygun hale getirilir (25 kV). Kampüs içindeki fakülteler, sağlık tesisleri, sosyal alanlar gibi yükler, feeder hatları aracılığıyla enerji sistemine bağlanır ve ihtiyaç duyulan enerji bu sistemden sağlanır.

        #### 🔧 Devrede Kullanılan Malzemeler ve Bileşenler

        1. **Güneş Panelleri**
        - Model: SunPower SPR-415E-WHT-D
        - Özellikler:
          - 16 modüllü stringler, toplamda 74 paralel string
          - STC'de nominal güç: 415 W

        2. **MPPT (Maksimum Güç Noktası Takibi) Kontrolü**
        - Algoritma: Perturb & Observe (P&O)
        - Bileşenler:
          - DC bağlantı voltajı ve akım ölçüm sensörleri
          - MPPT referans gerilim hesaplama ünitesi

        3. **İnverter (DC/AC Dönüştürücü)**
        - Model: Üç seviyeli IGBT köprüsü (3-Level IGBT's Bridge)
        - Bileşenler:
          - IGBT modülleri
          - PWM kontrol sistemi (Sinüzoidal PWM - SPWM)

        4. **Filtreler**
        - RL Filtre: Şebeke ile inverter arasındaki harmonikleri azaltır
        - Kapasitör (C): DC bağlantıda gerilim dalgalanmalarını düzenler

        5. **Transformatör**
        - Model: 120 kV / 25 kV, 47 MVA güç transformatörü
        - Görev: Gerilim seviyesini şebeke standartlarına uygun hale getirmek

        6. **Şebeke Bağlantısı**
        - Feeder Hatları:
          - 8 km Feeder: Şebeke bağlantısı
          - 2 km Feeder (Kültür ve Sosyal Alanlar)
          - 1-3 km Feeder: Kampüs içindeki yükler

        7. **Kampüs Yükleri**
        - Toplam Yük: 2 MW
        - Özel Yükler:
          - Fakülteler
          - Sağlık tesisleri
          - Araştırma ve uygulama merkezleri
          - Spor alanları
          - Sosyal alanlar
          - Yemek ve konaklama alanları
          - Helikopter pisti

        8. **Ölçüm Sistemleri**
        - DC Tarafı:
          - Gerilim sensörleri (Vdc)
          - Akım sensörleri (Idc)
        - AC Tarafı:
          - Gerilim sensörleri (Vabc)
          - Akım sensörleri (Iabc)

        9. **Şebeke Kontrol Sistemi**
        - PLL (Phase Locked Loop): Şebeke frekansı ile senkronizasyon
        - Gerilim Referansı (Uref): Şebeke için gerilim referansı üretimi

        10. **Topraklama Transformatörü**
        - Görev: Sistem güvenliğini ve akım dengesini sağlamak

        11. **PowerGUI**
        - Görev: Simulink'te sayısal hesaplama ayarları ve analiz desteği

        12. **Koruma ve Hata Yönetimi**
        - Devre Kesiciler (Breakers): Şebeke bağlantı kesintisi ve güvenlik için

        ### SunPower SPR-415E-WHT-D Güneş Paneli Özeti

        #### Elektriksel Özellikler
        - **Nominal Güç (STC):** 415 W
        - **Nominal Güç (PTC):** 385.2 W
        - **Maksimum Güç Gerilimi (Vmp):** 72.9 V
        - **Maksimum Güç Akımı (Imp):** 5.69 A
        - **Açık Devre Gerilimi (Voc):** 85.3 V
        - **Kısa Devre Akımı (Isc):** 6.09 A
        - **Hücre Çalışma Sıcaklığı (NOCT):** 45.8°C
        - **Maksimum Güç Sıcaklık Katsayısı:** -0.353 %/°C

        #### Fiziksel Özellikler
        - **Hücre Tipi:** Monokristalin
        - **Modül Alanı:** 2.16 m²
        - **Uzunluk:** 2067 mm
        - **Genişlik:** 1046 mm

        #### Performans
        - **Modül Verimliliği:** 19.21%
        - **Güç Yoğunluğu (STC):** 192.13 W/m²

        #### 🔄 Inverter (DC/AC Dönüştürücü) Özellikleri
        - **Yapı:** Üç seviyeli IGBT köprüsü
        - **Kontrol Yöntemi:** Sinüzoidal PWM (SPWM) ile enerji kalitesini artırır
        - **Giriş:** Güneş panellerinden gelen DC enerji (~583 V)
        - **Çıkış:** Şebekeye uygun sinüzoidal AC enerji (25 kV transformatöre aktarılır)
        - **Harmonik Azaltımı:** Üç seviyeli yapı sayesinde harmonik içerik minimum düzeye indirilir

        #### 🏗️ Şebeke Bağlantısı ve Kampüs Elektrik Dağıtım Sistemi

        Güvenli ve kararlı bir şekilde hem kampüs yüklerine hem de şebekeye aktarılmasını sağlamak üzere tasarlanmıştır. Bu bağlantı, enerji kalitesini optimize eden ve güvenlik sağlayan kritik bileşenler içerir: transformatör, topraklama transformatörü ve RLC dalları (RLC branch).

        ##### Transformatör (120 kV / 25 kV, 47 MVA)
        Sistemden elde edilen alternatif akım (AC) enerjisi, inverter çıkışında 25 kV seviyesinde üretilir. Bu enerji, kampüs içindeki yüklerin ihtiyaçlarını karşılamak ve şebekeye uygun şekilde enerji sağlamak için bir transformatör tarafından 120 kV seviyesine yükseltilir. Transformatör, hem şebeke hem de kampüs yükleri arasında izolasyon sağlayarak güvenli bir enerji aktarımı gerçekleştirir. Aynı zamanda, enerji kayıplarını minimize ederek sistemin genel verimliliğini artırır. Transformatör, şebeke tarafında harmoniklerin etkisini azaltır ve şebekeye temiz, kararlı bir enerji aktarımı yapar.

        ##### Topraklama Transformatörü
        Sistemin güvenliğini artırmak ve şebekeye entegrasyon sırasında oluşabilecek dengesizlikleri önlemek amacıyla topraklama transformatörü kullanılmıştır. Bu transformatör, üç fazlı sistemde herhangi bir dengesiz akım durumunda fazla akımı güvenli bir şekilde toprağa iletir. Ayrıca, inverter ve şebeke arasında ortak mod gerilimlerini stabilize ederek şebeke bağlantısında kararlılık sağlar. Topraklama transformatörü, olası hataları minimize eder ve enerji aktarımındaki güvenliği artırır. Böylece, hem şebeke hem de kampüs içindeki yüklerin enerji ihtiyaçları kesintisiz ve güvenli bir şekilde karşılanır.

        ##### RLC Dalları (RLC Branch)
        Şebeke bağlantısında enerji kalitesini artırmak için RLC dalları kullanılmıştır. Bu dallar, inverter çıkışındaki harmonikleri filtreler, reaktif güç dengelemesi yapar ve gerilim dalgalanmalarını azaltır. Direnç (R), endüktans (L) ve kapasitör (C) elemanlarından oluşan bu yapı, sistemin enerji kalitesini optimize eder. İnverter çıkışından şebekeye veya kampüs yüklerine enerji aktarılırken yüksek frekanslı harmonikler RLC filtreleri sayesinde azaltılır. Ayrıca, reaktif güç desteği sağlanarak sistemin kararlılığı artırılır ve şebeke ile inverter arasındaki enerji akışı sorunsuz bir şekilde gerçekleştirilir.

        ##### Feeder Hatları ve Kampüs Yükleri
        Transformatörden gelen enerji, farklı uzunluktaki feeder hatları aracılığıyla kampüs içindeki yüklerin enerji ihtiyacını karşılar. Örneğin, kültür ve sosyal alanlara enerji 2 km uzunluğundaki bir feeder hattı ile iletilirken, sağlık tesisleri 1 km uzunluğundaki bir feeder hattı ile enerji sağlar. Diğer yükler (örneğin, fakülteler, spor tesisleri, yemek ve konaklama alanları) ise 2-3 km uzunluğundaki feeder hatlarıyla bağlanmıştır. Toplamda 2 MW'lik yük, kampüsün enerji talebini temsil eder. Kampüs yükleri karşılandıktan sonra, fazla enerji şebekeye aktarılır ve bu fazla enerji ekonomik fayda sağlamak için satılır.

        ##### Yük Dağılımı ve Enerji Tüketimi
        1. **Akademik Birimler**
           - Toplam Güç: ~800 kW
           - Günlük tüketim: 12-14 MWh
           - Pik saatler: 09:00-17:00
           - Klima ve aydınlatma yükleri dominant

        2. **Sağlık Tesisleri**
           - Toplam Güç: ~600 kW
           - 7/24 kesintisiz operasyon
           - Kritik tıbbi cihaz yükleri
           - Yedek güç sistemleri ile entegre

        3. **Sosyal ve Destek Tesisleri**
           - Toplam Güç: ~400 kW
           - Değişken yük profili
           - Sezonsal değişimler belirgin
           - Etkinlik zamanlarında pik yükler

        ##### Akıllı Şebeke Özellikleri
        - **İzleme ve Kontrol**
          - SCADA sistemi entegrasyonu
          - Gerçek zamanlı yük takibi
          - Güç kalitesi monitörizasyonu
          - Arıza tespit ve izolasyon sistemleri

        - **Enerji Yönetimi**
          - Akıllı sayaç altyapısı
          - Yük dengeleme sistemleri
          - Enerji tasarruf algoritmaları
          - Talep yanıt programları

        - **Güvenlik ve Koruma**
          - Dijital koruma röleleri
          - Otomatik tekrar kapama sistemleri
          - Seçici açma-kapama koordinasyonu
          - Yıldırım ve aşırı gerilim koruması

        #### 🔄 Simülasyon ve Performans Testi Detayları
        **Test Koşulları:**
        - 12 aylık Eskişehir ışınım ve sıcaklık verileri
        - Örnek: Haziran'da ışınım 6.38 kWh/m², sıcaklık 22°C; Aralık'ta ışınım 1.47 kWh/m², sıcaklık 0°C

        **Sonuçlar:**
        - Yıllık Üretim: 2.4 GWh enerji üretilmiştir
        - Fazla Enerji: 0.6 GWh şebekeye satılmıştır
        - Verimlilik: Yaz aylarında maksimum kapasiteye ulaşmıştır
    """)

    # Simulink ölçüm değerleri
    simulink_data = {
        'Ay': ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December'],
        'Simulink_V': [583.1, 583.0, 583.2, 582.7, 582.8, 582.9,
                      582.9, 583.2, 583.1, 582.7, 583.1, 583.0],
        'Simulink_I': [31.97, 42.84, 68.87, 89.11, 111.5, 118.1,
                      116.9, 105.3, 86.38, 69.99, 36.46, 27.03]
    }

    # Simulink sonuçları için form
    with st.form("simulink_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            simulink_voltages = []
            st.markdown("#### Simulink Gerilim Değerleri (V)")
            for i, month in enumerate(panel_data['Ay']):
                voltage = st.number_input(
                    f"{month} Gerilim:",
                    value=simulink_data['Simulink_V'][i],
                    step=0.1,
                    format="%.2f",
                    key=f"voltage_{i}"
                )
                simulink_voltages.append(voltage)

        with col2:
            simulink_currents = []
            st.markdown("#### Simulink Akım Değerleri (A)")
            for i, month in enumerate(panel_data['Ay']):
                current = st.number_input(
                    f"{month} Akım:",
                    value=simulink_data['Simulink_I'][i],
                    step=0.01,
                    format="%.2f",
                    key=f"current_{i}"
                )
                simulink_currents.append(current)

        with col3:
            st.markdown("#### Güneşlenme Süresi")
            gunes_saati = st.number_input(
                "Günlük Ortalama Saat",
                value=8.0,
                min_value=1.0,
                max_value=24.0,
                step=0.5,
                key="gunes_saati"
            )

        submitted = st.form_submit_button("Karşılaştırmayı Güncelle")

    if 'yearly_energy' not in st.session_state:
        # Başlangıç değerlerini hesapla
        initial_power = [v * i for v, i in zip(simulink_data['Simulink_V'], simulink_data['Simulink_I'])]
        initial_daily = [(p * 8.0) / 1000 for p in initial_power]  # 8 saat varsayılan güneşlenme
        initial_monthly = [(d * 30) / 1000 for d in initial_daily]
        st.session_state.yearly_energy = sum(initial_monthly)
        st.session_state.monthly_energy = initial_monthly
        st.session_state.daily_energy = initial_daily
        st.session_state.power = initial_power

    if submitted or 'simulink_results' not in st.session_state:
        # Simulink güç ve enerji hesaplamaları
        simulink_power = [v * i for v, i in zip(simulink_voltages, simulink_currents)]
        daily_energy = [(p * gunes_saati) / 1000 for p in simulink_power]  # kWh
        monthly_energy = [(d * 30) / 1000 for d in daily_energy]  # MWh
        yearly_energy = sum(monthly_energy)  # MWh

        # Session state'i güncelle
        st.session_state.yearly_energy = yearly_energy
        st.session_state.monthly_energy = monthly_energy
        st.session_state.daily_energy = daily_energy
        st.session_state.power = simulink_power

        # Karşılaştırma sonuçlarını hesapla
        simulink_results = pd.DataFrame({
            'Ay': panel_data['Ay'],
            'Simulink Gerilim (V)': simulink_voltages,
            'Simulink Akım (A)': simulink_currents,
            'Simulink Güç (W)': st.session_state.power,
            'Python Gerilim (V)': panel_data['Toplam Gerilim (V)'],
            'Python Akım (A)': panel_data['Toplam Akım (A)'],
            'Python Güç (W)': panel_data['Maksimum Güç (W)']
        })
        
        # Fark hesaplamaları
        simulink_results['Gerilim Farkı (%)'] = ((simulink_results['Simulink Gerilim (V)'] - 
                                                 simulink_results['Python Gerilim (V)']) / 
                                                simulink_results['Python Gerilim (V)'] * 100)
        simulink_results['Akım Farkı (%)'] = ((simulink_results['Simulink Akım (A)'] - 
                                              simulink_results['Python Akım (A)']) / 
                                             simulink_results['Python Akım (A)'] * 100)
        simulink_results['Güç Farkı (%)'] = ((simulink_results['Simulink Güç (W)'] - 
                                             simulink_results['Python Güç (W)']) / 
                                            simulink_results['Python Güç (W)'] * 100)
        
        st.session_state.simulink_results = simulink_results

    # Finansal hesaplamalar için session_state'den değerleri al
    yillik_uretim = st.session_state.yearly_energy / 1000  # MWh to GWh conversion
    sebekeye_satilan = yillik_uretim * 0.25  # Üretimin %25'ini sattığımızı varsayalım
    tuketilen = yillik_uretim - sebekeye_satilan  # GWh

    # Üretim ve tüketim hesaplamaları
    if 'forecast_2025' in st.session_state:
        # Günlük enerji üretimlerini hesapla (kWh)
        gunluk_uretimler = []
        for v, i in zip(simulink_voltages, simulink_currents):
            guc = v * i  # Watt
            gunluk_enerji = (guc * gunes_saati) / 1000  # kWh
            gunluk_uretimler.append(gunluk_enerji)
        
        # Aylık üretimleri hesapla
        aylik_uretimler = [gunluk * 30 for gunluk in gunluk_uretimler]  # kWh/ay
        
        # Yıllık üretimi hesapla
        yillik_uretim = sum(aylik_uretimler) / 1000000  # GWh/yıl
        
        # Yıllık tüketimi hesapla (forecast_2025'ten)
        yillik_tuketim = sum(st.session_state.forecast_2025)  # GWh/yıl (forecast zaten GWh cinsinden)
        
        # Üretim-Tüketim Detaylı Karşılaştırma
        st.markdown("### 📊 Üretim-Tüketim Detaylı Karşılaştırma")

    # Karşılaştırma grafikleri
    st.markdown("### 📈 Karşılaştırma Grafikleri")
    
    # Grafik seçimi
    graph_type = st.selectbox(
        "Grafik Türü",
        ["Gerilim Karşılaştırması", "Akım Karşılaştırması", "Güç Karşılaştırması"]
    )

    if graph_type == "Gerilim Karşılaştırması":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.simulink_results['Ay'],
            y=st.session_state.simulink_results['Python Gerilim (V)'],
            name='Python',
            line=dict(color='#2ecc71', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=st.session_state.simulink_results['Ay'],
            y=st.session_state.simulink_results['Simulink Gerilim (V)'],
            name='Simulink',
            line=dict(color='#e74c3c', width=3)
        ))
        fig.update_layout(
            title='Gerilim Karşılaştırması',
            xaxis_title='Ay',
            yaxis_title='Gerilim (V)'
        )

    elif graph_type == "Akım Karşılaştırması":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.simulink_results['Ay'],
            y=st.session_state.simulink_results['Python Akım (A)'],
            name='Python',
            line=dict(color='#2ecc71', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=st.session_state.simulink_results['Ay'],
            y=st.session_state.simulink_results['Simulink Akım (A)'],
            name='Simulink',
            line=dict(color='#e74c3c', width=3)
        ))
        fig.update_layout(
            title='Akım Karşılaştırması',
            xaxis_title='Ay',
            yaxis_title='Akım (A)'
        )

    else:  # Güç Karşılaştırması
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.simulink_results['Ay'],
            y=st.session_state.simulink_results['Python Güç (W)'],
            name='Python',
            line=dict(color='#2ecc71', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=st.session_state.simulink_results['Ay'],
            y=st.session_state.simulink_results['Simulink Güç (W)'],
            name='Simulink',
            line=dict(color='#e74c3c', width=3)
        ))
        fig.update_layout(
            title='Güç Karşılaştırması',
            xaxis_title='Ay',
            yaxis_title='Güç (W)'
        )

    st.plotly_chart(fig, use_container_width=True)

    # Karşılaştırma tablosu
    st.markdown("### 📊 Detaylı Karşılaştırma Tablosu")
    st.dataframe(
        st.session_state.simulink_results.style.format({
            'Simulink Gerilim (V)': '{:.2f}',
            'Simulink Akım (A)': '{:.2f}',
            'Simulink Güç (W)': '{:.2f}',
            'Python Gerilim (V)': '{:.2f}',
            'Python Akım (A)': '{:.2f}',
            'Python Güç (W)': '{:.2f}',
            'Gerilim Farkı (%)': '{:.2f}%',
            'Akım Farkı (%)': '{:.2f}%',
            'Güç Farkı (%)': '{:.2f}%'
        }).background_gradient(
            subset=['Gerilim Farkı (%)', 'Akım Farkı (%)', 'Güç Farkı (%)'],
            cmap='RdYlGn_r'
        )
    )

    # İstatistiksel analiz
    st.markdown("### 📈 İstatistiksel Analiz")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Ortalama Gerilim Farkı",
            f"{abs(st.session_state.simulink_results['Gerilim Farkı (%)'].mean()):.2f}%"
        )
    with col2:
        st.metric(
            "Ortalama Akım Farkı",
            f"{abs(st.session_state.simulink_results['Akım Farkı (%)'].mean()):.2f}%"
        )
    with col3:
        st.metric(
            "Ortalama Güç Farkı",
            f"{abs(st.session_state.simulink_results['Güç Farkı (%)'].mean()):.2f}%"
        )

    # Açıklama ve notlar
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px'>
            <h4 style='color: #2c3e50; margin-bottom: 10px'>📝 Karşılaştırma Notları</h4>
            <ul>
                <li>Pozitif fark değerleri, Simulink sonuçlarının Python sonuçlarından yüksek olduğunu gösterir.</li>
                <li>Negatif fark değerleri, Python sonuçlarının Simulink sonuçlarından yüksek olduğunu gösterir.</li>
                <li>%5'ten düşük farklar genellikle kabul edilebilir sınırlar içindedir.</li>
                <li>Büyük farklar için modelleme varsayımları ve parametreler kontrol edilmelidir.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        ### 💰 Kar-Zarar Analizi
        ---
    """)

    # 2025 tüketim tahminlerini session state'den al
    if 'forecast_2025' in st.session_state:
        monthly_consumption_2025 = st.session_state.forecast_2025
        
        # Aylık tüketim verilerini DataFrame'e dönüştür
        consumption_df = pd.DataFrame({
            'Ay': ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 
                   'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
            'Toplam Günlük Enerji (kWh)': monthly_consumption_2025
        })
        
        st.markdown("""
        ### 📊 2025 Yılı Tahmini Aylık Enerji Tüketimi
        Bu grafik, 2025 yılı için tahmin edilen aylık enerji tüketimlerini göstermektedir. 
        Renk skalası, tüketim miktarına göre değişmektedir.
        """)
        
        fig8 = px.bar(
            consumption_df,
            x='Ay',
            y='Toplam Günlük Enerji (kWh)',
            title='2025 Yılı Aylık Enerji Tüketim Tahmini',
            labels={'Toplam Günlük Enerji (kWh)': 'Günlük Ortalama Enerji (kWh)'},
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
        
        st.plotly_chart(fig8, use_container_width=True, key="forecast_2025_consumption")
        
        # Toplam tüketim hesaplamaları
        toplam_gunluk_tuketim = consumption_df['Toplam Günlük Enerji (kWh)'].mean()
        toplam_yillik_tuketim = (toplam_gunluk_tuketim * 365) / 1000000  # GWh/yıl'a çevir

    # Finansal analiz kısmı
    st.markdown("### 💰 Finansal Analiz")
    
    col1, col2 = st.columns(2)
    
    with col1:
        satis_fiyati = st.number_input(
            "Şebekeye Satış Fiyatı (TL/kWh)",
            value=2.50,
            step=0.01,
            format="%.2f"
        )
        
        alis_fiyati = st.number_input(
            "Şebekeden Alış Fiyatı (TL/kWh)",
            value=3.00,
            step=0.01,
            format="%.2f"
        )
    
    with col2:
        sistem_maliyeti = st.number_input(
            "Sistem Toplam Maliyeti (TL)",
            value=47500000.00,
            step=1000.00,
            format="%.2f"
        )
        
        bakim_maliyeti = st.number_input(
            "Yıllık Bakım Maliyeti (TL)",
            value=250000.00,
            step=1000.00,
            format="%.2f"
        )

    # Finansal hesaplamalar
    yillik_uretim_kwh = yillik_uretim * 1000000  # GWh'den kWh'e çevir
    yillik_tasarruf = yillik_uretim_kwh * alis_fiyati  # TL/yıl
    
    # Amortisman süresi (sadece tasarruf üzerinden)
    amortisman_suresi = sistem_maliyeti / (yillik_tasarruf - bakim_maliyeti)
    
    # Finansal metrikler
    st.markdown("#### 📊 Finansal Özet")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Yıllık Enerji Tasarrufu",
            f"{yillik_tasarruf:,.2f} TL",
            f"{yillik_uretim:.3f} GWh değerinde"
        )
    
    with col2:
        st.metric(
            "Yıllık Net Tasarruf",
            f"{(yillik_tasarruf - bakim_maliyeti):,.2f} TL",
            f"Bakım maliyeti düşülmüş"
        )
    
    with col3:
        st.metric(
            "Amortisman Süresi",
            f"{amortisman_suresi:.1f} Yıl",
            "Yatırımın geri dönüş süresi"
        )

    # Yıllık karşılaştırma grafiği
    st.markdown("### 📈 Yıllık Maliyet Karşılaştırması")
    
    yillar = list(range(1, 26))  # 25 yıllık analiz
    kumulatif_tasarruf = [(yillik_tasarruf - bakim_maliyeti) * yil for yil in yillar]
    
    karsilastirma_df = pd.DataFrame({
        'Yıl': yillar,
        'Kümülatif Tasarruf': kumulatif_tasarruf,
        'Sistem Maliyeti': [sistem_maliyeti] * len(yillar)
    })
    
    fig = px.line(karsilastirma_df, x='Yıl', y=['Kümülatif Tasarruf', 'Sistem Maliyeti'],
                 title='Yıllara Göre Kümülatif Tasarruf vs Sistem Maliyeti')
    st.plotly_chart(fig, use_container_width=True)

    # Detaylı açıklama
    st.markdown("""
    #### 💡 Finansal Analiz Açıklaması
    - **Yıllık Enerji Tasarrufu**: Üretilen enerji sayesinde şebekeden alınmayan enerji maliyeti
    - **Yıllık Net Tasarruf**: Bakım maliyetleri düşüldükten sonraki net tasarruf
    - **Amortisman Süresi**: Net tasarruf ile sistem yatırımının kendini ödeme süresi
    - **Not**: Hesaplamalar güncel enerji fiyatları üzerinden yapılmıştır
    """)

    # Üretim-Tüketim Detaylı Karşılaştırma
    st.markdown("### 📊 Üretim-Tüketim Detaylı Karşılaştırma")

    # Günlük, aylık ve yıllık ortalamalar
    col1, col2, col3 = st.columns(3)

    # Günlük ortalamalar
    with col1:
        st.markdown("#### 📅 Günlük Ortalamalar")
        gunluk_ort_uretim = sum(gunluk_uretimler) / len(gunluk_uretimler)
        gunluk_ort_tuketim = (yillik_tuketim * 1000000) / 365  # GWh -> kWh
        
        st.metric(
            "Günlük Ortalama Üretim",
            f"{gunluk_ort_uretim:.2f} kWh"
        )
        st.metric(
            "Günlük Ortalama Tüketim",
            f"{gunluk_ort_tuketim:.2f} kWh"
        )
        gunluk_karsilama = (gunluk_ort_uretim / gunluk_ort_tuketim) * 100
        st.metric(
            "Günlük Karşılama Oranı",
            f"%{gunluk_karsilama:.1f}"
        )

    # Aylık ortalamalar
    with col2:
        st.markdown("#### 📅 Aylık Ortalamalar")
        aylik_ort_uretim = sum(aylik_uretimler) / len(aylik_uretimler)
        aylik_ort_tuketim = (yillik_tuketim * 1000000) / 12  # GWh -> kWh
        
        st.metric(
            "Aylık Ortalama Üretim",
            f"{aylik_ort_uretim/1000:.2f} MWh"
        )
        st.metric(
            "Aylık Ortalama Tüketim",
            f"{aylik_ort_tuketim/1000:.2f} MWh"
        )
        aylik_karsilama = (aylik_ort_uretim / aylik_ort_tuketim) * 100
        st.metric(
            "Aylık Karşılama Oranı",
            f"%{aylik_karsilama:.1f}"
        )

    # Yıllık toplamlar
    with col3:
        st.markdown("#### 📅 Yıllık Toplamlar")
        st.metric(
            "Yıllık Toplam Üretim",
            f"{yillik_uretim:.2f} GWh"
        )
        st.metric(
            "Yıllık Toplam Tüketim",
            f"{yillik_tuketim:.2f} GWh"
        )
        yillik_karsilama = (yillik_uretim / yillik_tuketim) * 100
        st.metric(
            "Yıllık Karşılama Oranı",
            f"%{yillik_karsilama:.1f}"
        )

    # Karşılaştırma grafiği
    st.markdown("#### 📈 Üretim-Tüketim Karşılaştırma Grafiği")
    
    karsilastirma_data = pd.DataFrame({
        'Periyot': ['Günlük', 'Aylık', 'Yıllık'],
        'Üretim (MWh)': [gunluk_ort_uretim/1000, aylik_ort_uretim/1000, yillik_uretim*1000],
        'Tüketim (MWh)': [gunluk_ort_tuketim/1000, aylik_ort_tuketim/1000, yillik_tuketim*1000],
        'Karşılama Oranı (%)': [gunluk_karsilama, aylik_karsilama, yillik_karsilama]
    })

    fig = px.bar(karsilastirma_data, x='Periyot', 
                 y=['Üretim (MWh)', 'Tüketim (MWh)'],
                 title='Periyodik Üretim-Tüketim Karşılaştırması',
                 barmode='group')
    
    # İkinci y-ekseni için karşılama oranı çizgisi
    fig.add_trace(
        go.Scatter(
            x=karsilastirma_data['Periyot'],
            y=karsilastirma_data['Karşılama Oranı (%)'],
            name='Karşılama Oranı (%)',
            yaxis='y2',
            line=dict(color='red', width=2)
        )
    )

    fig.update_layout(
        yaxis2=dict(
            title='Karşılama Oranı (%)',
            overlaying='y',
            side='right'
        ),
        yaxis_title='Enerji (MWh)',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detaylı tablo
    st.markdown("#### 📋 Detaylı Karşılaştırma Tablosu")
    st.dataframe(
        karsilastirma_data.style.format({
            'Üretim (MWh)': '{:.2f}',
            'Tüketim (MWh)': '{:.2f}',
            'Karşılama Oranı (%)': '{:.1f}%'
        })
    )

    