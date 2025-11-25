"""Módulo para geração de gráficos e visualizações."""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Optional

def plot_forecast_comparison(
    consumption: pd.Series,
    production: pd.Series,
    consumption_pred: Optional[pd.Series] = None,
    production_pred: Optional[pd.Series] = None,
    save_path: Optional[Path] = None,
    title: str = "Previsão de Consumo vs Produção"
) -> plt.Figure:
    """
    Plota comparação entre valores reais e previstos de consumo e produção.
    
    Args:
        consumption: Série de consumo (histórico ou previsto)
        production: Série de produção (histórico ou previsto)
        consumption_pred: Série de consumo previsto (opcional)
        production_pred: Série de produção prevista (opcional)
        save_path: Caminho para salvar figura (opcional)
        title: Título do gráfico
    
    Returns:
        Figura matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    periods = range(len(consumption))
    
    # Plotar valores históricos
    ax.plot(periods, consumption, label="Consumo", marker="o", linestyle="-", linewidth=2)
    ax.plot(periods, production, label="Produção", marker="s", linestyle="-", linewidth=2)
    
    # Plotar previsões se disponíveis
    if consumption_pred is not None:
        start_idx = len(consumption)
        pred_periods = range(start_idx, start_idx + len(consumption_pred))
        ax.plot(pred_periods, consumption_pred, label="Consumo Previsto", 
                marker="o", linestyle="--", linewidth=2, color='blue', alpha=0.7)
    
    if production_pred is not None:
        if consumption_pred is None:
            start_idx = len(consumption)
        else:
            start_idx = len(consumption)
        pred_periods = range(start_idx, start_idx + len(production_pred))
        ax.plot(pred_periods, production_pred, label="Produção Prevista", 
                marker="s", linestyle="--", linewidth=2, color='orange', alpha=0.7)
    
    ax.set_xlabel("Período", fontsize=12)
    ax.set_ylabel("Energia (kWh)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {save_path}")
    
    return fig

def plot_surplus_deficit(
    results_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    title: str = "Excedente vs Déficit"
) -> plt.Figure:
    """
    Plota gráfico de barras mostrando excedente e déficit.
    
    Args:
        results_df: DataFrame com colunas 'surplus_kwh' e 'deficit_kwh'
        save_path: Caminho para salvar figura (opcional)
        title: Título do gráfico
    
    Returns:
        Figura matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    periods = range(len(results_df))
    surplus = results_df["surplus_kwh"].values
    deficit = results_df["deficit_kwh"].values
    
    # Barras de excedente (verde) e déficit (vermelho)
    ax.bar(periods, surplus, label="Excedente (Venda)", color='green', alpha=0.7)
    ax.bar(periods, -deficit, label="Déficit (Compra)", color='red', alpha=0.7)
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    ax.set_xlabel("Período", fontsize=12)
    ax.set_ylabel("Energia (kWh)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {save_path}")
    
    return fig

def plot_cumulative_profit(
    results_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    title: str = "Lucro Líquido Acumulado"
) -> plt.Figure:
    """
    Plota lucro líquido acumulado ao longo do tempo.
    
    Args:
        results_df: DataFrame com coluna 'net_profit_brl'
        save_path: Caminho para salvar figura (opcional)
        title: Título do gráfico
    
    Returns:
        Figura matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    periods = range(len(results_df))
    cumulative_profit = results_df["net_profit_brl"].cumsum()
    
    # Plotar linha e área preenchida
    ax.plot(periods, cumulative_profit, marker="o", linewidth=2, markersize=6)
    ax.fill_between(periods, 0, cumulative_profit, 
                     where=(cumulative_profit >= 0), color='green', alpha=0.3, label="Lucro")
    ax.fill_between(periods, 0, cumulative_profit, 
                     where=(cumulative_profit < 0), color='red', alpha=0.3, label="Prejuízo")
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    ax.set_xlabel("Período", fontsize=12)
    ax.set_ylabel("Lucro Acumulado (R$)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    # Adicionar valor final
    final_profit = cumulative_profit.iloc[-1]
    ax.text(len(periods) - 1, final_profit, f'R$ {final_profit:.2f}', 
            verticalalignment='bottom' if final_profit >= 0 else 'top', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {save_path}")
    
    return fig

def plot_pld_timeseries(
    pld_df: pd.DataFrame,
    save_path: Optional[Path] = None,
    title: str = "Evolução do PLD"
) -> plt.Figure:
    """
    Plota série temporal do PLD.
    
    Args:
        pld_df: DataFrame com coluna 'pld_brl_mwh' e 'timestamp'
        save_path: Caminho para salvar figura (opcional)
        title: Título do gráfico
    
    Returns:
        Figura matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if "timestamp" in pld_df.columns:
        ax.plot(pld_df["timestamp"], pld_df["pld_brl_mwh"], marker="o", linewidth=2)
    else:
        periods = range(len(pld_df))
        ax.plot(periods, pld_df["pld_brl_mwh"], marker="o", linewidth=2)
    
    ax.set_xlabel("Data", fontsize=12)
    ax.set_ylabel("PLD (R$/MWh)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {save_path}")
    
    return fig
