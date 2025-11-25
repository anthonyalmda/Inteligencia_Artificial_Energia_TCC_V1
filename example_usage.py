#!/usr/bin/env python3
"""
Exemplos de uso do sistema de previsão de energia.
"""
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_data_with_fallback
from src.models.consumption import ConsumptionForecaster
from src.models.production import ProductionForecaster
from src.finance.profit import ProfitCalculator
from src.rules.engine import DecisionEngine
import pandas as pd
from datetime import datetime, timedelta

def example_basic_forecast():
    """Exemplo básico de previsão."""
    print("=" * 60)
    print("EXEMPLO 1: Previsão Básica")
    print("=" * 60)
    
    # Carregar dados
    start = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    
    consumption_df, production_df, pld_df, climate_df = load_data_with_fallback(
        start=start,
        end=end,
        region="SE",
        submercado="SE",
        use_real_data=False  # Usar dados simulados
    )
    
    # Treinar modelos
    print("\nTreinando modelos...")
    consumption_model = ConsumptionForecaster(algo="baseline")
    consumption_model.fit(consumption_df, target_col="consumption_kwh")
    
    production_model = ProductionForecaster(algo="baseline")
    production_model.fit(production_df, target_col="production_kwh")
    
    # Gerar previsões
    horizon = 7
    consumption_pred = consumption_model.predict(horizon)
    production_pred = production_model.predict(horizon)
    
    print(f"\nPrevisões geradas para {horizon} dias:")
    print(f"Consumo médio previsto: {consumption_pred.mean():.2f} kWh")
    print(f"Produção média prevista: {production_pred.mean():.2f} kWh")
    
    return consumption_pred, production_pred

def example_financial_analysis():
    """Exemplo de análise financeira."""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Análise Financeira")
    print("=" * 60)
    
    # Obter previsões
    consumption_pred, production_pred = example_basic_forecast()
    
    # Calcular lucro
    calculator = ProfitCalculator(
        sell_price_brl_per_kwh=0.75,
        buy_price_brl_per_kwh=0.90,
        cost_rate=0.10,
        use_pld=False
    )
    
    results_df = calculator.calculate(consumption_pred, production_pred)
    
    print("\nResultados financeiros:")
    print(results_df[['consumption_kwh', 'production_kwh', 'net_profit_brl', 'decision']])
    
    total_profit = results_df['net_profit_brl'].sum()
    print(f"\nLucro líquido total: R$ {total_profit:.2f}")
    
    return results_df

def example_decision_engine():
    """Exemplo de uso do motor de decisão."""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Motor de Decisão")
    print("=" * 60)
    
    consumption_pred, production_pred = example_basic_forecast()
    
    # Criar PLD simulado
    pld_future = pd.Series([300, 350, 320, 380, 290, 310, 330])  # R$/MWh
    
    # Motor de decisão
    decision_engine = DecisionEngine(
        buffer_kwh=1.0,
        pld_premium_threshold_brl_mwh=50.0,
        strategy="economic"
    )
    
    decisions = decision_engine.decide(
        consumption_pred,
        production_pred,
        pld_brl_mwh=pld_future
    )
    
    print("\nDecisões por período:")
    for i, decision in enumerate(decisions):
        print(f"Período {i+1}: {decision} (Consumo: {consumption_pred.iloc[i]:.2f} kWh, "
              f"Produção: {production_pred.iloc[i]:.2f} kWh, PLD: {pld_future.iloc[i]:.2f} R$/MWh)")
    
    return decisions

def example_with_real_data():
    """Exemplo tentando usar dados reais (com fallback)."""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Tentativa com Dados Reais")
    print("=" * 60)
    
    start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    
    try:
        consumption_df, production_df, pld_df, climate_df = load_data_with_fallback(
            start=start,
            end=end,
            region="SE",
            submercado="SE",
            use_real_data=True,  # Tentar dados reais
            cache_dir=Path("data/raw")
        )
        
        print(f"\nDados carregados:")
        print(f"- Consumo: {len(consumption_df)} registros")
        print(f"- Produção: {len(production_df)} registros")
        print(f"- PLD: {len(pld_df) if pld_df is not None else 0} registros")
        print(f"- Clima: {len(climate_df) if climate_df is not None else 0} registros")
        
        if pld_df is not None and len(pld_df) > 0:
            print(f"\nPLD médio: {pld_df['pld_brl_mwh'].mean():.2f} R$/MWh")
        
    except Exception as e:
        print(f"Erro ao carregar dados reais: {e}")
        print("Usando dados simulados como fallback...")

if __name__ == "__main__":
    print("\nEXEMPLOS DE USO DO SISTEMA DE PREVISAO DE ENERGIA\n")
    
    # Exemplo 1: Previsão básica
    example_basic_forecast()
    
    # Exemplo 2: Análise financeira
    example_financial_analysis()
    
    # Exemplo 3: Motor de decisão
    example_decision_engine()
    
    # Exemplo 4: Dados reais
    example_with_real_data()
    
    print("\n[OK] Exemplos concluidos!\n")
    print("Para executar o pipeline completo:")
    print("  python run_pipeline.py --horizon 14")

