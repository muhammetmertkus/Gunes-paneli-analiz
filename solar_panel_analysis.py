# solar_panel_analysis.py

import math
import numpy as np
import pandas as pd

def calculate_declination(day_of_year):
    """
    Güneş sapma açısını hesaplar.
    """
    if not (1 <= day_of_year <= 365):
        raise ValueError("day_of_year must be between 1 and 365")
    return 23.5 * math.sin(math.radians((360 / 365) * (day_of_year + 284)))

def calculate_annual_optimum_angle(latitude):
    """
    Jacobson yöntemiyle yıllık optimum panel açısını hesaplar.
    """
    beta = 1.3793 + latitude * (1.2011 + latitude * (-0.014404 + latitude * 0.000080509))
    return beta

def calculate_average_daily_irradiance_hourly(hourly_irradiance, delta_t=1):
    """
    Saatlik ışınım verilerini kullanarak ortalama günlük ışınımı hesaplar.
    """
    total_energy = sum(hourly_irradiance)  # kWh/m^2
    if sum(delta_t for _ in hourly_irradiance) == 0:
        return 0
    average_power_kW = total_energy / sum(delta_t for _ in hourly_irradiance)  # kW/m^2
    average_power_W = average_power_kW * 1000  # W/m^2
    return average_power_W

def calculate_panel_temperature(Gg, Ta):
    """
    Panel sıcaklığını hesaplar.
    Tc = 30 + 0.0175*(Gg - 300) + 1.14*(Ta - 25)
    """
    return 30 + 0.0175 * (Gg - 300) + 1.14 * (Ta - 25)

def adjust_parameters(V_ref, I_ref, Kv, Ki, delta_T):
    """
    Sıcaklık farkını kullanarak gerilim ve akımı ayarlar.
    """
    V = V_ref + (Kv * delta_T)
    I = I_ref + (Ki * delta_T)
    return V, I

def calculate_max_power(V, I):
    """
    Maksimum gücü hesaplar.
    """
    return V * I

def generate_hourly_irradiance(daylight_hours, global_radiation, seed=42):
    """
    Saatlik ışınım verilerini tahmin eder.
    """
    np.random.seed(seed)  # Sabit tohum
    hours = int(math.ceil(daylight_hours))
    if hours == 0:
        return [0] * 24
    irradiance = np.random.dirichlet(np.ones(hours), size=1)[0] * global_radiation
    hourly_irradiance = list(irradiance) + [0] * (24 - hours)
    return hourly_irradiance
import numpy as np

def calculate_panel_voltage_and_current(panel_data, irradiance, temperature):
    """
    Panel voltajını ve akımını tek diyot modeline göre hesaplar.
    """
    # Sabitler
    k = 1.380649e-23  # Boltzmann sabiti [J/K]
    q = 1.60217663e-19  # Elektron yükü [C]
    k_i = 0.0004  # Akım sıcaklık katsayısı [A/°C]
    k_v = -0.0023  # Gerilim sıcaklık katsayısı [V/°C]
    
    # Referans değerler
    T_ref = 298.15  # Referans sıcaklık (Kelvin)
    G_ref = 1000  # Referans ışınım (W/m²)
    
    # Panel parametreleri (tek modül için)
    Voc = panel_data['Voc']  # Açık devre gerilimi
    Isc = panel_data['Isc']  # Kısa devre akımı
    Vmp = panel_data['Vmp']  # Maksimum güç noktası gerilimi
    Imp = panel_data['Imp']  # Maksimum güç noktası akımı
    
    # Sıcaklık düzeltmesi
    T = temperature + 273.15
    delta_T = T - T_ref
    
    # Tek modül için voltaj ve akım hesaplama
    # Sıcaklık etkisi
    V_module = Vmp * (1 + k_v * delta_T)
    I_module = Imp * (1 + k_i * delta_T)
    
    # Işınım etkisi (sadece akımı etkiler)
    I_module = I_module * (irradiance / G_ref)
    
    # Seri ve paralel konfigürasyon
    series_modules = panel_data['series_modules']
    parallel_strings = panel_data['parallel_strings']
    
    # Toplam sistem değerleri
    V_total = V_module * series_modules
    I_total = I_module * parallel_strings
    
    # Güvenlik kontrolleri
    V_total = max(0, min(V_total, Voc * series_modules))
    I_total = max(0, min(I_total, Isc * parallel_strings))
    
    return V_total, I_total
