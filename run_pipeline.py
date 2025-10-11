# run_pipeline.py

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from interface import MainApplication
from src.models.forecasting_consumption.model import ConsumptionForecaster
from src.models.forecasting_production.model import ProductionForecaster
from src.finance.profit_analysis.profit import ProfitCalculator

def main():
    # Criar pasta de resultados
    os.makedirs("results", exist_ok=True)

    dias_para_prever = 10

    # Exemplo de dados simulados (10 períodos)
    consumo_real = [100, 120, 110, 95, 105, 130, 125, 140, 115, 100]
    producao_real = [110, 115, 90, 100, 120, 140, 100, 130, 105, 95]

    # --- Modelos de previsão ---
    consumo_model = ConsumptionForecaster()
    producao_model = ProductionForecaster()

    consumo_prev = consumo_model.predict(dias_para_prever)
    producao_prev = producao_model.predict(dias_para_prever)

    # --- Análise financeira ---
    calculator = ProfitCalculator(sell_price=0.75, buy_price=0.90, cost_rate=0.10)
    df_resultados = calculator.calculate(consumo_prev, producao_prev)

    # Salvar CSV com todas as colunas
    csv_path = "results/forecast_results.csv"
    df_resultados.to_csv(csv_path, index=False)
    print(f"Resultados salvos em {csv_path}")

    # --- Gráfico 1: Consumo vs Produção ---
    plt.figure(figsize=(10, 5))
    plt.plot(consumo_prev, label="Consumo Previsto", marker="o")
    plt.plot(producao_prev, label="Produção Prevista", marker="o")
    plt.title("Previsão de Consumo vs Produção")
    plt.xlabel("Período")
    plt.ylabel("Energia (kWh)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/forecast_graph.png")
    plt.close()
    print("Gráfico 'forecast_graph.png' gerado.")

    # --- Gráfico 2: Excedente vs Déficit ---
    plt.figure(figsize=(10, 5))
    plt.bar(df_resultados.index, df_resultados["Excedente"], label="Excedente (Venda)", color="green")
    plt.bar(df_resultados.index, -df_resultados["Deficit"], label="Déficit (Compra)", color="red")
    plt.title("Excedente vs Déficit")
    plt.xlabel("Período")
    plt.ylabel("Energia (kWh)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/excedente_deficit.png")
    plt.close()
    print("Gráfico 'excedente_deficit.png' gerado.")

    # --- Interface Gráfica ---
    app = MainApplication(df_resultados, "results/forecast_graph.png")
    app.mainloop()

if __name__ == "__main__":
    main()
