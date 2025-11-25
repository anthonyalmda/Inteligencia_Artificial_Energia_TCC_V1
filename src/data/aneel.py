"""Conector para dados da ANEEL (Agência Nacional de Energia Elétrica)."""
import pandas as pd
import requests
from pathlib import Path
from typing import Optional

def fetch_aneel_gd(cache_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Busca dados de geração distribuída da ANEEL.
    
    Args:
        cache_dir: Diretório para cache local (opcional)
    
    Returns:
        DataFrame com informações de empreendimentos de GD
    """
    # Dataset: https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida
    # CSV direto: https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv
    
    if cache_dir:
        cache_file = cache_dir / "aneel_gd.parquet"
        if cache_file.exists():
            return pd.read_parquet(cache_file)
    
    # Placeholder: retorna DataFrame vazio
    # Em produção, fazer download do CSV e processar
    
    url = "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv"
    
    try:
        df = pd.read_csv(url, encoding='latin-1', sep=';', low_memory=False)
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
            df.to_parquet(cache_file, index=False)
        return df
    except Exception as e:
        print(f"Erro ao buscar dados ANEEL: {e}")
        return pd.DataFrame()  # Retorna vazio em caso de erro

