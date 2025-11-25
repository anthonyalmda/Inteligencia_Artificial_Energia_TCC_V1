"""Engenharia de atributos para modelos de previsão."""
import pandas as pd
import numpy as np
from typing import List, Optional

def create_lag_features(
    df: pd.DataFrame,
    column: str,
    lags: List[int],
    groupby: Optional[str] = None
) -> pd.DataFrame:
    """
    Cria features de lag para séries temporais.
    
    Args:
        df: DataFrame com coluna temporal
        column: Nome da coluna para criar lags
        lags: Lista de lags (ex: [1, 2, 3, 7, 14, 24])
        groupby: Coluna para agrupar (opcional, ex: por região)
    
    Returns:
        DataFrame com colunas de lag adicionadas
    """
    df = df.copy()
    
    if groupby:
        for lag in lags:
            df[f"{column}_lag{lag}"] = df.groupby(groupby)[column].shift(lag)
    else:
        for lag in lags:
            df[f"{column}_lag{lag}"] = df[column].shift(lag)
    
    return df

def create_rolling_features(
    df: pd.DataFrame,
    column: str,
    windows: List[int],
    functions: List[str] = ["mean", "std"],
    groupby: Optional[str] = None
) -> pd.DataFrame:
    """
    Cria features de janelas móveis.
    
    Args:
        df: DataFrame
        column: Nome da coluna
        windows: Lista de janelas (ex: [7, 14, 30])
        functions: Funções estatísticas (mean, std, min, max)
        groupby: Coluna para agrupar (opcional)
    
    Returns:
        DataFrame com features de janela móvel
    """
    df = df.copy()
    
    for window in windows:
        if groupby:
            rolling = df.groupby(groupby)[column].rolling(window=window, min_periods=1)
        else:
            rolling = df[column].rolling(window=window, min_periods=1)
        
        for func in functions:
            if func == "mean":
                df[f"{column}_rolling{window}_mean"] = rolling.mean().values
            elif func == "std":
                df[f"{column}_rolling{window}_std"] = rolling.std().values
            elif func == "min":
                df[f"{column}_rolling{window}_min"] = rolling.min().values
            elif func == "max":
                df[f"{column}_rolling{window}_max"] = rolling.max().values
    
    return df

def create_calendar_features(df: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """
    Cria features de calendário (dia da semana, mês, feriados, etc.).
    
    Args:
        df: DataFrame com coluna temporal
        timestamp_col: Nome da coluna de timestamp
    
    Returns:
        DataFrame com features de calendário
    """
    df = df.copy()
    
    if timestamp_col in df.columns:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
        df["day_of_week"] = df[timestamp_col].dt.dayofweek
        df["month"] = df[timestamp_col].dt.month
        df["day_of_month"] = df[timestamp_col].dt.day
        df["week_of_year"] = df[timestamp_col].dt.isocalendar().week
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
        df["is_month_start"] = df[timestamp_col].dt.is_month_start.astype(int)
        df["is_month_end"] = df[timestamp_col].dt.is_month_end.astype(int)
        
        # Features cíclicas (sin/cos)
        df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    
    return df

def create_climate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features derivadas de dados climáticos.
    
    Args:
        df: DataFrame com colunas climáticas (temp_c, ghi_wm2, wind_ms)
    
    Returns:
        DataFrame com features climáticas adicionais
    """
    df = df.copy()
    
    if "ghi_wm2" in df.columns:
        # Índice de claridade (clarity index)
        df["clearness_index"] = df["ghi_wm2"] / 1000  # Normalizado
        df["ghi_lag1"] = df["ghi_wm2"].shift(1)
        df["ghi_rolling7_mean"] = df["ghi_wm2"].rolling(7, min_periods=1).mean()
    
    if "temp_c" in df.columns:
        df["temp_lag1"] = df["temp_c"].shift(1)
        df["temp_rolling7_mean"] = df["temp_c"].rolling(7, min_periods=1).mean()
    
    return df

def engineer_features(
    df: pd.DataFrame,
    target_col: str,
    timestamp_col: str = "timestamp",
    lags: List[int] = [1, 2, 3, 7, 14, 24],
    windows: List[int] = [7, 14, 30],
    include_climate: bool = True,
    include_calendar: bool = True
) -> pd.DataFrame:
    """
    Pipeline completo de engenharia de atributos.
    
    Args:
        df: DataFrame de entrada
        target_col: Coluna alvo para criar features
        timestamp_col: Coluna de timestamp
        lags: Lags a criar
        windows: Janelas móveis
        include_climate: Incluir features climáticas
        include_calendar: Incluir features de calendário
    
    Returns:
        DataFrame com todas as features
    """
    df = df.copy()
    
    # Ordenar por timestamp
    if timestamp_col in df.columns:
        df = df.sort_values(timestamp_col).reset_index(drop=True)
    
    # Features de lag
    df = create_lag_features(df, target_col, lags)
    
    # Features de janela móvel
    df = create_rolling_features(df, target_col, windows, ["mean", "std"])
    
    # Features de calendário
    if include_calendar:
        df = create_calendar_features(df, timestamp_col)
    
    # Features climáticas
    if include_climate:
        df = create_climate_features(df)
    
    return df

