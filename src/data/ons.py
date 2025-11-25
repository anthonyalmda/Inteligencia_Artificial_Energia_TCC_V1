"""Conector para dados do ONS (Operador Nacional do Sistema Elétrico)."""
import pandas as pd
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime

def fetch_ons_load(
    region: str,
    start: str,
    end: str,
    cache_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Busca dados de carga/geração do ONS.
    
    Args:
        region: Região (SE, S, NE, N, CO)
        start: Data inicial (YYYY-MM-DD)
        end: Data final (YYYY-MM-DD)
        cache_dir: Diretório para cache local (opcional)
    
    Returns:
        DataFrame com colunas: timestamp, load_mw, generation_mw, etc.
    """
    # Portal: https://dados.ons.org.br/
    # Catálogo: https://dados.ons.org.br/dataset/
    # Carga diária: https://dados.ons.org.org/dataset/carga-energia
    
    if cache_dir:
        cache_file = cache_dir / f"ons_load_{region}_{start}_{end}.parquet"
        if cache_file.exists():
            return pd.read_parquet(cache_file)
    
    # Placeholder: dados simulados
    # Em produção, implementar via API CKAN ou download de CSV/Parquet
    # Exemplo: usar requests para acessar API CKAN do ONS
    
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    
    import numpy as np
    np.random.seed(42)
    
    # Simulação de carga com padrão semanal
    load_base = 50000  # MW
    weekly_pattern = np.sin(np.arange(len(dates)) * 2 * np.pi / 7)
    
    df = pd.DataFrame({
        "timestamp": dates,
        "load_mw": load_base + weekly_pattern * 5000 + np.random.normal(0, 1000, len(dates)),
        "generation_mw": load_base * 0.95 + np.random.normal(0, 2000, len(dates)),
        "region": region
    })
    
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file, index=False)
    
    return df

