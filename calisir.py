# calisir.py

import streamlit as st
from PIL import Image

def render_variable_with_explanation(variable_latex, explanation):
    """
    LaTeX ile değişkeni ve açıklamasını yan yana göstermek için yardımcı fonksiyon.
    
    Args:
        variable_latex (str): LaTeX formatında değişken ifadesi.
        explanation (str): Değişkenin açıklaması.
    """
    col1, col2 = st.columns([1, 3])
    with col1:
        st.latex(variable_latex)
    with col2:
        st.markdown(f"**{explanation}**")

def program_nasil_calisir():
    """Program çalışma mantığını ve formülleri gösterir."""
    st.header("Program Nasıl Çalışır?")
    
    # Genel Çalışma Mantığı
    st.subheader("🔄 Genel Çalışma Mantığı")
    st.markdown("""
    1. **Veri Girişi ve Validasyon**
       - Konum bilgileri (enlem, boylam)
       - Panel özellikleri (güç, verim, sayı)
       - Çevresel koşullar (sıcaklık, ışınım)
       - Bina tüketim verileri
       
    2. **Hesaplama Aşamaları**
       - Güneş geometrisi hesaplamaları
       - Panel performans analizi
       - Enerji üretim tahmini
       - Finansal analiz
       - Karbon ayak izi hesabı
    """)

    # Güneş Paneli Formülleri
    st.subheader("☀️ Güneş Paneli Formülleri")
    
    # 1. Güneş Sapma Açısı
    st.markdown("#### 1. Güneş Sapma Açısı (δ)")
    st.latex(r'''
    \delta = 23.5 \times \sin\left(\frac{360}{365} \times (284 + n)\right)
    ''')
    st.markdown("""
    - n: Yılın günü (1-365)
    - δ: Güneş sapma açısı (°)
    """)

    # 2. Optimum Panel Açısı
    st.markdown("#### 2. Optimum Panel Açısı (β)")
    st.latex(r'''
    \beta = 1.3793 + \phi \times (1.2011 + \phi \times (-0.014404 + \phi \times 0.000080509))
    ''')
    st.markdown("""
    - φ: Enlem (°)
    - β: Optimum panel açısı (°)
    """)

    # 3. Panel Sıcaklığı
    st.markdown("#### 3. Panel Sıcaklığı (Tc)")
    st.latex(r'''
    T_c = 30 + 0.0175 \times (G_g - 300) + 1.14 \times (T_a - 25)
    ''')
    st.markdown("""
    - Gg: Günlük ışınım (W/m²)
    - Ta: Hava sıcaklığı (°C)
    - Tc: Panel sıcaklığı (°C)
    """)

    # 4. Panel Verimi
    st.markdown("#### 4. Panel Verimi (η)")
    st.latex(r'''
    \eta = \frac{P_{nominal}}{A_{panel} \times G_{ref}}
    ''')
    st.markdown("""
    - Pnominal: Panel nominal gücü (W)
    - Apanel: Panel alanı (m²)
    - Gref: Referans ışınım (1000 W/m²)
    """)

    # 5. Sistem Performans Oranı
    st.markdown("#### 5. Sistem Performans Oranı (PR)")
    st.latex(r'''
    PR = \eta_{base} \times (1 + k_T \times \Delta T) \times f_{soiling} \times f_{shading}
    ''')
    st.markdown("""
    - ηbase: Temel panel verimi
    - kT: Sıcaklık katsayısı (%/°C)
    - ΔT: Sıcaklık farkı (°C)
    - fsoiling: Kirlenme faktörü
    - fshading: Gölgelenme faktörü
    """)

    # Finansal Formüller
    st.subheader("💰 Finansal Formüller")
    
    # 1. Toplam Yatırım Maliyeti
    st.markdown("#### 1. Toplam Yatırım Maliyeti")
    st.latex(r'''
    C_{total} = (N_{panel} \times C_{panel}) \times (1 + KDV) + C_{installation}
    ''')
    st.markdown("""
    - Npanel: Panel sayısı
    - Cpanel: Panel birim fiyatı
    - KDV: Katma değer vergisi oranı
    - Cinstallation: Kurulum maliyeti
    """)

    # 2. Yıllık Enerji Üretimi
    st.markdown("#### 2. Yıllık Enerji Üretimi")
    st.latex(r'''
    E_{annual} = \sum_{i=1}^{12} (P_{max} \times H_i \times N_i \times PR)
    ''')
    st.markdown("""
    - Pmax: Maksimum güç
    - Hi: Aylık ortalama günlük ışınım
    - Ni: Aydaki gün sayısı
    - PR: Performans oranı
    """)

    # 3. Geri Ödeme Süresi
    st.markdown("#### 3. Geri Ödeme Süresi")
    st.latex(r'''
    T_{payback} = \frac{C_{total}}{S_{annual}}
    ''')
    st.markdown("""
    - Ctotal: Toplam yatırım maliyeti
    - Sannual: Yıllık tasarruf
    """)

    # 4. Net Bugünkü Değer
    st.markdown("#### 4. Net Bugünkü Değer (NPV)")
    st.latex(r'''
    NPV = -C_{total} + \sum_{t=1}^{n} \frac{CF_t}{(1 + r)^t}
    ''')
    st.markdown("""
    - CFt: t yılındaki nakit akışı
    - r: İskonto oranı
    - n: Proje ömrü
    """)

    # Enerji Dengesi Formülleri
    st.subheader("⚡ Enerji Dengesi Formülleri")
    
    # 1. Enerji Fazlası/Eksiği
    st.markdown("#### 1. Enerji Fazlası/Eksiği")
    st.latex(r'''
    E_{net} = (E_{production} \times \eta_{system}) - E_{consumption}
    ''')
    st.markdown("""
    - Eproduction: Panel üretimi
    - ηsystem: Sistem verimi
    - Econsumption: Bina tüketimi
    """)

    # 2. Net Maliyet/Kazanç
    st.markdown("#### 2. Net Maliyet/Kazanç")
    st.latex(r'''
    C_{net} = \begin{cases} 
    E_{net} \times T_{sell} & \text{if } E_{net} > 0 \\
    E_{net} \times T_{buy} & \text{if } E_{net} < 0
    \end{cases}
    ''')
    st.markdown("""
    - Enet: Net enerji farkı
    - Tsell: Satış tarifesi
    - Tbuy: Alış tarifesi
    """)

    # Program Özellikleri
    st.subheader("🔧 Program Özellikleri")
    st.markdown("""
    - **Detaylı Analiz:** Güneş paneli, bina tüketimi ve finansal analizler
    - **Görselleştirme:** İnteraktif grafikler ve tablolar
    - **Raporlama:** Detaylı PDF raporu oluşturma
    - **Veri Dışa Aktarma:** CSV formatında veri aktarımı
    - **Optimizasyon:** Panel açısı ve sistem boyutlandırma
    """)

    # Önemli Notlar
    st.warning("""
    ⚠️ **Önemli Notlar:**
    1. Tüm hesaplamalar teorik değerler üzerine kuruludur
    2. Gerçek performans çevresel faktörlere göre değişebilir
    3. Finansal projeksiyonlar tahmini değerlerdir
    4. Düzenli bakım ve kontrol önemlidir
    5. Sistem tasarımı için profesyonel destek alınmalıdır
    """)




