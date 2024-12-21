# finansal_hesaplamalar.py

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class FinansalAnalizler:
    def __init__(self):
        self.kdv_orani = 0.20
        self.enflasyon_orani = 0.30
        self.elektrik_zam_orani = 0.35
        self.faiz_orani = 0.35
        
    def panel_maliyeti_hesapla(self, panel_sayisi, panel_birim_fiyat):
        """Panel maliyetini hesaplar."""
        toplam_maliyet = panel_sayisi * panel_birim_fiyat
        kdv_tutari = toplam_maliyet * self.kdv_orani
        return {
            'panel_maliyeti': toplam_maliyet,
            'kdv_tutari': kdv_tutari,
            'toplam_maliyet': toplam_maliyet + kdv_tutari
        }
    
    def kurulum_maliyeti_hesapla(self, panel_sayisi, iscilik_birim_fiyat, 
                                ekipman_maliyeti, tasima_montaj_maliyeti):
        """Kurulum maliyetlerini hesaplar."""
        iscilik_maliyeti = panel_sayisi * iscilik_birim_fiyat
        toplam_kurulum = iscilik_maliyeti + ekipman_maliyeti + tasima_montaj_maliyeti
        return {
            'iscilik_maliyeti': iscilik_maliyeti,
            'ekipman_maliyeti': ekipman_maliyeti,
            'tasima_montaj': tasima_montaj_maliyeti,
            'toplam_kurulum': toplam_kurulum
        }

    def bakim_maliyeti_hesapla(self, sistem_gucu, yillik_bakim_orani=0.015):
        """Yıllık bakım maliyetlerini hesaplar."""
        yillik_bakim = sistem_gucu * yillik_bakim_orani
        return {
            'yillik_bakim': yillik_bakim,
            '5_yillik_bakim': yillik_bakim * 5 * (1 + self.enflasyon_orani) ** 5,
            '10_yillik_bakim': yillik_bakim * 10 * (1 + self.enflasyon_orani) ** 10
        }

    def kredi_hesapla(self, kredi_tutari, vade_yil, faiz_orani):
        """
        Kredi ödeme planını hesaplar
        
        Args:
            kredi_tutari (float): Kredi tutarı
            vade_yil (int): Vade süresi (yıl)
            faiz_orani (float): Yıllık faiz oranı (%)
        
        Returns:
            pd.DataFrame: Kredi ödeme planı
        """
        vade_ay = vade_yil * 12
        aylik_faiz = faiz_orani / 12 / 100
        
        # Aylık taksit tutarı
        aylik_taksit = (kredi_tutari * aylik_faiz * (1 + aylik_faiz)**vade_ay) / ((1 + aylik_faiz)**vade_ay - 1)
        
        # Ödeme planı oluşturma
        odeme_plani = []
        kalan = kredi_tutari
        
        for ay in range(1, vade_ay + 1):
            faiz = kalan * aylik_faiz
            anapara = aylik_taksit - faiz
            kalan = kalan - anapara
            
            odeme_plani.append({
                'Taksit No': ay,
                'Taksit Tutarı': aylik_taksit,
                'Anapara': anapara,
                'Faiz': faiz,
                'Kalan Anapara': max(0, kalan)  # Negatif değer olmaması için
            })
        
        return pd.DataFrame(odeme_plani) 
    def elektrik_uretim_geliri(self, yillik_uretim, elektrik_birim_fiyat, yil=25):
        """Elektrik üretiminden elde edilecek geliri hesaplar."""
        gelirler = []
        birim_fiyat = elektrik_birim_fiyat
        
        for i in range(yil):
            yillik_gelir = yillik_uretim * birim_fiyat
            gelirler.append({
                'yil': i + 1,
                'birim_fiyat': birim_fiyat,
                'yillik_uretim': yillik_uretim,
                'yillik_gelir': yillik_gelir
            })
            birim_fiyat *= (1 + self.elektrik_zam_orani)
            
        return pd.DataFrame(gelirler)

    def net_bugunki_deger(self, nakit_akislari, iskonto_orani=0.15):
        """
        Net Bugünkü Değer (NPV) hesaplar
        
        Args:
            nakit_akislari (list): Yıllık nakit akışları listesi
            iskonto_orani (float): Yıllık iskonto oranı
        
        Returns:
            float: Net bugünkü değer
        """
        npv = 0
        for t, nakit in enumerate(nakit_akislari, 1):
            npv += nakit / (1 + iskonto_orani) ** t
        return npv

    def ic_verim_orani(self, nakit_akislari, baslangic_yatirimi, tolerans=0.0001, max_iterasyon=1000):
        """
        İç Verim Oranı (IRR) hesaplar (Newton-Raphson yöntemi ile)
        
        Args:
            nakit_akislari (list): Yıllık nakit akışları listesi
            baslangic_yatirimi (float): İlk yatırım tutarı
            tolerans (float): Hesaplama hassasiyeti
            max_iterasyon (int): Maksimum iterasyon sayısı
        
        Returns:
            float: İç verim oranı (IRR)
        """
        def npv(rate):
            # Net Bugünkü Değer hesaplama
            npv_value = -baslangic_yatirimi
            for t, nakit in enumerate(nakit_akislari, 1):
                npv_value += nakit / (1 + rate) ** t
            return npv_value
        
        def npv_turev(rate):
            # NPV'nin türevi
            turev = 0
            for t, nakit in enumerate(nakit_akislari, 1):
                turev -= t * nakit / (1 + rate) ** (t + 1)
            return turev
        
        # Newton-Raphson yöntemi ile IRR hesaplama
        rate = 0.1  # Başlangıç tahmini
        for _ in range(max_iterasyon):
            npv_value = npv(rate)
            if abs(npv_value) < tolerans:
                return rate
            
            turev = npv_turev(rate)
            if turev == 0:
                return None
            
            yeni_rate = rate - npv_value / turev
            if abs(yeni_rate - rate) < tolerans:
                return yeni_rate
            
            rate = yeni_rate
        
        return None  # Yakınsama sağlanamazsa None döndür

    def geri_odeme_suresi(self, yillik_tasarruf, toplam_yatirim, 
                         elektrik_zam_orani=None, enflasyon_orani=None):
        """Detaylı geri ödeme süresi hesaplar."""
        if elektrik_zam_orani is None:
            elektrik_zam_orani = self.elektrik_zam_orani
        if enflasyon_orani is None:
            enflasyon_orani = self.enflasyon_orani
            
        kalan_yatirim = toplam_yatirim
        yil = 0
        tasarruf = yillik_tasarruf
        geri_odeme_detay = []
        
        while kalan_yatirim > 0 and yil < 25:
            yil += 1
            tasarruf *= (1 + elektrik_zam_orani)
            kalan_yatirim -= tasarruf
            
            geri_odeme_detay.append({
                'yil': yil,
                'yillik_tasarruf': tasarruf,
                'kalan_yatirim': max(0, kalan_yatirim)
            })
            
        return pd.DataFrame(geri_odeme_detay)

    def duyarlilik_analizi(self, baz_senaryo, degisken_parametreler):
        """Duyarlılık analizi yapar."""
        sonuclar = []
        
        for param, degerler in degisken_parametreler.items():
            for deger in degerler:
                senaryo = baz_senaryo.copy()
                senaryo[param] = deger
                
                # Senaryo hesaplamaları
                npv = self.net_bugunki_deger(senaryo['nakit_akislari'])
                irr = self.ic_verim_orani(senaryo['nakit_akislari'], 
                                        senaryo['baslangic_yatirimi'])
                
                sonuclar.append({
                    'parametre': param,
                    'deger': deger,
                    'npv': npv,
                    'irr': irr
                })
                
        return pd.DataFrame(sonuclar)

    def risk_analizi(self, senaryo_sayisi=1000):
        """Monte Carlo simülasyonu ile risk analizi yapar."""
        sonuclar = []
        
        for _ in range(senaryo_sayisi):
            # Rastgele parametre değerleri
            elektrik_zam = np.random.normal(self.elektrik_zam_orani, 0.05)
            enflasyon = np.random.normal(self.enflasyon_orani, 0.05)
            uretim_performansi = np.random.normal(1, 0.1)
            
            # Senaryo hesaplamaları
            senaryo = {
                'elektrik_zam': elektrik_zam,
                'enflasyon': enflasyon,
                'uretim_performansi': uretim_performansi
            }
            
            sonuclar.append(senaryo)
            
        return pd.DataFrame(sonuclar)

    def karbon_ayak_izi_analizi(self, yillik_uretim, sera_gazi_faktoru=0.5):
        """Karbon ayak izi tasarrufunu hesaplar."""
        yillik_tasarruf = yillik_uretim * sera_gazi_faktoru
        
        return {
            'yillik_karbon_tasarrufu': yillik_tasarruf,
            '25_yillik_tasarruf': yillik_tasarruf * 25,
            'agac_esdegeri': yillik_tasarruf * 0.0165  # 1 ton CO2 = 60.5 ağaç
        }

    def rapor_olustur(self, proje_bilgileri):
        """Detaylı finansal rapor oluşturur."""
        # Hesaplamalar
        npv = self.net_bugunki_deger(proje_bilgileri['nakit_akislari'])
        irr = self.ic_verim_orani(proje_bilgileri['nakit_akislari'], 
                                 proje_bilgileri['toplam_yatirim'])
        geri_odeme = self.geri_odeme_suresi(
            proje_bilgileri['yillik_tasarruf'],
            proje_bilgileri['toplam_yatirim']
        )
        karbon = self.karbon_ayak_izi_analizi(proje_bilgileri['yillik_uretim'])
        
        # Rapor formatı
        return {
            'proje_ozeti': {
                'Toplam Yatırım': f"{proje_bilgileri['toplam_yatirim']:,.2f} TL",
                'Yıllık Üretim': f"{proje_bilgileri['yillik_uretim']:,.2f} kWh",
                'Sistem Gücü': f"{proje_bilgileri['sistem_gucu']:,.2f} kW"
            },
            'finansal_metrikler': {
                'Net Bugünk�� Değer (NPV)': f"{npv:,.2f} TL",
                'İç Verim Oranı (IRR)': f"%{irr*100:.2f}",
                'Geri Ödeme Süresi': f"{len(geri_odeme)} yıl"
            },
            'karbon_analizi': {
                'Yıllık CO₂ Tasarrufu': f"{karbon['yillik_karbon_tasarrufu']:,.2f} ton",
                '25 Yıllık CO₂ Tasarrufu': f"{karbon['25_yillik_tasarruf']:,.2f} ton",
                'Ağaç Eşdeğeri': f"{karbon['agac_esdegeri']:,.0f} ağaç"
            }
            }
    def elektrik_uretim_analizi(self, yillik_uretim, elektrik_birim_fiyat, panel_verim=0.20, 
                            golgelenme_kayip=0.05, sistem_kayip=0.10, yillik_tuketim=None):
        """
        Detaylı elektrik üretim ve tüketim analizi yapar
        
        Args:
            yillik_uretim (float): Tahmini yıllık üretim (kWh)
            elektrik_birim_fiyat (float): Elektrik birim fiyatı (TL/kWh)
            panel_verim (float): Panel verimi (default: 0.20)
            golgelenme_kayip (float): Gölgelenme kayıp oranı (default: 0.05)
            sistem_kayip (float): Sistem kayıpları (inverter, kablo vs.) (default: 0.10)
            yillik_tuketim (float): Yıllık tüketim miktarı (kWh) (default: None)
        
        Returns:
            pd.DataFrame: Detaylı üretim analizi
        """
        # Kayıp hesaplamaları
        golgelenme_kaybi = yillik_uretim * golgelenme_kayip
        sistem_kaybi = yillik_uretim * sistem_kayip
        
        # Net üretim
        net_uretim = yillik_uretim * (1 - golgelenme_kayip - sistem_kayip)
        
        # Aylık ortalama üretim
        aylik_ortalama = net_uretim / 12
        
        # Mevsimsel dağılım (yaklaşık değerler)
        mevsimsel_carpanlar = {
            'Kış': 0.6,    # Aralık, Ocak, Şubat
            'İlkbahar': 1.1,  # Mart, Nisan, Mayıs
            'Yaz': 1.4,    # Haziran, Temmuz, Ağustos
            'Sonbahar': 0.9   # Eylül, Ekim, Kasım
        }
        
        mevsimsel_uretim = {
            mevsim: aylik_ortalama * carpan * 3
            for mevsim, carpan in mevsimsel_carpanlar.items()
        }
        
        # Finansal hesaplamalar
        yillik_gelir = net_uretim * elektrik_birim_fiyat
        
        # Tüketim analizi
        if yillik_tuketim is None:
            yillik_tuketim = net_uretim  # Varsayılan olarak üretim kadar tüketim
        
        fazla_uretim = max(0, net_uretim - yillik_tuketim)
        eksik_uretim = max(0, yillik_tuketim - net_uretim)
        
        # Mahsuplaşma ve satış geliri
        mahsuplasma_gelir = min(net_uretim, yillik_tuketim) * elektrik_birim_fiyat
        satis_geliri = fazla_uretim * (elektrik_birim_fiyat * 0.85)  # Fazla üretim daha düşük fiyattan satılır
        toplam_gelir = mahsuplasma_gelir + satis_geliri
        
        # Verileri DataFrame'e dönüştürme
        analiz_sonuclari = pd.DataFrame([{
            'Parametre': 'Brüt Üretim (kWh)',
            'Değer': yillik_uretim,
            'Açıklama': 'Toplam teorik üretim miktarı'
        }, {
            'Parametre': 'Gölgelenme Kaybı (kWh)',
            'Değer': golgelenme_kaybi,
            'Açıklama': f'Gölgelenme nedeniyle kayıp (%{golgelenme_kayip*100:.1f})'
        }, {
            'Parametre': 'Sistem Kaybı (kWh)',
            'Değer': sistem_kaybi,
            'Açıklama': f'Sistem kayıpları (%{sistem_kayip*100:.1f})'
        }, {
            'Parametre': 'Net Üretim (kWh)',
            'Değer': net_uretim,
            'Açıklama': 'Kayıplar sonrası net üretim'
        }, {
            'Parametre': 'Panel Verimi',
            'Değer': panel_verim,
            'Açıklama': f'Panel verim oranı (%{panel_verim*100:.1f})'
        }])
        
        # Mevsimsel üretim verilerini ekle
        for mevsim, uretim in mevsimsel_uretim.items():
            analiz_sonuclari = pd.concat([analiz_sonuclari, pd.DataFrame([{
                'Parametre': f'{mevsim} Üretimi (kWh)',
                'Değer': uretim,
                'Açıklama': f'{mevsim} mevsimi toplam üretim'
            }])], ignore_index=True)
        
        # Finansal verileri ekle
        finansal_veriler = pd.DataFrame([{
            'Parametre': 'Yıllık Tüketim (kWh)',
            'Değer': yillik_tuketim,
            'Açıklama': 'Tesisin yıllık tüketimi'
        }, {
            'Parametre': 'Fazla Üretim (kWh)',
            'Değer': fazla_uretim,
            'Açıklama': 'Şebekeye satılan üretim'
        }, {
            'Parametre': 'Eksik Üretim (kWh)',
            'Değer': eksik_uretim,
            'Açıklama': 'Şebekeden alınan enerji'
        }, {
            'Parametre': 'Mahsuplaşma Geliri (TL)',
            'Değer': mahsuplasma_gelir,
            'Açıklama': 'Tüketim dengeleme geliri'
        }, {
            'Parametre': 'Satış Geliri (TL)',
            'Değer': satis_geliri,
            'Açıklama': 'Fazla üretim satış geliri'
        }, {
            'Parametre': 'Toplam Gelir (TL)',
            'Değer': toplam_gelir,
            'Açıklama': 'Toplam yıllık gelir'
        }])
    
    def detayli_elektrik_analizi(self, yillik_uretim, elektrik_birim_fiyat, panel_verim=0.20,
                                golgelenme_kayip=0.05, sistem_kayip=0.10, yillik_tuketim=None,
                                panel_yaslanma_kaybi=0.007, enflasyon_orani=0.30, 
                                elektrik_zam_orani=0.35, bakim_maliyet_orani=0.015,
                                inverter_degisim_yili=10, inverter_maliyet_orani=0.15,
                                sigorta_maliyet_orani=0.005, temizlik_maliyet=2000,
                                sistem_maliyeti=None):
        """
        25 yıllık detaylı elektrik üretim, tüketim ve finansal analiz
        """
        if yillik_tuketim is None:
            yillik_tuketim = yillik_uretim
        
        if sistem_maliyeti is None:
            sistem_maliyeti = yillik_uretim * 1000  # Yaklaşık maliyet hesabı
        
        yillik_analiz = []
        kumulatif_tasarruf = 0
        amortisman_yili = None
        
        for yil in range(1, 26):
            # Panel yaşlanma etkisi
            verim_kaybi = (1 - panel_yaslanma_kaybi) ** (yil - 1)
            yillik_net_uretim = yillik_uretim * verim_kaybi * (1 - golgelenme_kayip - sistem_kayip)
            
            # Elektrik fiyatı artışı
            guncel_elektrik_fiyati = elektrik_birim_fiyat * (1 + elektrik_zam_orani) ** (yil - 1)
            
            # Tüketim ve üretim analizi
            fazla_uretim = max(0, yillik_net_uretim - yillik_tuketim)
            eksik_uretim = max(0, yillik_tuketim - yillik_net_uretim)
            
            # Gelir hesaplaması
            mahsuplasma_gelir = min(yillik_net_uretim, yillik_tuketim) * guncel_elektrik_fiyati
            satis_geliri = fazla_uretim * (guncel_elektrik_fiyati * 0.85)
            toplam_gelir = mahsuplasma_gelir + satis_geliri
            
            # Gider hesaplaması
            bakim_maliyeti = sistem_maliyeti * bakim_maliyet_orani * (1 + enflasyon_orani) ** (yil - 1)
            sigorta_maliyeti = sistem_maliyeti * sigorta_maliyet_orani * (1 + enflasyon_orani) ** (yil - 1)
            temizlik_maliyeti = temizlik_maliyet * (1 + enflasyon_orani) ** (yil - 1)
            
            # İnverter değişim maliyeti
            inverter_maliyeti = (sistem_maliyeti * inverter_maliyet_orani * (1 + enflasyon_orani) ** (yil - 1)) if yil == inverter_degisim_yili else 0
            
            toplam_gider = bakim_maliyeti + sigorta_maliyeti + temizlik_maliyeti + inverter_maliyeti
            
            # Net kazanç
            net_kazanc = toplam_gelir - toplam_gider
            kumulatif_tasarruf += net_kazanc
            
            # Amortisman yılı kontrolü
            if amortisman_yili is None and kumulatif_tasarruf >= sistem_maliyeti:
                amortisman_yili = yil
            
            yillik_analiz.append({
                'Yıl': yil,
                'Net Üretim (kWh)': yillik_net_uretim,
                'Verim Kaybı (%)': (1 - verim_kaybi) * 100,
                'Elektrik Birim Fiyatı (TL)': guncel_elektrik_fiyati,
                'Mahsuplaşma Geliri (TL)': mahsuplasma_gelir,
                'Satış Geliri (TL)': satis_geliri,
                'Toplam Gelir (TL)': toplam_gelir,
                'Bakım Gideri (TL)': bakim_maliyeti,
                'Sigorta Gideri (TL)': sigorta_maliyeti,
                'Temizlik Gideri (TL)': temizlik_maliyeti,
                'İnverter Gideri (TL)': inverter_maliyeti,
                'Toplam Gider (TL)': toplam_gider,
                'Net Kazanç (TL)': net_kazanc,
                'Kümülatif Tasarruf (TL)': kumulatif_tasarruf
            })
        
        return pd.DataFrame(yillik_analiz), amortisman_yili

    def hesapla_performans_metrikleri(self, yillik_analiz_df, sistem_maliyeti):
        """
        Sistem performans metriklerini hesaplar
        """
        toplam_uretim = yillik_analiz_df['Net Üretim (kWh)'].sum()
        toplam_gelir = yillik_analiz_df['Toplam Gelir (TL)'].sum()
        toplam_gider = yillik_analiz_df['Toplam Gider (TL)'].sum()
        net_kazanc = toplam_gelir - toplam_gider
        
        # ROI (Return on Investment)
        roi = (net_kazanc / sistem_maliyeti) * 100
        
        # LCOE (Levelized Cost of Energy)
        lcoe = (sistem_maliyeti + toplam_gider) / toplam_uretim
        
        return {
            'Toplam Üretim (kWh)': toplam_uretim,
            'Toplam Gelir (TL)': toplam_gelir,
            'Toplam Gider (TL)': toplam_gider,
            'Net Kazanç (TL)': net_kazanc,
            'ROI (%)': roi,
            'LCOE (TL/kWh)': lcoe
        }
    
    def enerji_dengesi_analizi(self, panel_uretimi, bina_tuketimi, elektrik_satis_fiyati=None, 
                              elektrik_alis_fiyati=None, panel_efficiency=0.20, 
                              satis_carpani=0.85, varsayilan_parametreler=None):
        """
        Panel üretimi ve bina tüketimi arasındaki enerji dengesini analiz eder
        
        Args:
            panel_uretimi (float): Panel yıllık üretim miktarı (kWh)
            bina_tuketimi (float): Bina yıllık tüketim miktarı (kWh)
            elektrik_satis_fiyati (float): Elektrik satış fiyatı (TL/kWh) (default: None)
            elektrik_alis_fiyati (float): Elektrik alış fiyatı (TL/kWh) (default: None)
            panel_efficiency (float): Panel verimi (default: 0.20)
            satis_carpani (float): Şebekeye satış fiyat çarpanı (default: 0.85)
            varsayilan_parametreler (dict): Varsayılan parametreler sözlüğü
        
        Returns:
            dict: Enerji dengesi ve finansal analiz sonuçları
        """
        # Varsayılan parametreleri ayarla
        if varsayilan_parametreler is None:
            varsayilan_parametreler = {
                'elektrik_satis_fiyati': 1.5,  # TL/kWh
                'elektrik_alis_fiyati': 1.8,   # TL/kWh
                'panel_efficiency': 0.20,       # %20
                'satis_carpani': 0.85,         # Şebekeye satış fiyat çarpanı
                'kayip_faktoru': 0.15,         # Sistem kayıpları
                'golgelenme_kaybi': 0.05,      # Gölgelenme kayıpları
                'sicaklik_kaybi': 0.03,        # Sıcaklık kayıpları
                'kablo_kaybi': 0.02,           # Kablo kayıpları
                'inverter_verimi': 0.96        # İnverter verimi
            }
        
        # Parametreleri kontrol et ve varsayılan değerleri kullan
        elektrik_satis_fiyati = elektrik_satis_fiyati or varsayilan_parametreler['elektrik_satis_fiyati']
        elektrik_alis_fiyati = elektrik_alis_fiyati or varsayilan_parametreler['elektrik_alis_fiyati']
        panel_efficiency = panel_efficiency or varsayilan_parametreler['panel_efficiency']
        
        # Panel üretimini kayıpları hesaba katarak düzelt
        net_uretim = panel_uretimi * (1 - varsayilan_parametreler['kayip_faktoru']) * \
                     (1 - varsayilan_parametreler['golgelenme_kaybi']) * \
                     (1 - varsayilan_parametreler['sicaklik_kaybi']) * \
                     (1 - varsayilan_parametreler['kablo_kaybi']) * \
                     varsayilan_parametreler['inverter_verimi']
        
        # Enerji dengesi hesaplamaları
        fazla_enerji = max(0, net_uretim - bina_tuketimi)
        eksik_enerji = max(0, bina_tuketimi - net_uretim)
        
        # Finansal hesaplamalar
        satis_geliri = fazla_enerji * elektrik_satis_fiyati * satis_carpani
        alis_maliyeti = eksik_enerji * elektrik_alis_fiyati
        
        # Verim hesaplamaları
        teorik_uretim = panel_uretimi
        gercek_uretim = net_uretim
        sistem_verimi = gercek_uretim / teorik_uretim if teorik_uretim > 0 else 0
        
        # Öz tüketim ve şebeke bağımlılığı
        oz_tuketim_orani = min(net_uretim, bina_tuketimi) / bina_tuketimi if bina_tuketimi > 0 else 0
        sebeke_bagimliligi = eksik_enerji / bina_tuketimi if bina_tuketimi > 0 else 0
        
        return {
            'Enerji Dengesi': {
                'Teorik Panel Üretimi (kWh)': teorik_uretim,
                'Net Panel Üretimi (kWh)': net_uretim,
                'Bina Tüketimi (kWh)': bina_tuketimi,
                'Fazla Enerji (kWh)': fazla_enerji,
                'Eksik Enerji (kWh)': eksik_enerji
            },
            'Finansal Analiz': {
                'Şebekeye Satış Geliri (TL)': satis_geliri,
                'Şebekeden Alış Maliyeti (TL)': alis_maliyeti,
                'Net Finansal Etki (TL)': satis_geliri - alis_maliyeti
            },
            'Verim Analizi': {
                'Panel Verimi (%)': panel_efficiency * 100,
                'Sistem Verimi (%)': sistem_verimi * 100,
                'Kayıplar (%)': (1 - sistem_verimi) * 100,
                'Öz Tüketim Oranı (%)': oz_tuketim_orani * 100,
                'Şebeke Bağımlılığı (%)': sebeke_bagimliligi * 100
            },
            'Kayıp Detayları': {
                'Sistem Kayıpları (%)': varsayilan_parametreler['kayip_faktoru'] * 100,
                'Gölgelenme Kayıpları (%)': varsayilan_parametreler['golgelenme_kaybi'] * 100,
                'Sıcaklık Kayıpları (%)': varsayilan_parametreler['sicaklik_kaybi'] * 100,
                'Kablo Kayıpları (%)': varsayilan_parametreler['kablo_kaybi'] * 100,
                'İnverter Verimi (%)': varsayilan_parametreler['inverter_verimi'] * 100
            }
        }

    def guncelle_varsayilan_parametreler(self, yeni_parametreler):
        """
        Varsayılan parametreleri günceller
        
        Args:
            yeni_parametreler (dict): Güncellenecek parametreler sözlüğü
        """
        varsayilan_parametreler = {
            'elektrik_satis_fiyati': 1.5,
            'elektrik_alis_fiyati': 1.8,
            'panel_efficiency': 0.20,
            'satis_carpani': 0.85,
            'kayip_faktoru': 0.15,
            'golgelenme_kaybi': 0.05,
            'sicaklik_kaybi': 0.03,
            'kablo_kaybi': 0.02,
            'inverter_verimi': 0.96
        }
        
        # Yeni parametreleri güncelle
        varsayilan_parametreler.update(yeni_parametreler)
        return varsayilan_parametreler
    
