"""Testes básicos para módulo de análise financeira."""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.finance.profit import ProfitCalculator

def test_profit_calculator_basic():
    """Teste básico do calculador de lucro."""
    calculator = ProfitCalculator(
        sell_price_brl_per_kwh=0.75,
        buy_price_brl_per_kwh=0.90,
        cost_rate=0.10
    )
    
    consumption = pd.Series([100, 120, 80])
    production = pd.Series([110, 100, 90])
    
    results = calculator.calculate(consumption, production)
    
    assert len(results) == 3
    assert 'consumption_kwh' in results.columns
    assert 'production_kwh' in results.columns
    assert 'surplus_kwh' in results.columns
    assert 'deficit_kwh' in results.columns
    assert 'net_profit_brl' in results.columns
    assert 'decision' in results.columns

def test_profit_calculator_with_pld():
    """Teste do calculador com PLD."""
    calculator = ProfitCalculator(
        sell_price_brl_per_kwh=0.75,
        buy_price_brl_per_kwh=0.90,
        cost_rate=0.10,
        use_pld=True
    )
    
    consumption = pd.Series([100, 120])
    production = pd.Series([110, 100])
    pld = pd.Series([300, 350])  # R$/MWh
    
    results = calculator.calculate(consumption, production, pld_brl_mwh=pld)
    
    assert len(results) == 2
    assert results.iloc[0]['surplus_kwh'] > 0  # Primeiro período tem excedente
    assert results.iloc[1]['deficit_kwh'] > 0  # Segundo período tem déficit

def test_profit_calculator_decisions():
    """Teste das decisões geradas."""
    calculator = ProfitCalculator()
    
    consumption = pd.Series([100, 80, 120])
    production = pd.Series([120, 70, 100])
    
    results = calculator.calculate(consumption, production)
    
    assert results.iloc[0]['decision'] == 'Vender'  # Excedente
    assert results.iloc[1]['decision'] == 'Comprar'  # Déficit
    assert results.iloc[2]['decision'] == 'Comprar'  # Déficit

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

