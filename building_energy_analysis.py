# building_energy_analysis.py

import math
import pandas as pd

def calculate_building_energy(data_with_counts, power_factor=0.9):
    """
    Bina tiplerine göre toplam günlük enerji, aktif güç ve reaktif güç hesaplar.
    """
    results_with_counts = []
    
    for i, item in enumerate(data_with_counts["Bina Tipi"]):
        yearly_energy = data_with_counts["Yıllık Ortalama Enerji (kWh)"][i]
        count = data_with_counts["Adet"][i]
        daily_energy = yearly_energy / 365  # Günlük enerji tüketimi (kWh/gün)
        total_daily_energy = daily_energy * count  # Toplam günlük enerji (kWh)
        active_power = total_daily_energy * 1000  # Aktif güç (W)
        reactive_power = active_power * math.tan(math.acos(power_factor))  # Reaktif güç (VAR)
        results_with_counts.append({
            "Bina Tipi": item,
            "Adet": count,
            "Toplam Günlük Enerji (kWh)": round(total_daily_energy, 2),
            "Toplam Aktif Güç (W)": round(active_power, 2),
            "Toplam Reaktif Güç (VAR)": round(reactive_power, 2)
        })
    
    results_with_counts_df = pd.DataFrame(results_with_counts)
    return results_with_counts_df
