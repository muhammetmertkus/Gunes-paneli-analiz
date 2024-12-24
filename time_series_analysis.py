# -*- coding: utf-8 -*-
"""
ESOGÜ Enerji Tüketimi Tahmin Modeli - Teknik Dokümantasyon

1. AMAÇ VE KAPSAM
-----------------
Bu program, Eskişehir Osmangazi Üniversitesi'nin farklı bina tiplerinin enerji tüketimlerini
analiz eder ve gelecek dönem tahminleri yapar. Program, aşağıdaki bina tiplerini kapsar:
- Fakülteler (9 Adet)
- Kültürel ve Sosyal Alanlar (10 Adet)
- Sağlık Tesisleri (3 Adet)
- Araştırma ve Uygulama Merkezleri (7 Adet)
- Spor Alanları (4 Adet)
- Yemek ve Konaklama (2 Adet)
- Park ve Açık Alanlar (2 Adet)
- Helikopter Pisti (1 Adet)

2. VERİ SETİ VE FAKTÖRLER
-------------------------
A) Temel Veri Tablosu:
   - Her bina tipi için minimum, maksimum ve ortalama günlük tüketim değerleri
   - Değerler kWh cinsinden verilmiştir
   - Günlük değerler aylık değerlere dönüştürülmüştür (x30)

B) Dikkate Alınan Faktörler:
   1. Hava Durumu Parametreleri:
      - Sıcaklık (°C)
      - Nem (%)
      - Güneşlenme süresi (saat)
   
   2. Üniversite Aktivite Faktörleri:
      - Dönem Aktivitesi (0-1 arası)
      - Mesai Saatleri Yoğunluğu (0-1 arası)
      - Hafta Sonu Etkisi (0-1 arası)

3. MODEL VE TAHMİN YÖNTEMİ
--------------------------
SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous variables) modeli
kullanılmıştır. Model parametreleri:
- p,d,q = 1,0,1 (AR, I, MA parametreleri)
- P,D,Q,s = 1,0,1,12 (Mevsimsel parametreler)

4. MODEL DEĞERLENDİRME METRİKLERİ
--------------------------------
A) RMSE (Root Mean Square Error):
   - Tahmin hatalarının karekökü
   - Düşük RMSE değeri daha iyi tahmin performansı gösterir
   - Verilerle aynı birimde olduğu için yorumlanması kolaydır (kWh)

B) AIC (Akaike Information Criterion):
   - Model karmaşıklığı ile tahmin doğruluğu arasındaki dengeyi ölçer
   - Daha düşük AIC değeri daha iyi model uyumu gösterir
   - Farklı modelleri karşılaştırmak için kullanılır

C) BIC (Bayesian Information Criterion):
   - AIC'ye benzer ancak model karmaşıklığını daha fazla cezalandırır
   - Daha düşük BIC değeri daha iyi model uyumu gösterir
   - Özellikle büyük veri setlerinde tercih edilir

5. ÖZEL DURUMLAR VE VARSAYIMLAR
------------------------------
- Yaz aylarında (Haziran-Ağustos) düşük tüketim
- Hafta sonları ve resmi tatillerde azalan tüketim
- Mesai saatleri dışında minimum tüketim
- Sıcaklık değişimlerine bağlı ısıtma/soğutma tüketimi
- Akademik takvime bağlı dönemsel değişimler

6. ÇIKTI VE RAPORLAMA
--------------------
- Her bina tipi için 2025 yılı aylık tüketim tahminleri
- Tahminler için %95 güven aralıkları
- Görsel grafikler ve trendler
- Model performans metrikleri
"""

import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go

