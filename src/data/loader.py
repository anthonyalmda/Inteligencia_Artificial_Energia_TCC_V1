"""Carregador principal de dados com fallback para simulação."""
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime, timedelta
import numpy as np

from .inmet import fetch_inmet
from .ons import fetch_ons_load
from .ccee import fetch_pld
from .pvgis import fetch_pvgis_ghi
from .openweather import fetch_weather_owm
import yaml

def load_data_with_fallback(
    start: str,
    end: str,
    region: str = "SE",
    submercado: str = "SE",
    inmet_station: str = "A701",
    cache_dir: Optional[Path] = None,
    use_real_data: bool = True,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    openweather_api_key: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carrega dados de múltiplas fontes com fallback para simulação.
    
    Returns:
        Tuple[consumption_df, production_df, pld_df, climate_df]
    """
    if cache_dir is None:
        cache_dir = Path("data/raw")
    
    consumption_df = None
    production_df = None
    pld_df = None
    climate_df = None
    
    if use_real_data:
        try:
            # Tentar carregar dados reais
            ons_data = fetch_ons_load(region, start, end, cache_dir)
            pld_df = fetch_pld(submercado, start, end, "diario", cache_dir)
            
            # Clima: tentar OpenWeatherMap primeiro, depois PVGIS, depois INMET
            climate_df = None
            if openweather_api_key and lat and lon:
                try:
                    climate_df = fetch_weather_owm(lat, lon, start, end, openweather_api_key, cache_dir)
                    print("[OK] Dados climaticos obtidos via OpenWeatherMap")
                except Exception as e:
                    print(f"Aviso: Erro ao buscar OpenWeatherMap ({e})")
            
            if climate_df is None and lat and lon:
                try:
                    climate_df = fetch_pvgis_ghi(lat, lon, start, end, cache_dir)
                    if climate_df is not None and len(climate_df) > 0:
                        print("[OK] Dados climaticos obtidos via PVGIS")
                except Exception as e:
                    print(f"Aviso: Erro ao buscar PVGIS ({e})")
            
            if climate_df is None:
                try:
                    climate_df = fetch_inmet(inmet_station, start, end, cache_dir)
                except Exception as e:
                    print(f"Aviso: Erro ao buscar INMET ({e})")
            
            # Converter carga ONS para consumo (aproximação)
            if "load_mw" in ons_data.columns:
                consumption_df = ons_data[["timestamp", "load_mw"]].rename(
                    columns={"load_mw": "consumption_kwh"}
                )
                consumption_df["consumption_kwh"] *= 1000  # MW para kWh (aproximação diária)
            
            if "generation_mw" in ons_data.columns:
                production_df = ons_data[["timestamp", "generation_mw"]].rename(
                    columns={"generation_mw": "production_kwh"}
                )
                production_df["production_kwh"] *= 1000
            
        except Exception as e:
            print(f"Erro ao carregar dados reais: {e}. Usando dados simulados.")
            use_real_data = False
    
    if not use_real_data or consumption_df is None or production_df is None:
        # Fallback: dados simulados
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        
        np.random.seed(42)
        n_days = len(dates)
        
        # Consumo com padrão semanal
        weekly = np.sin(np.arange(n_days) * 2 * np.pi / 7)
        consumption = 100 + 20 * weekly + np.random.normal(0, 5, n_days)
        
        # Produção solar com padrão sazonal e GHI
        if climate_df is not None and "ghi_wm2" in climate_df.columns:
            ghi_normalized = climate_df["ghi_wm2"].values / 1000
            production = 110 * ghi_normalized + np.random.normal(0, 10, n_days)
        else:
            seasonal = np.sin(np.arange(n_days) * 2 * np.pi / 365)
            production = 90 + 25 * seasonal + np.random.normal(0, 10, n_days)
        
        consumption_df = pd.DataFrame({
            "timestamp": dates,
            "consumption_kwh": np.maximum(0, consumption)
        })
        
        production_df = pd.DataFrame({
            "timestamp": dates,
            "production_kwh": np.maximum(0, production)
        })
        
        if pld_df is None:
            pld_df = fetch_pld(submercado, start, end, "diario", cache_dir)
        
        if climate_df is None:
            if lat and lon:
                climate_df = fetch_pvgis_ghi(lat, lon, start, end, cache_dir)
            else:
                climate_df = fetch_inmet(inmet_station, start, end, cache_dir)
    
    return consumption_df, production_df, pld_df, climate_df

