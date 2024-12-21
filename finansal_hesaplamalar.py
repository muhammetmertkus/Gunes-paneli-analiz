# finansal_hesaplamalar.py

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class FinansalAnalizler:
    def __init__(self):
        # Temel parametreler
        self.kdv_orani = 0.20
        self.enflasyon_orani = 0.30
        self.elektrik_zam_orani = 0.35
        self.faiz_orani = 0.35
        
        # Sistem kayıp parametreleri
        self.golgelenme_kaybi = 0.05
        self.sicaklik_kaybi = 0.03
        self.kablo_kaybi = 0.02
        self.inverter_verimi = 0.96
        self.panel_yaslanma_kaybi = 0.007  # Yıllık panel yaşlanma kaybı
        
        # Bakım ve işletme parametreleri
        self.bakim_maliyet_orani = 0.015
        self.sigorta_maliyet_orani = 0.005
        self.temizlik_maliyet = 2000
        self.inverter_degisim_yili = 10
        self.inverter_maliyet_orani = 0.15
        
    def panel_maliyeti_hesapla(self, panel_sayisi, panel_birim_fiyat, kdv_orani=None):
        """Panel maliyetini ve KDV'yi hesaplar."""
        if kdv_orani is None:
            kdv_orani = self.kdv_orani
            
        toplam_maliyet = panel_sayisi * panel_birim_fiyat
        kdv_tutari = toplam_maliyet * kdv_orani
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

    def kredi_hesapla(self, kredi_tutari, vade_yil, faiz_orani):
        """Kredi ödeme planını hesaplar."""
        vade_ay = vade_yil * 12
        aylik_faiz = faiz_orani / 12 / 100
        
        aylik_taksit = (kredi_tutari * aylik_faiz * (1 + aylik_faiz)**vade_ay) / ((1 + aylik_faiz)**vade_ay - 1)
        
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
                'Kalan Anapara': max(0, kalan)
            })
        
        return pd.DataFrame(odeme_plani)

    def detayli_elektrik_analizi(self, yillik_uretim, elektrik_birim_fiyat, panel_verim=0.20,
                                sistem_kayip=0.10, sistem_maliyeti=None, yillik_tuketim=None,
                                golgelenme_kayip=0.05, sicaklik_kayip=0.03, kablo_kayip=0.02,
                                inverter_verim=0.96):
        """25 yıllık detaylı elektrik üretim ve finansal analiz."""
        if yillik_tuketim is None:
            yillik_tuketim = yillik_uretim
        
        if sistem_maliyeti is None:
            sistem_maliyeti = yillik_uretim * 1000
        
        yillik_analiz = []
        kumulatif_tasarruf = 0
        amortisman_yili = None
        
        # Toplam sistem kayıpları
        toplam_kayip = (sistem_kayip + golgelenme_kayip + sicaklik_kayip + 
                       kablo_kayip + (1 - inverter_verim))
        
        for yil in range(1, 26):
            # Panel yaşlanma etkisi
            verim_kaybi = (1 - self.panel_yaslanma_kaybi) ** (yil - 1)
            yillik_net_uretim = yillik_uretim * verim_kaybi * (1 - toplam_kayip)
            
            # Elektrik fiyatı artışı
            guncel_elektrik_fiyati = elektrik_birim_fiyat * (1 + self.elektrik_zam_orani) ** (yil - 1)
            
            # Öz tüketim ve şebeke etkileşimi
            oz_tuketim = min(yillik_net_uretim, yillik_tuketim)
            sebekeye_satilan = max(0, yillik_net_uretim - yillik_tuketim)
            sebekeden_alinan = max(0, yillik_tuketim - yillik_net_uretim)
            
            # Gelir hesaplaması
            oz_tuketim_geliri = oz_tuketim * guncel_elektrik_fiyati
            satis_geliri = sebekeye_satilan * guncel_elektrik_fiyati * 0.85  # Şebekeye satış indirimi
            toplam_gelir = oz_tuketim_geliri + satis_geliri
            
            # Gider hesaplaması
            bakim_maliyeti = sistem_maliyeti * self.bakim_maliyet_orani * (1 + self.enflasyon_orani) ** (yil - 1)
            sigorta_maliyeti = sistem_maliyeti * self.sigorta_maliyet_orani * (1 + self.enflasyon_orani) ** (yil - 1)
            temizlik_maliyeti = self.temizlik_maliyet * (1 + self.enflasyon_orani) ** (yil - 1)
            
            # İnverter değişim maliyeti
            inverter_maliyeti = (sistem_maliyeti * self.inverter_maliyet_orani * 
                               (1 + self.enflasyon_orani) ** (yil - 1)) if yil == self.inverter_degisim_yili else 0
            
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
                'Öz Tüketim (kWh)': oz_tuketim,
                'Şebekeye Satılan (kWh)': sebekeye_satilan,
                'Şebekeden Alınan (kWh)': sebekeden_alinan,
                'Öz Tüketim Geliri (TL)': oz_tuketim_geliri,
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
        """Sistem performans metriklerini hesaplar."""
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

    def karbon_ayak_izi_analizi(self, yillik_uretim, sera_gazi_faktoru=0.5, agac_esdeger_faktoru=60.5):
        """Karbon ayak izi tasarrufunu hesaplar."""
        yillik_tasarruf = yillik_uretim * sera_gazi_faktoru / 1000  # ton CO2
        
        return {
            'yillik_karbon_tasarrufu': yillik_tasarruf,
            '25_yillik_tasarruf': yillik_tasarruf * 25,
            'agac_esdegeri': yillik_tasarruf * agac_esdeger_faktoru
        }

    def risk_analizi(self, senaryo_sayisi=1000, elektrik_zam_orani=0.35, 
                     enflasyon_orani=0.30, uretim_dalgalanma=0.10):
        """Monte Carlo simülasyonu ile risk analizi yapar."""
        sonuclar = []
        
        for _ in range(senaryo_sayisi):
            # Rastgele parametre değerleri
            elektrik_zam = np.random.normal(elektrik_zam_orani, elektrik_zam_orani * 0.2)  # %20 standart sapma
            enflasyon = np.random.normal(enflasyon_orani, enflasyon_orani * 0.2)
            uretim_performansi = np.random.normal(1, uretim_dalgalanma)
            
            sonuclar.append({
                'elektrik_zam': elektrik_zam * 100,  # Yüzde olarak
                'enflasyon': enflasyon * 100,
                'uretim_performansi': uretim_performansi
            })
            
        return pd.DataFrame(sonuclar)
    
