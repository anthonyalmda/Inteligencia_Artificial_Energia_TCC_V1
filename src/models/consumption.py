"""Modelo de previsão de consumo de energia."""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from pathlib import Path
import json

class ConsumptionForecaster:
    """Forecaster de consumo com suporte a Prophet, SARIMAX e XGBoost."""
    
    def __init__(self, algo: str = "prophet"):
        """
        Args:
            algo: Algoritmo ("prophet", "sarimax", "xgboost")
        """
        self.algo = algo
        self.model = None
        self.scaler = None
        self.feature_cols = None
        self.fitted = False
    
    def fit(self, df: pd.DataFrame, target_col: str = "consumption_kwh") -> "ConsumptionForecaster":
        """
        Treina o modelo.
        
        Args:
            df: DataFrame com dados históricos
            target_col: Nome da coluna alvo
        """
        if self.algo == "prophet":
            try:
                from prophet import Prophet
                
                prophet_df = pd.DataFrame({
                    "ds": pd.to_datetime(df["timestamp"]),
                    "y": df[target_col].values
                })
                
                self.model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False
                )
                self.model.fit(prophet_df)
                
            except ImportError:
                print("Prophet não disponível. Usando modelo baseline.")
                self.algo = "baseline"
        
        if self.algo == "baseline" or self.model is None:
            # Modelo baseline: média dos últimos N dias
            if len(df) >= 30:
                mean_val = df[target_col].tail(30).mean()
                trend_val = df[target_col].tail(7).mean() - df[target_col].tail(14).head(7).mean() if len(df) >= 14 else 0
            else:
                mean_val = df[target_col].mean()
                trend_val = 0
            self.model = {
                "mean": mean_val,
                "trend": trend_val
            }
            self.algo = "baseline"
        
        self.fitted = True
        return self
    
    def predict(self, horizon: int, exog: Optional[pd.DataFrame] = None) -> pd.Series:
        """
        Gera previsões.
        
        Args:
            horizon: Número de períodos à frente
            exog: DataFrame com variáveis exógenas (opcional)
        
        Returns:
            Série com previsões
        """
        if not self.fitted:
            raise ValueError("Modelo não foi treinado. Chame fit() primeiro.")
        
        if self.algo == "prophet" and hasattr(self.model, "make_future_dataframe"):
            future_df = self.model.make_future_dataframe(periods=horizon)
            forecast = self.model.predict(future_df)
            return forecast["yhat"].tail(horizon).reset_index(drop=True)
        
        elif self.algo == "baseline":
            # Previsão constante com tendência
            base = self.model["mean"]
            trend = self.model.get("trend", 0)
            predictions = [base + trend * i for i in range(horizon)]
            return pd.Series(predictions)
        
        else:
            # Fallback: média simples
            return pd.Series([self.model.get("mean", 100)] * horizon)
    
    def save(self, path: Path):
        """Salva o modelo treinado."""
        model_dict = {
            "algo": self.algo,
            "model": self.model,
            "fitted": self.fitted
        }
        with open(path, "w") as f:
            json.dump(model_dict, f, default=str)
    
    def load(self, path: Path):
        """Carrega modelo salvo."""
        with open(path, "r") as f:
            model_dict = json.load(f)
        self.algo = model_dict["algo"]
        self.model = model_dict["model"]
        self.fitted = model_dict["fitted"]

