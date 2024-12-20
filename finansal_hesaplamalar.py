# finansal_hesaplamalar.py

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import numpy_financial as npf

class FinansalAnalizler:
    def __init__(self):
        self.kdv_orani = 0.20
        self.enflasyon_orani = 0.45  # Yıllık enflasyon oranı
        self.elektrik_zam_orani = 0.35  # Yıllık elektrik zam oranı
        self.faiz_orani = 0.30  # Yıllık faiz oranı
        
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

    def kredi_hesapla(self, kredi_tutari, vade_yil, yillik_faiz_orani=None):
        """Kredi ödemelerini hesaplar."""
        if yillik_faiz_orani is None:
            yillik_faiz_orani = self.faiz_orani
            
        aylik_faiz = yillik_faiz_orani / 12
        vade_ay = vade_yil * 12
        
        # Aylık taksit tutarı hesaplama
        taksit = kredi_tutari * (aylik_faiz * (1 + aylik_faiz)**vade_ay) / ((1 + aylik_faiz)**vade_ay - 1)
        
        odeme_plani = []
        kalan_anapara = kredi_tutari
        
        for ay in range(1, vade_ay + 1):
            faiz_tutari = kalan_anapara * aylik_faiz
            anapara_tutari = taksit - faiz_tutari
            kalan_anapara -= anapara_tutari
            
            odeme_plani.append({
                'ay': ay,
                'taksit': taksit,
                'anapara': anapara_tutari,
                'faiz': faiz_tutari,
                'kalan_anapara': max(0, kalan_anapara)
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
        """Net Bugünkü Değer (NPV) hesaplar."""
        npv = 0
        for t, nakit in enumerate(nakit_akislari, 1):
            npv += nakit / (1 + iskonto_orani) ** t
        return npv

    def ic_verim_orani(self, nakit_akislari, baslangic_yatirimi):
        """İç Verim Oranı (IRR) hesaplar."""
        nakit_akislari = [-baslangic_yatirimi] + nakit_akislari
        return npf.irr(nakit_akislari)

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
                'Net Bugünkü Değer (NPV)': f"{npv:,.2f} TL",
                'İç Verim Oranı (IRR)': f"%{irr*100:.2f}",
                'Geri Ödeme Süresi': f"{len(geri_odeme)} yıl"
            },
            'karbon_analizi': {
                'Yıllık CO₂ Tasarrufu': f"{karbon['yillik_karbon_tasarrufu']:,.2f} ton",
                '25 Yıllık CO₂ Tasarrufu': f"{karbon['25_yillik_tasarruf']:,.2f} ton",
                'Ağaç Eşdeğeri': f"{karbon['agac_esdegeri']:,.0f} ağaç"
            }
        }
