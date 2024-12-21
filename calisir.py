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
    """
    "Program Nasıl Çalışır" sekmesinin içeriğini render eder.
    """
    # ==========================================
    # Başlık ve Giriş
    # ==========================================
    st.header("Program Nasıl Çalışır?")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
    Bu uygulama, güneş enerjisi sistemlerinin analizi ve bina enerji tüketiminin optimizasyonu için geliştirilmiş kapsamlı bir araçtır.
    </div>
    """, unsafe_allow_html=True)

    # Ana Adımlar
    st.subheader("🔄 Ana İşlem Adımları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Veri Girişi ve Validasyon
        - **Konum Bilgileri:**
          - Enlem ve boylam koordinatları
          - Rakım değeri
          - Bölgesel iklim verileri
        
        - **Panel Özellikleri:**
          - Panel tipi ve markası
          - Nominal güç değerleri
          - Verimlilik katsayıları
          - Montaj açısı ve yönü
        
        - **Bina Parametreleri:**
          - Yapı tipi ve yaşı
          - Kullanım amacı
          - Toplam kullanım alanı
          - Mevcut enerji tüketimi
        """)
        
        st.markdown("""
        ### 2️⃣ Teknik Hesaplamalar
        - **Güneş Geometrisi:**
          - Güneş sapma açısı
          - Zenit açısı
          - Azimut açısı
          - Optimum panel eğimi
        
        - **Enerji Üretimi:**
          - Saatlik üretim tahminleri
          - Günlük toplam üretim
          - Aylık ve yıllık projeksiyonlar
          - Kayıp faktörleri analizi
        """)

    with col2:
        st.markdown("""
        ### 3️⃣ Performans Analizi
        - **Sistem Verimliliği:**
          - Panel sıcaklık etkileri
          - Gölgelenme kayıpları
          - İnverter verimliliği
          - Kablo kayıpları
        
        - **Çevresel Faktörler:**
          - Mevsimsel değişimler
          - Hava durumu etkileri
          - Kirlilik faktörleri
          - Bakım gereksinimleri
        """)
        
        st.markdown("""
        ### 4️⃣ Ekonomik Değerlendirme
        - **Maliyet Analizi:**
          - Başlangıç yatırım maliyeti
          - İşletme giderleri
          - Bakım maliyetleri
          - Yedek parça giderleri
        
        - **Finansal Projeksiyon:**
          - Geri ödeme süresi
          - Net bugünkü değer (NPV)
          - İç verim oranı (IRR)
          - Yıllık tasarruf miktarı
        """)

    # Görselleştirme ve Raporlama
    st.subheader("📊 Görselleştirme ve Raporlama")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("""
        **Görsel Çıktılar:**
        - İnteraktif performans grafikleri
        - Aylık üretim-tüketim karşılaştırmaları
        - Sıcaklık ve verim ilişki grafikleri
        - Finansal projeksiyon göstergeleri
        """)
        
    with col4:
        st.success("""
        **Raporlama Özellikleri:**
        - Detaylı PDF raporu
        - CSV formatında veri dışa aktarımı
        - Özelleştirilebilir rapor şablonları
        - Karşılaştırmalı analiz tabloları
        """)

    # Sistem Gereksinimleri
    st.subheader("⚙️ Sistem Gereksinimleri ve Öneriler")
    st.warning("""
    - **Tarayıcı:** Modern bir web tarayıcısı (Chrome, Firefox, Safari)
    - **İnternet Bağlantısı:** Minimum 1 Mbps
    - **Ekran Çözünürlüğü:** En az 1280x720 piksel
    - **Tavsiye Edilen:** Masaüstü veya dizüstü bilgisayar kullanımı
    """)

    # Kullanım İpuçları
    st.subheader("💡 Kullanım İpuçları")
    st.markdown("""
    1. Tüm veri girişlerini dikkatli ve eksiksiz yapın
    2. Hesaplama sonuçlarını karşılaştırmalı olarak değerlendirin
    3. Farklı senaryo analizleri için parametreleri değiştirerek tekrar hesaplayın
    4. Sonuçları kaydetmeyi unutmayın
    5. Önemli değişiklikleri not alın
    """)

    # ==========================================
    # Kullanılan Veriler
    # ==========================================
    st.header("Kullanılan Veriler")
    st.markdown("""
    Bu analiz için aşağıdaki veriler kullanılmıştır:
    - **Aylık Güneş Radyasyonu (Global Işınım):** Her ay için ortalama güneş radyasyonu değerleri (W/m²).
    - **Gün Işıklama Süreleri:** Her ay için ortalama gün ışığı süresi (saat).
    - **Ortalama Hava Sıcaklıkları:** Her ay için ortalama hava sıcaklıkları (°C).
    - **Bina Tipleri ve Enerji Tüketimleri:** Farklı bina tipleri için adetleri ve yıllık ortalama enerji tüketimleri (kWh).
    """)

    # ==========================================
    # Görsellerin Yüklenmesi
    # ==========================================
    st.header("Kullanılan Veri kaynakları")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            image1 = Image.open("images/eskişehir_radyasyon.png")
            st.image(image1, caption="Eskişehir Global Radyasyon Değerleri", use_container_width=True)
        except FileNotFoundError:
            st.error("Eskişehir Global Radyasyon Değerleri görseli bulunamadı.")
    
    with col2:
        try:
            image2 = Image.open("images/eskişehir_gunesleme.png")
            st.image(image2, caption="Eskişehir Güneşlenme Süresi (saat)", use_container_width=True)
        except FileNotFoundError:
            st.error("Eskişehir Güneşlenme Süresi görseli bulunamadı.")
    
    with col3:
        try:
            image3 = Image.open("images/eskişehir_hava_sicakligi.png")
            st.image(image3, caption="Ortalama Hava Sıcaklığı (mgm.gov.tr)", use_container_width=True)
        except FileNotFoundError:
            st.error("Ortalama Hava Sıcaklığı görseli bulunamadı.")

    # ==========================================
    # Kullanılan Formüller ve Uygulamaları
    # ==========================================
    st.header("📐 Kullanılan Formüller ve Hesaplama Yöntemleri")
    
    st.info("""
    Bu bölümde, güneş enerjisi sistemlerinin tasarımında ve performans analizinde kullandığımız 
    temel formüller ve bunların pratik uygulamaları açıklanmaktadır.
    """)

    # 1. Güneş Sapma Açısı
    st.subheader("1️⃣ Güneş Sapma Açısı (δ)")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        \delta = 23.5 \times \sin\left(\frac{360}{365} \times (284 + n)\right)
        ''')
        st.markdown("""
        **Parametreler:**
        - n: Yılın günü (1-365)
        - δ: Güneş sapma açısı (°)
        """)
    
    with col2:
        st.success("""
        **📌 Pratik Uygulama:**
        1. 21 Haziran (n=172) için:
           - δ ≈ +23.5° (En yüksek değer)
        2. 21 Aralık (n=355) için:
           - δ ≈ -23.5° (En düşük değer)
        3. 21 Mart ve 23 Eylül için:
           - δ ≈ 0° (Ekinoks)
        """)

    st.subheader("2️⃣ Yıllık Optimum Panel Açısı (θ)")
    
    # Önce formülü göster
    st.latex(r'''
    \theta = 1.3793 + \text{Enlem} \times (1.2011 + \text{Enlem} \times (-0.014404 + \text{Enlem} \times 0.000080509))
    ''')
    
    st.markdown("""
    **Parametreler:**
    - Enlem: Lokasyon enlemi (°)
    - θ: Yıllık optimum panel açısı (°)
    """)
    
    # Örnek hesaplamayı ayrı bir bölümde göster
    st.markdown("---")  # Ayırıcı çizgi ekle
    st.markdown("#### 📌 Örnek Hesaplama")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("""
        **Eskişehir için (Enlem: 39.78°):**
        1. θ = 1.3793 + 39.78 × (1.2011 + ...)
        2. θ ≈ 33° (Yıllık optimum açı)
        """)
    
    with col2:
        st.success("""
        **🔍 Mevsimsel Ayarlama:**
        - Yaz: θ - 15°
        - Kış: θ + 15°
        """)
    # 3. Ortalama Günlük Işınım
    st.subheader("3️⃣ Ortalama Günlük Işınım (Gg)")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        G_g = \frac{\sum G_i}{\sum \Delta t_i} \times 1000
        ''')
        st.markdown("""
        **Parametreler:**
        - Gi: Saatlik ışınım (kWh/m²)
        - Δti: Zaman aralığı (saat)
        - Gg: Günlük ışınım (W/m²)
        """)
    
    with col2:
        st.success("""
        **📌 Örnek Analiz:**
        6 saatlik ölçüm için:
        1. Gi değerleri: [0.5, 0.8, 0.9, 0.7, 0.4, 0.2] kWh/m²
        2. Toplam süre: 6 saat
        3. Gg = (3.5 ÷ 6) × 1000 = 583.33 W/m²
        """)

    # 4. Panel Sıcaklığı
    st.subheader("4️⃣ Panel Sıcaklığı (Tc)")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        T_c = 30 + 0.0175 \times (G_g - 300) + 1.14 \times (T_a - 25)
        ''')
        st.markdown("""
        **Parametreler:**
        - Gg: Günlük ışınım (W/m²)
        - Ta: Hava sıcaklığı (°C)
        - Tc: Panel sıcaklığı (°C)
        """)
    
    with col2:
        st.success("""
        **📌 Örnek Hesaplama:**
        Veriler:
        - Gg = 800 W/m²
        - Ta = 30°C
        
        Hesaplama:
        1. Işınım etkisi: 0.0175 × (800 - 300) = 8.75
        2. Sıcaklık etkisi: 1.14 × (30 - 25) = 5.7
        3. Tc = 30 + 8.75 + 5.7 = 44.45°C
        """)

    # Yeni formüller bölümü eklenecek
    st.subheader("5️⃣ Gerilim ve Akım Ayarı")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        \begin{align*}
        V &= V_{\text{ref}} + (K_v \times \Delta T) \\
        I &= I_{\text{ref}} + (K_i \times \Delta T)
        \end{align*}
        ''')
        st.markdown("""
        **Parametreler:**
        - Vref: Referans gerilim (V)
        - Iref: Referans akım (A)
        - Kv: Gerilim sıcaklık katsayısı (V/°C)
        - Ki: Akım sıcaklık katsayısı (A/°C)
        - ΔT: Sıcaklık farkı (°C)
        """)
    
    with col2:
        st.success("""
        **📌 Örnek Hesaplama:**
        Veriler:
        - Vref = 30V
        - Kv = -0.37 V/°C
        - ΔT = 15°C
        
        Hesaplama:
        V = 30 + (-0.37 × 15) = 24.45V
        
        Benzer şekilde akım için:
        I = 8A + (0.05 × 15) = 8.75A
        """)

    st.subheader("6️⃣ Maksimum Güç Hesaplama")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        P_{\text{max}} = V_{\text{total}} \times I_{\text{total}}
        ''')
        st.markdown("""
        **Parametreler:**
        - Vtotal: Toplam gerilim (V)
        - Itotal: Toplam akım (A)
        - Pmax: Maksimum güç (W)
        """)
    
    with col2:
        st.success("""
        **📌 Örnek Hesaplama:**
        Veriler:
        - Vtotal = 24.45V
        - Itotal = 8.75A
        
        Hesaplama:
        Pmax = 24.45 × 8.75 = 213.94W
        """)

    st.subheader("7️⃣ Bina Enerji Tüketimi")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        \begin{align*}
        E_{\text{daily}} &= \frac{E_{\text{yearly}}}{365} \\
        E_{\text{total daily}} &= E_{\text{daily}} \times \text{Adet}
        \end{align*}
        ''')
        st.markdown("""
        **Parametreler:**
        - Eyearly: Yıllık enerji tüketimi (kWh)
        - Edaily: Günlük enerji tüketimi (kWh)
        - Etotal daily: Toplam günlük tüketim (kWh)
        - Adet: Bina sayısı
        """)
    
    with col2:
        st.success("""
        **📌 Örnek Hesaplama:**
        Veriler:
        - Eyearly = 3650 kWh
        - Adet = 5 bina
        
        Hesaplama:
        1. Edaily = 3650 ÷ 365 = 10 kWh/gün
        2. Etotal daily = 10 × 5 = 50 kWh/gün
        """)

    st.subheader("8️⃣ Tasarruf ve Geri Dönüş Hesaplaması")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.latex(r'''
        \begin{align*}
        S_{\text{total}} &= \sum_{t=\text{day, peak, night}}(E_t \times C_t) \\
        T_{\text{payback}} &= \frac{C_{\text{initial}}}{S_{\text{net annual}}}
        \end{align*}
        ''')
        st.markdown("""
        **Parametreler:**
        - Et: Üretilen enerji miktarı (kWh)
        - Ct: Zaman dilimi enerji fiyatı (TL/kWh)
        - Cinitial: Başlangıç maliyeti (TL)
        - Snet annual: Net yıllık tasarruf (TL)
        """)
    
    with col2:
        st.success("""
        **📌 Örnek Hesaplama:**
        Veriler:
        - Gündüz: 100 kWh × 2.5 TL
        - Puant: 50 kWh × 3.5 TL
        - Gece: 30 kWh × 1.5 TL
        - Başlangıç maliyeti: 50,000 TL
        
        Hesaplama:
        1. Stotal = (250 + 175 + 45) = 470 TL/gün
        2. Yıllık tasarruf ≈ 171,550 TL
        3. Tpayback = 50,000 ÷ 171,550 ≈ 0.29 yıl
        """)

    # Formüller hakkında genel notlar güncelleniyor
    st.warning("""
    ⚠️ **Önemli Notlar:**
    1. Tüm formüller ideal koşullar için geçerlidir
    2. Gerçek değerler çevresel faktörlerden etkilenebilir
    3. Hesaplamalarda güvenlik faktörü kullanılması önerilir
    4. Periyodik kalibrasyon ve doğrulama gereklidir
    5. Sıcaklık değişimleri panel performansını önemli ölçüde etkiler
    6. Finansal hesaplamalarda enflasyon ve kur değişimleri dikkate alınmalıdır
    """)

    # ==========================================
    # Programın Genel İşleyişi
    # ==========================================
    st.header("Programın Genel İşleyişi")
    
    # Akış şeması açıklaması
    st.markdown("#### Program Akış Şeması")
    
    # Adımları görsel olarak göster
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1️⃣ Veri Girişi ve Doğrulama**
        - Kullanıcı parametrelerinin alınması
        - Veri doğrulama kontrolleri
        - Hata kontrolü ve geri bildirim
        
        **2️⃣ Temel Hesaplamalar**
        - Güneş geometrisi hesaplamaları
        - Panel açısı optimizasyonu
        - Sıcaklık etkisi hesaplamaları
        
        **3️⃣ Enerji Üretim Analizi**
        - Saatlik/günlük üretim tahminleri
        - Mevsimsel performans analizi
        - Kayıp faktörlerinin değerlendirilmesi
        """)
    
    with col2:
        st.markdown("""
        **4️⃣ Finansal Hesaplamalar**
        - Yatırım maliyeti analizi
        - Geri ödeme süresi hesaplaması
        - Finansal kazanç projeksiyonları
        
        **5️⃣ Raporlama ve Görselleştirme**
        - Grafik ve tablo oluşturma
        - PDF rapor hazırlama
        - Veri dışa aktarma seçenekleri
        
        **6️⃣ Sonuç ve Öneriler**
        - Sistem optimizasyon önerileri
        - Performans iyileştirme tavsiyeleri
        - Bakım ve izleme planı
        """)
    
    # İşleyiş hakkında ek bilgiler
    st.info("""
    🔄 **Sürekli İyileştirme:**
    Program, kullanıcı geri bildirimleri ve güncel teknolojik gelişmeler doğrultusunda 
    sürekli güncellenmekte ve iyileştirilmektedir.
    """)




