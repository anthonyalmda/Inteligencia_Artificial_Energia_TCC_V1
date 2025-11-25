"""Conector para dados do INMET (Instituto Nacional de Meteorologia)."""
import pandas as pd
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
import time

def fetch_inmet(
    station_id: str,
    start: str,
    end: str,
    cache_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Busca dados meteorológicos do INMET.
    
    Args:
        station_id: ID da estação (ex: "A701")
        start: Data inicial (YYYY-MM-DD)
        end: Data final (YYYY-MM-DD)
        cache_dir: Diretório para cache local (opcional)
    
    Returns:
        DataFrame com colunas: timestamp, temp_c, wind_ms, ghi_wm2, etc.
    """
    # API pública do INMET (tempo.inmet.gov.br)
    # Nota: API real requer implementação específica baseada na documentação
    # Esta é uma estrutura base que pode ser expandida
    
    if cache_dir:
        cache_file = cache_dir / f"inmet_{station_id}_{start}_{end}.parquet"
        if cache_file.exists():
            return pd.read_parquet(cache_file)
    
    # Placeholder: retorna dados simulados se API não estiver disponível
    # Em produção, implementar requisições reais conforme:
    # https://tempo.inmet.gov.br/ ou API de dados abertos
    
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    
    # Dados simulados baseados em padrões sazonais
    import numpy as np
    np.random.seed(42)
    
    df = pd.DataFrame({
        "timestamp": dates,
        "temp_c": 25 + 5 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.normal(0, 2, len(dates)),
        "wind_ms": 5 + 2 * np.random.randn(len(dates)),
        "ghi_wm2": 800 * np.maximum(0, np.sin(np.arange(len(dates)) * np.pi / 365)) + np.random.normal(0, 100, len(dates)),
        "station_id": station_id
    })
    
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file, index=False)
    
    return df

