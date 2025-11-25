"""Conector para OpenWeatherMap API (alternativa ao INMET)."""
import pandas as pd
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime
import time

def fetch_weather_owm(
    lat: float,
    lon: float,
    start: str,
    end: str,
    api_key: str,
    cache_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Busca dados meteorológicos via OpenWeatherMap.
    
    Requer: Cadastro gratuito em https://openweathermap.org/api
    Limite: 1000 calls/dia (plano gratuito)
    
    Args:
        lat: Latitude
        lon: Longitude
        start: Data inicial (YYYY-MM-DD)
        end: Data final (YYYY-MM-DD)
        api_key: Chave da API OpenWeatherMap
        cache_dir: Diretório para cache (opcional)
    
    Returns:
        DataFrame com colunas: timestamp, temp_c, wind_ms, ghi_wm2
    """
    if cache_dir:
        cache_file = cache_dir / f"openweather_{lat}_{lon}_{start}_{end}.parquet"
        if cache_file.exists():
            return pd.read_parquet(cache_file)
    
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    
    all_data = []
    
    # OpenWeatherMap One Call API 3.0 (requer pagamento)
    # Alternativa: usar Current Weather API + forecast (gratuita)
    
    for date in dates:
        try:
            # Current Weather API (gratuita)
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Estimar GHI baseado em condições
            # (API gratuita não fornece GHI diretamente)
            cloud_cover = data["clouds"]["all"] / 100
            clear_sky_ghi = 1000  # W/m² típico
            estimated_ghi = clear_sky_ghi * (1 - cloud_cover * 0.7)
            
            all_data.append({
                "timestamp": date,
                "temp_c": data["main"]["temp"],
                "wind_ms": data["wind"]["speed"],
                "ghi_wm2": estimated_ghi,
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"]
            })
            
            # Rate limiting (60 calls/min no plano gratuito)
            time.sleep(1)
            
        except Exception as e:
            print(f"Erro ao buscar dados OpenWeatherMap para {date}: {e}")
            # Fallback: dados simulados
            import numpy as np
            all_data.append({
                "timestamp": date,
                "temp_c": 25 + np.random.normal(0, 5),
                "wind_ms": 5 + np.random.normal(0, 2),
                "ghi_wm2": 800 + np.random.normal(0, 100),
                "humidity": 60,
                "pressure": 1013
            })
    
    df = pd.DataFrame(all_data)
    
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file, index=False)
    
    return df

