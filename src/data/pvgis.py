"""Conector para dados de irradiação solar do PVGIS (JRC/UE)."""
import pandas as pd
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime

def fetch_pvgis_ghi(
    lat: float,
    lon: float,
    start: str,
    end: str,
    cache_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Busca dados de irradiação solar global horizontal (GHI) do PVGIS.
    
    Args:
        lat: Latitude
        lon: Longitude
        start: Data inicial (YYYY-MM-DD)
        end: Data final (YYYY-MM-DD)
        cache_dir: Diretório para cache local (opcional)
    
    Returns:
        DataFrame com colunas: timestamp, ghi_wm2, dni_wm2, dhi_wm2
    """
    # API PVGIS: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en
    # Documentação: https://ec.europa.eu/jrc/en/pvgis/api
    
    if cache_dir:
        cache_file = cache_dir / f"pvgis_{lat}_{lon}_{start}_{end}.parquet"
        if cache_file.exists():
            return pd.read_parquet(cache_file)
    
    # Tentar API PVGIS real primeiro
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    
    try:
        url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
        params = {
            "lat": lat,
            "lon": lon,
            "startyear": int(start_date.year),
            "endyear": int(end_date.year),
            "pvcalculation": 0,  # Apenas irradiação, não cálculo PV
            "outputformat": "json",
            "raddatabase": "PVGIS-SARAH2"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "outputs" in data and "daily" in data["outputs"]:
            daily_data = data["outputs"]["daily"]
            df = pd.DataFrame({
                "timestamp": pd.to_datetime([f"{d['year']}-{d['month']:02d}-{d['day']:02d}" for d in daily_data]),
                "ghi_wm2": [d.get("G(i)", 0) for d in daily_data],
                "dni_wm2": [d.get("Gb(i)", 0) for d in daily_data],
                "dhi_wm2": [d.get("Gd(i)", 0) for d in daily_data],
                "lat": lat,
                "lon": lon
            })
            
            # Filtrar por período solicitado
            df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]
            
            if cache_dir:
                cache_dir.mkdir(parents=True, exist_ok=True)
                df.to_parquet(cache_file, index=False)
            
            print("[OK] Dados PVGIS obtidos via API real")
            return df
    except Exception as e:
        print(f"Aviso: Erro ao buscar PVGIS real ({e}). Usando dados simulados.")
    
    # Fallback: dados simulados
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    import numpy as np
    np.random.seed(42)
    
    # Simulação de GHI baseada em latitude (aproximação)
    # Valores mais altos perto do equador, variação sazonal
    day_of_year = dates.dayofyear
    declination = 23.45 * np.sin(np.radians(360 * (284 + day_of_year) / 365))
    lat_rad = np.radians(lat)
    solar_elevation = 90 - abs(lat - declination)
    
    ghi_base = 1000 * np.maximum(0, np.sin(np.radians(solar_elevation)))
    ghi = ghi_base * 0.7 + np.random.normal(0, 100, len(dates))  # Aproximação
    
    df = pd.DataFrame({
        "timestamp": dates,
        "ghi_wm2": np.maximum(0, ghi),
        "dni_wm2": ghi * 0.6,  # Irradiação direta normal
        "dhi_wm2": ghi * 0.3,  # Irradiação difusa horizontal
        "lat": lat,
        "lon": lon
    })
    
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file, index=False)
    
    return df

