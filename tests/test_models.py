"""Testes básicos para modelos de previsão."""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.consumption import ConsumptionForecaster
from src.models.production import ProductionForecaster

def test_consumption_forecaster_baseline():
    """Teste do forecaster de consumo (baseline)."""
    model = ConsumptionForecaster(algo="baseline")
    
    # Criar dados de treino
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    df = pd.DataFrame({
        "timestamp": dates,
        "consumption_kwh": 100 + 20 * np.sin(np.arange(100) * 2 * np.pi / 7) + np.random.normal(0, 5, 100)
    })
    
    model.fit(df, target_col="consumption_kwh")
    
    predictions = model.predict(horizon=10)
    
    assert len(predictions) == 10
    assert all(predictions > 0)  # Consumo deve ser positivo

def test_production_forecaster_baseline():
    """Teste do forecaster de produção (baseline)."""
    model = ProductionForecaster(algo="baseline")
    
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    df = pd.DataFrame({
        "timestamp": dates,
        "production_kwh": 90 + 25 * np.sin(np.arange(100) * 2 * np.pi / 365) + np.random.normal(0, 10, 100)
    })
    
    model.fit(df, target_col="production_kwh")
    
    predictions = model.predict(horizon=10)
    
    assert len(predictions) == 10
    assert all(predictions >= 0)  # Produção não pode ser negativa

def test_model_not_fitted_error():
    """Teste de erro quando modelo não foi treinado."""
    model = ConsumptionForecaster()
    
    with pytest.raises(ValueError, match="não foi treinado"):
        model.predict(horizon=10)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

