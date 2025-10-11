# data_loader.py

from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parents[2]  # aponta para a pasta do projeto (dois níveis acima de src/utils)

def _generate_simulated(dias=100, seed=42, start_date="2024-01-01"):
    np.random.seed(seed)
    start = datetime.fromisoformat(start_date)
    dates = [start + timedelta(days=i) for i in range(dias)]
    consumo = 80 + 20 * np.sin(np.linspace(0, 6.28, dias)) + np.random.normal(0, 5, size=dias)
    producao = 70 + 25 * np.cos(np.linspace(0, 6.28, dias)) + np.random.normal(0, 7, size=dias)
    df_consumo = pd.DataFrame({"date": [d.strftime("%Y-%m-%d") for d in dates], "consumption": consumo.round(2)})
    df_producao = pd.DataFrame({"date": [d.strftime("%Y-%m-%d") for d in dates], "production": producao.round(2)})
    return df_consumo, df_producao

def _read_if_exists(path: Path):
    if path.exists():
        try:
            df = pd.read_csv(path, parse_dates=["date"], dayfirst=False)
            return df
        except Exception as e:
            # Tentativa sem parse_dates se coluna diferente
            df = pd.read_csv(path)
            return df
    return None

def load_from_raw():
    raw_dir = BASE_DIR / "src" / "data" / "raw"
    if not raw_dir.exists():
        return None

    # Procura por arquivos padrão
    consumo_path = raw_dir / "consumption.csv"
    producao_path = raw_dir / "production.csv"

    # Se não existirem com esses nomes, tentar encontrar por padrão
    if not consumo_path.exists():
        # procurar arquivos que contenham 'consum' no nome
        candidates = list(raw_dir.glob("*consum*.csv")) + list(raw_dir.glob("*consumption*.csv"))
        consumo_path = candidates[0] if candidates else consumo_path

    if not producao_path.exists():
        candidates = list(raw_dir.glob("*produc*.csv")) + list(raw_dir.glob("*production*.csv"))
        producao_path = candidates[0] if candidates else producao_path

    df_c = _read_if_exists(consumo_path) if consumo_path.exists() else None
    df_p = _read_if_exists(producao_path) if producao_path.exists() else None

    if df_c is not None and df_p is not None:
        return df_c, df_p
    return None

def load_from_simulation_folder():
    sim_dir = BASE_DIR / "src" / "data" / "simulation"
    if not sim_dir.exists():
        return None
    c = _read_if_exists(sim_dir / "consumption.csv")
    p = _read_if_exists(sim_dir / "production.csv")
    if c is not None and p is not None:
        return c, p
    return None

def load_simulated_data(dias=100, seed=42, start_date="2024-01-01"):
    """Gera e retorna DataFrames simulados em memória (sem salvar em disco)."""
    return _generate_simulated(dias=dias, seed=seed, start_date=start_date)

def load_data(prefer="raw", dias=100, seed=42, start_date="2024-01-01"):
    """
    Tenta carregar dados na ordem:
      1) src/data/raw (se prefer=='raw' ou sempre, dependendo)
      2) src/data/simulation
      3) gera simulado em memória
    Retorna: (df_consumption, df_production)
    """
    # 1) tentar raw, se preferencia raw
    if prefer == "raw":
        raw = load_from_raw()
        if raw:
            return raw

    # 2) tentar sim folder
    sim = load_from_simulation_folder()
    if sim:
        return sim

    # 3) tentar raw mesmo sem prefer (última chance)
    raw = load_from_raw()
    if raw:
        return raw

    # 4) gerar simulado em memória
    return load_simulated_data(dias=dias, seed=seed, start_date=start_date)