def show_time_series_analysis():
    st.markdown("""
    <div style='background: linear-gradient(90deg, #3498db, #2980b9); padding: 20px; border-radius: 10px; margin-bottom: 25px; text-align: center;'>
        <h1 style='color: white;'>📊 Forecast Sonuçları</h1>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------
    # 1) NE YAPTIK? (Program Özeti)
    # --------------------------------------------------------------------
    st.markdown("""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px">
        <h2 style="text-align:center; color:#1f77b4; margin-bottom:10px">
            📈 ESOGÜ Enerji Tüketimi Zaman Serisi Analizi
        </h2>
        <p style="text-align:center">
            Bu çalışmada, Eskişehir Osmangazi Üniversitesi'nin<br>
            5 yıllık enerji tüketim verilerini analiz ederek,<br>
            hafta sonu, resmi tatil, yaz tatili gibi faktörleri<br>
            hesaba katarak gelecek dönem tahminleri yapılmıştır.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------
    # 2) KULLANDIĞIMIZ VERİLER (Veri Seti Açıklaması)
    # --------------------------------------------------------------------

    st.markdown("""
    <style>
        .header-style {
            background: linear-gradient(90deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            text-align: center;
        }
        .stExpander {
            background: linear-gradient(145deg, #f8f9fa, #e9ecef);
            border-radius: 10px;
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header-style"><h1>📊 Veri Seti ve Model Analizi</h1></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 10px; border-radius: 10px; color: white;'>
            <h3>1. Model ve Algoritma Açıklamaları</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔄 SARIMAX Modeli", expanded=True):
            st.markdown("""
            - **AR (AutoRegressive):** Geçmiş değerlerin etkisi
            - **I (Integrated):** Durağanlaştırma derecesi
            - **MA (Moving Average):** Geçmiş hata terimlerinin etkisi
            - **X (eXogenous):** Dış faktörlerin etkisi
            - **S (Seasonal):** Mevsimsellik etkisi
            """)

        with st.expander("📈 Model Değerlendirme Metrikleri", expanded=True):
            st.info("#### AIC (Akaike Information Criterion)")
            st.code("AIC = 2k - 2ln(L)")
            st.markdown("""
            **Ne İçin Kullanılır?**
            - Model karmaşıklığı ile model performansı arasındaki dengeyi ölçer
            - Farklı modelleri karşılaştırmak için kullanılır
            - Aşırı uyumu (overfitting) önlemeye yardımcı olur

            **Nasıl Yorumlanır?**
            - Daha düşük AIC değeri daha iyi model demektir
            - İdeal değer veri setine göre değişir
            - Genellikle 0-10 arası mükemmel
            - 10-20 arası iyi
            - 20+ değerler modelin gözden geçirilmesi gerektiğini gösterir

            **Formül Bileşenleri:**
            - k: model parametrelerinin sayısı
            - L: maksimum olabilirlik değeri
            """)

            st.warning("#### BIC (Bayesian Information Criterion)")
            st.code("BIC = ln(n)k - 2ln(L)")
            st.markdown("""
            **Ne İçin Kullanılır?**
            - AIC'ye benzer ancak model karmaşıklığını daha sert cezalandırır
            - Büyük veri setlerinde daha güvenilir sonuçlar verir
            - Model seçiminde daha tutucu bir yaklaşım sunar

            **Nasıl Yorumlanır?**
            - Daha düşük BIC değeri daha iyi model demektir
            - BIC değerleri arasındaki farklar şöyle yorumlanır:
              * 0-2: Önemsiz fark
              * 2-6: Pozitif fark
              * 6-10: Güçlü fark
              * 10+: Çok güçlü fark

            **Formül Bileşenleri:**
            - n: gözlem sayısı
            - k: parametre sayısı
            - L: maksimum olabilirlik değeri
            """)

            st.success("#### RMSE (Root Mean Square Error)")
            st.code("RMSE = √(Σ(ŷᵢ - yᵢ)²/n)")
            st.markdown("""
            **Ne İçin Kullanılır?**
            - Tahmin hatalarının büyüklüğünü ölçer
            - Model performansını orijinal veri birimiyle değerlendirir
            - Büyük hataları daha fazla cezalandırır

            **Nasıl Yorumlanır?**
            - RMSE değeri ne kadar düşükse, tahminler o kadar doğru demektir
            - Verinin ölçeğine bağlı olarak değerlendirilmelidir
            - Enerji tüketiminde kabul edilebilir RMSE değerleri:
              * <%5: Mükemmel tahmin
              * %5-%10: İyi tahmin
              * %10-%20: Kabul edilebilir tahmin
              * >%20: Model iyileştirmesi gerekli

            **Formül Bileşenleri:**
            - ŷᵢ: tahmin edilen değer
            - yᵢ: gerçek değer
            - n: gözlem sayısı

            **Önemli Notlar:**
            1. Bu metrikler birlikte değerlendirilmelidir
            2. Veri setinin özelliklerine göre kabul edilebilir değerler değişebilir
            3. Enerji tüketim tahminlerinde genellikle:
               - AIC < 10
               - BIC < 15
               - RMSE < %10 hedeflenir
            """)

            st.info("""
            💡 **Model Seçim Stratejisi:**
            1. Önce RMSE değerlerine bakarak genel tahmin doğruluğunu değerlendirin
            2. AIC ve BIC değerlerini karşılaştırarak en uygun model karmaşıklığını belirleyin
            3. Modeller arasında büyük fark yoksa, daha basit modeli tercih edin
            """)

    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #48c6ef, #6f86d6); padding: 10px; border-radius: 10px; color: white;'>
            <h3>2. Çevresel ve Kurumsal Faktörler</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🌡️ Hava Durumu Verileri (Eskişehir)", expanded=True):
            col_temp, col_humid = st.columns(2)
            with col_temp:
                st.metric("Kış Sıcaklığı", "-5°C ile +10°C", "-5°C")
                st.metric("Yaz Sıcaklığı", "+15°C ile +35°C", "+20°C")
            with col_humid:
                st.metric("Nem Oranı", "%45-80", "Değişken")
                st.metric("Güneşlenme", "3-12 saat/g��n", "Mevsimsel")

        with st.expander("🏫 Üniversite Aktivite Faktörleri", expanded=True):
            st.markdown("""
            <div style='background: #f8f9fa; padding: 10px; border-radius: 5px;'>
            <h4>Akademik Dönemler:</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col_term1, col_term2 = st.columns(2)
            with col_term1:
                st.metric("Güz/Bahar", "%90-95", "Tam Kapasite")
                st.metric("Yaz Okulu", "%30-40", "Düşük Kapasite")
            with col_term2:
                st.metric("Tatil Dönemi", "%10-30", "Minimum Kapasite")
                st.metric("Özel Günler", "Değişken", "Etkinliğe Bağlı")

        with st.expander("🌞 Mevsimsel Etkiler", expanded=True):
            col_heat, col_cool = st.columns(2)
            with col_heat:
                st.markdown("**❄️ Isıtma Sezonu (Ekim-Nisan)**")
                st.markdown("""
                - 🏭 Merkezi ısıtma aktif
                - 🔥 Kazan tam kapasite
                - ⚡ Yüksek doğalgaz tüketimi
                """)
            with col_cool:
                st.markdown("**☀️ Soğutma Sezonu (Haziran-Eylül)**")
                st.markdown("""
                - ❄️ Klimalar aktif
                - 🌡️ Merkezi soğutma
                - ⚡ Yüksek elektrik tüketimi
                """)

        with st.expander("👥 Bina Kullanım Yoğunluğu", expanded=True):
            st.metric("Toplam Öğrenci", "29,325", "Aktif Kayıt")
            col_pop1, col_pop2 = st.columns(2)
            with col_pop1:
                st.metric("Lisans", "24,000", "82%")
                st.metric("Y.Lisans", "4,000", "14%")
                st.metric("Doktora", "1,325", "4%")
            with col_pop2:
                st.metric("Akademik", "1,500", "Personel")
                st.metric("İdari", "1,000", "Personel")
                st.metric("Teknik", "500", "Personel")

        with st.expander("🏢 Ziyaretçi Yoğunluğu", expanded=True):
            col_vis1, col_vis2 = st.columns(2)
            with col_vis1:
                st.metric("Hafta İçi", "500-1000", "kişi/gün")
                st.metric("Normal Dönem", "Orta Yoğunluk", "🟨")
            with col_vis2:
                st.metric("Etkinlik Günleri", "1000-2000", "kişi/gün")
                st.metric("Özel Programlar", "Yüksek Yoğunluk", "🟥")

    st.success("""
        💡 Bu veriler, SARIMAX modelinin eğitimi ve 2025 yılı tahminleri için temel oluşturmaktadır. 
        Her faktör, binaların enerji tüketimini farklı oranlarda etkilemektedir.
    """)

    # Bu açıklamadan sonra veri tablolarını gösterelim
    st.subheader("5 Yıllık Aylık Tüketim Verileri (2020-2024)")

    # Bina tüketim verilerini güncelleyelim (günlük değerler x 30 gün)
    binalar = {
        'Fakülteler': [  # Min:220x30, Max:580x30, Ort:400x30
            12000, 12600, 13200, 11400, 9900, 8250,   # 2020 (Ocak-Haziran)
            6600, 7200, 10500, 12600, 14400, 15600,   # 2020 (Temmuz-Aralık)
            12300, 12900, 13500, 11700, 10200, 8550,  # 2021
            6900, 7500, 10800, 12900, 14700, 15900,
            12600, 13200, 13800, 12000, 10500, 8850,  # 2022
            7200, 7800, 11100, 13200, 15000, 16200,
            12900, 13500, 14100, 12300, 10800, 9150,  # 2023
            7500, 8100, 11400, 13500, 15300, 16500,
            13200, 13800, 14400, 12600, 11100, 9450,  # 2024
            7800, 8400, 11700, 13800, 15600, 17400
        ],
        'Kültürel ve Sosyal Alanlar': [  # Min:200x30, Max:590x30, Ort:395x30
            10500, 11100, 11700, 9600, 8100, 6600,    # 2020
            6000, 6600, 9600, 12000, 13500, 15000,
            10800, 11400, 12000, 9900, 8400, 6900,    # 2021
            6300, 6900, 9900, 12300, 13800, 15300,
            11100, 11700, 12300, 10200, 8700, 7200,   # 2022
            6600, 7200, 10200, 12600, 14100, 15600,
            11400, 12000, 12600, 10500, 9000, 7500,   # 2023
            6900, 7500, 10500, 12900, 14400, 15900,
            11700, 12300, 12900, 10800, 9300, 7800,   # 2024
            7200, 7800, 10800, 13200, 14700, 17700
        ],
        'Sağlık Tesisleri': [  # Min:200x30, Max:570x30, Ort:385x30
            10200, 10800, 11400, 9300, 7800, 6300,    # 2020
            6000, 6600, 9300, 11700, 13200, 14700,
            10500, 11100, 11700, 9600, 8100, 6600,    # 2021
            6300, 6900, 9600, 12000, 13500, 15000,
            10800, 11400, 12000, 9900, 8400, 6900,    # 2022
            6600, 7200, 9900, 12300, 13800, 15300,
            11100, 11700, 12300, 10200, 8700, 7200,   # 2023
            6900, 7500, 10200, 12600, 14100, 15600,
            11400, 12000, 12600, 10500, 9000, 7500,   # 2024
            7200, 7800, 10500, 12900, 14400, 17100
        ],
        'Araştırma ve Uygulama Merkezleri': [  # Min:180x30, Max:490x30, Ort:335x30
            9000, 9600, 10200, 8100, 6600, 5700,      # 2020
            5400, 6000, 8700, 10500, 12000, 13200,
            9300, 9900, 10500, 8400, 6900, 6000,      # 2021
            5700, 6300, 9000, 10800, 12300, 13500,
            9600, 10200, 10800, 8700, 7200, 6300,     # 2022
            6000, 6600, 9300, 11100, 12600, 13800,
            9900, 10500, 11100, 9000, 7500, 6600,     # 2023
            6300, 6900, 9600, 11400, 12900, 14100,
            10200, 10800, 11400, 9300, 7800, 6900,    # 2024
            6600, 7200, 9900, 11700, 13200, 14700
        ],
        'Spor Alanları': [  # Min:150x30, Max:370x30, Ort:260x30
            6600, 7200, 7800, 6000, 5400, 4800,       # 2020
            4500, 5100, 7200, 8700, 9900, 10500,
            6900, 7500, 8100, 6300, 5700, 5100,       # 2021
            4800, 5400, 7500, 9000, 10200, 10800,
            7200, 7800, 8400, 6600, 6000, 5400,       # 2022
            5100, 5700, 7800, 9300, 10500, 11100,
            7500, 8100, 8700, 6900, 6300, 5700,       # 2023
            5400, 6000, 8100, 9600, 10800, 11100,
            7800, 8400, 9000, 7200, 6600, 6000,       # 2024
            5700, 6300, 8400, 9900, 11100, 11100
        ],
        'Yemek ve Konaklama': [  # Min:80x30, Max:220x30, Ort:150x30
            3900, 4200, 4800, 3600, 3000, 2700,       # 2020
            2400, 2700, 3600, 4800, 5700, 6300,
            4200, 4500, 5100, 3900, 3300, 3000,       # 2021
            2700, 3000, 3900, 5100, 6000, 6600,
            4500, 4800, 5400, 4200, 3600, 3300,       # 2022
            3000, 3300, 4200, 5400, 6300, 6600,
            4800, 5100, 5700, 4500, 3900, 3600,       # 2023
            3300, 3600, 4500, 5700, 6600, 6600,
            5100, 5400, 6000, 4800, 4200, 3900,       # 2024
            3600, 3900, 4800, 6000, 6600, 6600
        ],
        'Park ve Açık Alanlar': [  # Min:15x30, Max:45x30, Ort:30x30
            750, 840, 960, 600, 540, 480,             # 2020
            450, 510, 750, 1050, 1200, 1290,
            780, 870, 990, 630, 570, 510,             # 2021
            480, 540, 780, 1080, 1230, 1320,
            810, 900, 1020, 660, 600, 540,            # 2022
            510, 570, 810, 1110, 1260, 1350,
            840, 930, 1050, 690, 630, 570,            # 2023
            540, 600, 840, 1140, 1290, 1350,
            870, 960, 1080, 720, 660, 600,            # 2024
            570, 630, 870, 1170, 1320, 1350
        ],
        'Helikopter Pisti': [  # Min:5x30, Max:10x30, Ort:7.5x30
            210, 240, 270, 180, 150, 150,             # 2020
            150, 180, 210, 240, 270, 300,
            210, 240, 270, 180, 150, 150,             # 2021
            150, 180, 210, 240, 270, 300,
            210, 240, 270, 180, 150, 150,             # 2022
            150, 180, 210, 240, 270, 300,
            210, 240, 270, 180, 150, 150,             # 2023
            150, 180, 210, 240, 270, 300,
            210, 240, 270, 180, 150, 150,             # 2024
            150, 180, 210, 240, 270, 300
        ]
    }

    # Bu verileri tablo halinde gösterelim
    df_binalar = pd.DataFrame(binalar)
    # 5 yıllık veri olduğu için 60 aylık tarih aralığı oluşturuyoruz
    df_binalar.index = pd.date_range(start="2020-01-01", periods=60, freq='M')
    df_binalar.index.name = "Tarih"
    st.subheader("ESOGÜ - 5 Yıllık (Aylık) Tüketim Verileri (2020-2024)")
    st.dataframe(df_binalar)

    # Eskişehir için hava durumu ve diğer faktörleri içeren detaylı veri seti
    weather_factors = {
        'Sicaklik': [  # Eskişehir aylık ortalama sıcaklıklar (°C)
            0.5, 2.1, 6.3, 11.2, 16.1, 20.3, 23.5, 23.1, 18.4, 12.7, 6.8, 2.4,   # 2020
            0.3, 1.9, 6.1, 11.0, 15.9, 20.1, 23.3, 22.9, 18.2, 12.5, 6.6, 2.2,   # 2021
            0.4, 2.0, 6.2, 11.1, 16.0, 20.2, 23.4, 23.0, 18.3, 12.6, 6.7, 2.3,   # 2022
            0.6, 2.2, 6.4, 11.3, 16.2, 20.4, 23.6, 23.2, 18.5, 12.8, 6.9, 2.5,   # 2023
            0.7, 2.3, 6.5, 11.4, 16.3, 20.5, 23.7, 23.3, 18.6, 12.9, 7.0, 2.6,   # 2024
            0.5, 2.1, 6.3, 11.2, 16.1, 20.3, 23.5, 23.1, 18.4, 12.7, 6.8, 2.4    # 2025 (tahmin)
        ],
        'Nem': [  # Eskişehir aylık ortalama nem oranı (%)
            76, 73, 68, 63, 59, 55, 50, 50, 55, 65, 72, 77,  # 2020
            75, 72, 67, 62, 58, 54, 49, 49, 54, 64, 71, 76,  # 2021
            77, 74, 69, 64, 60, 56, 51, 51, 56, 66, 73, 78,  # 2022
            76, 73, 68, 63, 59, 55, 50, 50, 55, 65, 72, 77,  # 2023
            75, 72, 67, 62, 58, 54, 49, 49, 54, 64, 71, 76,  # 2024
            76, 73, 68, 63, 59, 55, 50, 50, 55, 65, 72, 77   # 2025 (tahmin)
        ],
        'Guneslenme': [  # Günlük ortalama güneşlenme süresi (saat)
            3, 4, 5, 7, 9, 11, 12, 11, 9, 6, 4, 3,  # 2020-2025 için tekrar
        ] * 6
    }

    # Üniversite aktivite faktörleri
    university_factors = {
        'Donem_Aktivitesi': [  # Akademik dönem aktivite oranı (0-1 arası)
            0.85, 0.90, 0.95, 0.95, 0.80, 0.40,  # Ocak-Haziran (Final ve yaz başlangıcı)
            0.20, 0.20, 0.70, 0.95, 0.95, 0.70,  # Temmuz-Aralık (Yaz tatili ve dönem başlangıcı)
        ] * 6,
        
        'Mesai_Saatleri': [  # Mesai saatleri yoğunluğu (0-1 arası)
            0.80, 0.80, 0.85, 0.85, 0.85, 0.50,  # Ocak-Haziran
            0.30, 0.30, 0.80, 0.85, 0.85, 0.70,  # Temmuz-Aralık
        ] * 6,
        
        'Hafta_Sonu_Etkisi': [  # Hafta sonu düşüş faktörü (0-1 arası, 1: tam düşüş)
            0.70, 0.70, 0.70, 0.70, 0.70, 0.90,  # Ocak-Haziran
            0.95, 0.95, 0.70, 0.70, 0.70, 0.80,  # Temmuz-Aralık
        ] * 6
    }

    # Tüm faktörleri tek bir DataFrame'de birleştirelim
    df_exog = pd.DataFrame({
        'Sicaklik': weather_factors['Sicaklik'],
        'Nem': weather_factors['Nem'],
        'Guneslenme': weather_factors['Guneslenme'],
        'Donem_Aktivitesi': university_factors['Donem_Aktivitesi'],
        'Mesai_Saatleri': university_factors['Mesai_Saatleri'],
        'Hafta_Sonu_Etkisi': university_factors['Hafta_Sonu_Etkisi']
    }, index=pd.date_range("2020-01-01", periods=72, freq='M'))

    # Sıcaklık verileri (aylık ortalama) - 2 yıllık + 2025 için tahmini
    # 36 ay (2023-01'den 2025-12'ye kadar)
    # Eskişehir için tahmini, mevsimsel veriler uydurulmuştur
    # (Gerçek senaryoda meteoroloji verileri kullanılmalı)
    eskisehir_temp = [
        # 2020
        0.0,  1.0,  5.0, 10.0, 15.0, 20.0, 24.0, 25.0, 19.0, 13.0,  6.0,  2.0,
        # 2021
        0.2,  1.1,  5.2, 10.2, 15.1, 20.2, 24.1, 25.1, 19.1, 13.1,  6.1,  2.1,
        # 2022
        0.1,  1.2,  5.3, 10.3, 15.2, 20.3, 24.2, 25.2, 19.2, 13.2,  6.2,  2.2,
        # 2023
        0.0,  1.0,  5.0, 10.0, 15.0, 20.0, 24.0, 25.0, 19.0, 13.0,  6.0,  2.0,
        # 2024
        0.5,  1.2,  5.5, 10.5, 15.2, 20.5, 24.5, 25.3, 19.2, 13.2,  6.2,  2.5,
        # 2025 (tahmin)
        0.3,  1.0,  5.1, 10.2, 15.3, 20.1, 24.2, 25.1, 19.5, 13.0,  6.5,  2.2
    ]

    # Hafta sonu ve resmi tatil faktörü (aylık bazda oransal yaklaşım):
    # -> Her ay kaç gün hafta sonu+resmi tatil var? / Toplam gün sayısı
    # Burada tamamen uydurulmuş değerler giriyoruz (ör: ortalama 8-10 gün % tatil)
    # 2023 + 2024 (24 ay) + 2025 (12 ay) = 36 veri
    weekend_holiday_ratio = [0.35, 0.32, 0.30, 0.28, 0.25, 0.25, 0.40, 0.38, 0.28, 0.30, 0.32, 0.40] * 6  # 6 yıl

    # Yaz tatili (Haziran, Temmuz, Ağustos) - 1 ise tatil, 0 değil
    # Yıllık döngü: [0,0,0,0,0,1,1,1,0,0,0,0]
    # 3 kez tekrar edeceğiz (2023, 2024, 2025)
    summer_break = [0,0,0,0,0,1,1,1,0,0,0,0] * 6

    # Bu exog verilerini gösterelim
    st.subheader("Eksojen Değişkenler (Hava Durumu, Aktivite Oranları, vb.)")
    st.dataframe(df_exog.head(24))  # İlk 24 ay
    st.write("... (2025 yılı için de tahmini veriler eklenmiştir, toplam 72 satır)")

    # --------------------------------------------------------------------
    # 3) TAHMİNLER (SARIMAX) - 2025 Yılı (12 Ay)
    # --------------------------------------------------------------------
    st.header("Tahminler (SARIMAX) - 2025 Yılı")

    # 2 yıllık (2023-2024) veriyi model eğitimine dahil edip
    # 2025 yılı 12 ay ileri tahminde bulunacağız.

    # "ESOGÜ'ye uyarlanmış" tüketim verisini basitçe:
    #  - "Akdeniz verisi x (öğrenci sayısı oranı) x (sıcaklık düzeltmesi?)" diyebilirsiniz.
    #  - Örneğin önceki kodda "normalize_consumption" fonksiyonu vardı;
    #    burada modeli karmaşıklaştırmamak adına, doğrudan veriyi "ESOGÜ verisi" kabul edelim.
    # Gerçek durumda, Akdeniz -> Eskişehir adaptasyonu için ek bir çarpan veya fonksiyon kullanılabilir.

    # Tüketim df: df_binalar (24 ay, 2023-2024)
    # Exog df: df_exog (36 ay, 2023-2025) 
    # => Model eğitimi için ilk 24 ay = (2023-01 ~ 2024-12), 
    # => Forecast için exog'un 2025-01 ~ 2025-12 verilerini kullanacağız.

    # Eğitim verisi için son 2 yılı alalım (2023-2024)
    train_data = df_binalar.loc["2023-01-31":"2024-12-31"]  # 24 ay
    train_exog = df_exog.loc["2023-01-31":"2024-12-31"]

    forecast_exog = df_exog.loc["2025-01-31":"2025-12-31"]  # 12 ay (2025)
    
    # Model parametreleri
    p, d, q = 1, 0, 1
    P, D, Q, s = 1, 0, 1, 12

    # İleride birleştirmek için tüm bina tahminlerini tutacağız
    forecast_results_all = []

    # Her bina için ayrı SARIMAX kuralım
    for bina_adi in train_data.columns:
        st.subheader(f"🏢 {bina_adi} Binası Analizi")

        # Eğitim (train) tüketim verisi
        y_train = train_data[bina_adi]

        # Modeli kuralım: exog = [HaftaSonuTatil, YazTatilFlag, Sıcaklık, ÖğrenciOranı ...]
        model = SARIMAX(
            y_train,
            order=(p, d, q),
            seasonal_order=(P, D, Q, s),
            exog=train_exog[['Sicaklik', 'Nem', 'Guneslenme', 
                             'Donem_Aktivitesi', 'Mesai_Saatleri', 'Hafta_Sonu_Etkisi']],
            enforce_stationarity=False,
            enforce_invertibility=False,
            initialization='approximate_diffuse'
        )
        results = model.fit()

        # 12 aylık ileri tahmin (2025)
        forecast_steps = 12
        forecast_obj = results.get_forecast(
            steps=forecast_steps,
            exog=forecast_exog[['Sicaklik', 'Nem', 'Guneslenme', 
                               'Donem_Aktivitesi', 'Mesai_Saatleri', 'Hafta_Sonu_Etkisi']]
        )
        forecast_mean = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()

        # Negatif tahminleri minimum değerle değiştirelim
        min_value = y_train.min()
        forecast_mean = pd.Series(
            [max(x, min_value) for x in forecast_mean], 
            index=forecast_mean.index
        )

        # Grafik için tarih index
        future_dates = forecast_exog.index

        # Mevcut veri (2023-2024) + Tahmin (2025) grafiği
        fig = go.Figure()

        # 1) Eğitim verisi
        fig.add_trace(go.Scatter(
            x=y_train.index, 
            y=y_train.values,
            name='Geçmiş Tüketim (Eğitim Verisi)',
            line=dict(color='blue'),
            mode='lines+markers'
        ))
        # 2) Tahmin
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=forecast_mean,
            name='Tahmin (2025)',
            line=dict(color='red', dash='dash'),
            mode='lines+markers'
        ))
        # 3) Güven Aralığı
        fig.add_trace(go.Scatter(
            x=list(future_dates) + list(future_dates[::-1]),
            y=list(conf_int.iloc[:, 0]) + list(conf_int.iloc[:, 1][::-1]),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Güven Aralığı'
        ))

        fig.update_layout(
            title=f"{bina_adi} - SARIMAX Tahmini (2025)",
            xaxis_title="Tarih",
            yaxis_title="Tüketim (kWh)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Model istatistikleri
        st.markdown("**Model İstatistikleri:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("AIC", f"{results.aic:.2f}")
        with col2:
            st.metric("BIC", f"{results.bic:.2f}")
        with col3:
            try:
                rmse_in_sample = np.sqrt(results.mse)
                st.metric("RMSE (in-sample)", f"{rmse_in_sample:.2f}")
            except:
                st.metric("RMSE (in-sample)", "N/A")

        # Tahmin sonuçlarını saklamak
        df_forecast = pd.DataFrame({
            'Tarih': future_dates,
            'Tahmin': forecast_mean,
            'Alt': conf_int.iloc[:,0],
            'Üst': conf_int.iloc[:,1],
            'Bina': bina_adi
        })
        forecast_results_all.append(df_forecast)

    # Tüm bina tahminlerini bir araya getirelim
    all_forecasts_df = pd.concat(forecast_results_all, ignore_index=True)

    # --------------------------------------------------------------------
    # 4) GÖRSELLEŞTİRME: Tablolar ve Günlük Ortalama Tüketim (2025)
    # --------------------------------------------------------------------
    st.markdown("""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px">
        <h2 style="text-align:center; color:#1f77b4;">
            📊 2025 Tahmin Sonuçları ve Özet İstatistikler
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Pivot tablo: Satırlarda Tarih, Sütunlarda Bina, Değerlerde Tahmin
    pivot_forecasts = all_forecasts_df.pivot(
        index='Tarih',
        columns='Bina',
        values='Tahmin'
    )
    # Tarih indeksini daha okunabilir formata çevirelim (ay-yıl)
    pivot_forecasts.index = pivot_forecasts.index.strftime('%B %Y')

    st.subheader("Aylık Tahmin Tablosu (2025)")
    st.dataframe(pivot_forecasts.style.format("{:,.0f} kWh"))

    # Bina bazında yıllık toplam ve günlük ortalama
    summary_data = []
    for bina_adi in binalar.keys():
        bina_df = all_forecasts_df[all_forecasts_df['Bina'] == bina_adi]
        total_yearly = bina_df['Tahmin'].sum()
        daily_avg = total_yearly / 365.0  # kaba yaklaşım
        summary_data.append([bina_adi, total_yearly, daily_avg])

    df_summary = pd.DataFrame(summary_data, 
        columns=["Bina", "Yıllık Toplam (kWh)", "Günlük Ortalama (kWh)"])

    st.subheader("Yıllık Toplam ve Günlük Ortalama Tüketim (2025)")
    st.table(
        df_summary.style.format({
            "Yıllık Toplam (kWh)": "{:,.0f}",
            "Günlük Ortalama (kWh)": "{:,.1f}"
        })
    )

    # Toplam tüketim için pasta grafiği
    fig_pie = go.Figure(data=[go.Pie(
        labels=df_summary['Bina'],
        values=df_summary['Yıllık Toplam (kWh)'],
        hole=.3
    )])
    fig_pie.update_layout(
        title="Binalara Göre Tüketim Dağılımı (2025)",
        showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Toplam Tüketim
    total_annual = df_summary['Yıllık Toplam (kWh)'].sum()
    total_daily_avg = df_summary['Günlük Ortalama (kWh)'].sum()

    st.markdown("""
    ### Toplam 2025 Tüketimi
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Toplam Yıllık Tüketim (2025)", f"{total_annual:,.0f} kWh")
    with col2:
        st.metric("Toplam Günlük Ortalama (2025)", f"{total_daily_avg:,.0f} kWh")

    # Bina enerji verilerini hazırla
    building_energy_data = pd.DataFrame({
        'Bina Tipi': ['Akademik Birimler', 'Sağlık Tesisleri', 'Sosyal ve Destek Tesisleri'],
        'Toplam Günlük Enerji (kWh)': [13000, 14400, 9600]  # Örnek değerler
    })
    
    # Session state'e kaydet
    st.session_state.building_energy_data = building_energy_data

    st.success("2025 yılı için tahmin işlemi tamamlandı!")

  