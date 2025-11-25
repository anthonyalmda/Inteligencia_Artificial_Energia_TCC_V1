"""Avaliação de modelos com métricas e backtests."""
import pandas as pd
import numpy as np
try:
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
except ImportError:
    # Fallback se sklearn não estiver instalado
    def mean_absolute_error(y_true, y_pred):
        import numpy as np
        return np.mean(np.abs(y_true - y_pred))
    def mean_squared_error(y_true, y_pred, squared=True):
        import numpy as np
        mse = np.mean((y_true - y_pred) ** 2)
        return np.sqrt(mse) if not squared else mse
    def r2_score(y_true, y_pred):
        import numpy as np
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
from typing import Dict, List

def calculate_metrics(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
    """
    Calcula métricas de avaliação.
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
    
    Returns:
        Dicionário com métricas: MAE, RMSE, MAPE, R²
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    # MAPE com proteção contra divisão por zero
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
    
    r2 = r2_score(y_true, y_pred)
    
    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "R2": r2
    }

def expanding_window_backtest(
    model,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    target_col: str,
    step_size: int = 1
) -> pd.DataFrame:
    """
    Backtest com janela expansiva.
    
    Args:
        model: Modelo com métodos fit() e predict()
        train_df: DataFrame de treino inicial
        test_df: DataFrame de teste
        target_col: Nome da coluna alvo
        step_size: Tamanho do passo (períodos)
    
    Returns:
        DataFrame com previsões e métricas
    """
    predictions = []
    actuals = []
    
    train = train_df.copy()
    
    for i in range(0, len(test_df), step_size):
        # Treinar modelo
        model.fit(train, target_col=target_col)
        
        # Prever próximo passo
        horizon = min(step_size, len(test_df) - i)
        pred = model.predict(horizon)
        actual = test_df[target_col].iloc[i:i+horizon]
        
        predictions.extend(pred)
        actuals.extend(actual)
        
        # Expandir janela de treino
        train = pd.concat([train, test_df.iloc[i:i+horizon]])
    
    results_df = pd.DataFrame({
        "actual": actuals,
        "predicted": predictions
    })
    
    return results_df

