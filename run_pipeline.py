#!/usr/bin/env python3
"""
Pipeline principal para previsão de consumo e produção de energia.
Integra carregamento de dados, previsão, análise financeira e visualização.
"""
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import yaml
import pandas as pd
import numpy as np

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_data_with_fallback
from src.models.consumption import ConsumptionForecaster
from src.models.production import ProductionForecaster
from src.finance.profit import ProfitCalculator
from src.rules.engine import DecisionEngine
from src.viz.plots import plot_forecast_comparison, plot_surplus_deficit, plot_cumulative_profit, plot_pld_timeseries
from src.config.schemas import FinanceParams

def load_config(config_path: Path = None) -> dict:
    """Carrega configuração do arquivo YAML."""
    if config_path is None:
        config_path = Path(__file__).parent / "config" / "default.yaml"
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def prepare_data(
    consumption_df: pd.DataFrame,
    production_df: pd.DataFrame,
    pld_df: pd.DataFrame,
    climate_df: pd.DataFrame
) -> tuple:
    """Prepara e combina dados para modelagem."""
    # Garantir que timestamp está presente
    for df in [consumption_df, production_df, pld_df, climate_df]:
        if df is not None and 'timestamp' not in df.columns:
            if 'date' in df.columns:
                df['timestamp'] = pd.to_datetime(df['date'])
            else:
                df['timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
    
    # Merge dos dados
    combined = consumption_df.copy()
    
    if production_df is not None:
        combined = combined.merge(
            production_df[['timestamp', 'production_kwh']],
            on='timestamp',
            how='outer',
            suffixes=('', '_prod')
        )
    
    if pld_df is not None:
        combined = combined.merge(
            pld_df[['timestamp', 'pld_brl_mwh']],
            on='timestamp',
            how='left'
        )
    
    if climate_df is not None:
        climate_cols = ['timestamp'] + [c for c in climate_df.columns if c != 'timestamp']
        combined = combined.merge(
            climate_df[climate_cols],
            on='timestamp',
            how='left'
        )
    
    # Ordenar por timestamp
    combined = combined.sort_values('timestamp').reset_index(drop=True)
    
    # Preencher valores faltantes
    combined = combined.ffill().bfill()
    
    return combined

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline de previsão de energia com análise financeira",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/default.yaml"),
        help="Caminho para arquivo de configuração YAML"
    )
    
    parser.add_argument(
        "--horizon",
        type=int,
        default=14,
        help="Horizonte de previsão em dias"
    )
    
    parser.add_argument(
        "--region",
        type=str,
        default="SE",
        help="Região (SE, S, NE, N, CO)"
    )
    
    parser.add_argument(
        "--submercado",
        type=str,
        default="SE",
        help="Submercado (SE, S, NE, N)"
    )
    
    parser.add_argument(
        "--train-start",
        type=str,
        default=None,
        help="Data inicial de treino (YYYY-MM-DD). Se não especificado, usa 90 dias atrás"
    )
    
    parser.add_argument(
        "--train-end",
        type=str,
        default=None,
        help="Data final de treino (YYYY-MM-DD). Se não especificado, usa hoje"
    )
    
    parser.add_argument(
        "--use-real-data",
        action="store_true",
        help="Tentar usar dados reais (fallback para simulado)"
    )
    
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Usar cache de dados"
    )
    
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Não abrir interface gráfica"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Diretório para salvar resultados"
    )
    
    parser.add_argument(
        "--inmet-station",
        type=str,
        default=None,
        help="ID da estação INMET (ex: A701)"
    )
    
    parser.add_argument(
        "--lat",
        type=float,
        default=None,
        help="Latitude para PVGIS (ex: -23.5505)"
    )
    
    parser.add_argument(
        "--lon",
        type=float,
        default=None,
        help="Longitude para PVGIS (ex: -46.6333)"
    )
    
    args = parser.parse_args()
    
    # Carregar configuração
    config = load_config(args.config)
    
    # Mesclar argumentos CLI com config
    region = args.region or config.get('data', {}).get('region', 'SE')
    submercado = args.submercado or config.get('data', {}).get('submercado', 'SE')
    horizon = args.horizon or config.get('model', {}).get('horizon_days', 14)
    inmet_station = args.inmet_station or config.get('data', {}).get('inmet_station', 'A701')
    
    # Datas
    end_date = datetime.now()
    if args.train_end:
        end_date = datetime.strptime(args.train_end, '%Y-%m-%d')
    
    start_date = end_date - timedelta(days=90)
    if args.train_start:
        start_date = datetime.strptime(args.train_start, '%Y-%m-%d')
    
    train_start_str = start_date.strftime('%Y-%m-%d')
    train_end_str = end_date.strftime('%Y-%m-%d')
    
    print("Pipeline de Previsao de Energia")
    print(f"=" * 60)
    print(f"Região: {region}")
    print(f"Submercado: {submercado}")
    print(f"Período de treino: {train_start_str} a {train_end_str}")
    print(f"Horizonte de previsão: {horizon} dias")
    print(f"=" * 60)
    
    # Criar diretório de resultados
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Cache dir
    cache_dir = None
    if args.cache or config.get('data', {}).get('cache_dir'):
        cache_dir = Path(config.get('data', {}).get('cache_dir', 'data/raw'))
        cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Carregar dados
    print("\n[1/7] Carregando dados...")
    try:
        # Carregar chave OpenWeatherMap do config
        openweather_key = config.get('data', {}).get('openweather_api_key') or None
        
        consumption_df, production_df, pld_df, climate_df = load_data_with_fallback(
            start=train_start_str,
            end=train_end_str,
            region=region,
            submercado=submercado,
            inmet_station=inmet_station,
            cache_dir=cache_dir,
            use_real_data=args.use_real_data,
            lat=args.lat,
            lon=args.lon,
            openweather_api_key=openweather_key
        )
        print(f"[OK] Dados carregados: {len(consumption_df)} registros")
        
        # Validar dados carregados
        if len(consumption_df) > 0 and 'consumption_kwh' in consumption_df.columns:
            consumo_mean = consumption_df['consumption_kwh'].mean()
            if consumo_mean > 10000:  # Flag para valores absurdos
                print(f"[AVISO] Valores de consumo muito altos detectados ({consumo_mean:.2f} kWh/dia)")
                print("[AVISO] Valores esperados: 50-200 kWh/dia. Verifique a origem dos dados.")
            elif consumo_mean < 1:
                print(f"[AVISO] Valores de consumo muito baixos detectados ({consumo_mean:.2f} kWh/dia)")
                print("[AVISO] Verifique a origem dos dados.")
        
        if production_df is not None and len(production_df) > 0 and 'production_kwh' in production_df.columns:
            producao_mean = production_df['production_kwh'].mean()
            if producao_mean > 100000:
                print(f"[AVISO] Valores de producao muito altos detectados ({producao_mean:.2f} kWh/dia)")
                print("[AVISO] Valores esperados: 0-300 kWh/dia. Verifique a origem dos dados.")
    except Exception as e:
        print(f"[ERRO] Erro ao carregar dados: {e}")
        return 1
    
    # 2. Preparar dados combinados
    print("\n[2/7] Preparando dados...")
    try:
        combined_df = prepare_data(consumption_df, production_df, pld_df, climate_df)
        print(f"[OK] Dados preparados: {len(combined_df)} registros, {len(combined_df.columns)} colunas")
        
        # Estatísticas descritivas dos dados históricos
        if len(combined_df) > 0:
            print("\nEstatisticas dos dados historicos:")
            stats_cols = ['consumption_kwh', 'production_kwh']
            available_cols = [col for col in stats_cols if col in combined_df.columns]
            if available_cols:
                stats_df = combined_df[available_cols].describe()
                print(stats_df.to_string())
    except Exception as e:
        print(f"[ERRO] Erro ao preparar dados: {e}")
        return 1
    
    # 3. Treinar modelos
    print("\n[3/7] Treinando modelos...")
    algo_consumption = config.get('model', {}).get('algo_consumption', 'prophet')
    algo_production = config.get('model', {}).get('algo_production', 'xgboost')
    
    try:
        consumption_model = ConsumptionForecaster(algo=algo_consumption)
        consumption_model.fit(combined_df, target_col='consumption_kwh')
        print(f"[OK] Modelo de consumo treinado ({algo_consumption})")
        
        production_model = ProductionForecaster(algo=algo_production)
        exog_cols = ['ghi_wm2', 'temp_c'] if 'ghi_wm2' in combined_df.columns else None
        production_model.fit(combined_df, target_col='production_kwh', exog_cols=exog_cols)
        print(f"[OK] Modelo de producao treinado ({algo_production})")
        
        # Validação no conjunto de treino (últimos 7-14 dias)
        if len(combined_df) >= 14:
            try:
                from src.models.evaluate import calculate_metrics
                
                print("\n[VALIDACAO] Avaliando qualidade do modelo no conjunto de treino...")
                val_size = min(7, len(combined_df) // 4)
                
                if val_size > 0 and len(combined_df) > val_size:
                    train_df = combined_df.iloc[:-val_size].copy()
                    val_df = combined_df.iloc[-val_size:].copy()
                    
                    # Validar modelo de consumo
                    if 'consumption_kwh' in val_df.columns and len(val_df) > 0:
                        try:
                            temp_cons_model = ConsumptionForecaster(algo=algo_consumption)
                            temp_cons_model.fit(train_df, target_col='consumption_kwh')
                            val_cons_pred = temp_cons_model.predict(val_size)
                            
                            # Converter para Series se necessário
                            if not isinstance(val_cons_pred, pd.Series):
                                val_cons_pred = pd.Series(val_cons_pred)
                            
                            # Garantir mesmo tamanho
                            min_len = min(len(val_df), len(val_cons_pred))
                            val_cons_true = pd.Series(val_df['consumption_kwh'].values[:min_len])
                            val_cons_pred_trim = pd.Series(val_cons_pred.values[:min_len] if hasattr(val_cons_pred, 'values') else val_cons_pred[:min_len])
                            
                            if len(val_cons_true) > 0 and len(val_cons_pred_trim) > 0:
                                cons_metrics = calculate_metrics(val_cons_true, val_cons_pred_trim)
                                print(f"  Consumo - MAE: {cons_metrics['MAE']:.2f} kWh, RMSE: {cons_metrics['RMSE']:.2f} kWh")
                                print(f"  Consumo - MAPE: {cons_metrics['MAPE']:.2f}%, R²: {cons_metrics['R2']:.3f}")
                        except Exception as e:
                            print(f"  [AVISO] Nao foi possivel validar modelo de consumo: {e}")
                    
                    # Validar modelo de produção
                    if 'production_kwh' in val_df.columns and len(val_df) > 0:
                        try:
                            temp_prod_model = ProductionForecaster(algo=algo_production)
                            temp_prod_model.fit(train_df, target_col='production_kwh', exog_cols=exog_cols)
                            
                            # Preparar exógenas para validação
                            val_exog = None
                            if exog_cols:
                                val_exog = val_df[exog_cols] if all(col in val_df.columns for col in exog_cols) else None
                            
                            val_prod_pred = temp_prod_model.predict(val_size, exog=val_exog)
                            
                            # Converter para Series se necessário
                            if not isinstance(val_prod_pred, pd.Series):
                                val_prod_pred = pd.Series(val_prod_pred)
                            
                            # Garantir mesmo tamanho
                            min_len = min(len(val_df), len(val_prod_pred))
                            val_prod_true = pd.Series(val_df['production_kwh'].values[:min_len])
                            val_prod_pred_trim = pd.Series(val_prod_pred.values[:min_len] if hasattr(val_prod_pred, 'values') else val_prod_pred[:min_len])
                            
                            if len(val_prod_true) > 0 and len(val_prod_pred_trim) > 0:
                                prod_metrics = calculate_metrics(val_prod_true, val_prod_pred_trim)
                                print(f"  Producao - MAE: {prod_metrics['MAE']:.2f} kWh, RMSE: {prod_metrics['RMSE']:.2f} kWh")
                                print(f"  Producao - MAPE: {prod_metrics['MAPE']:.2f}%, R²: {prod_metrics['R2']:.3f}")
                        except Exception as e:
                            print(f"  [AVISO] Nao foi possivel validar modelo de producao: {e}")
            except ImportError:
                print("[AVISO] Modulo de avaliacao nao disponivel. Pulando validacao.")
            except Exception as e:
                print(f"[AVISO] Erro na validacao: {e}")
    except Exception as e:
        print(f"[ERRO] Erro ao treinar modelos: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 4. Gerar previsões
    print("\n[4/7] Gerando previsões...")
    try:
        # Preparar dados futuros para exógenas
        future_exog = None
        if exog_cols and pld_df is not None and len(pld_df) >= horizon:
            # Usar últimas observações ou média para previsão
            future_exog = pd.DataFrame({
                col: [combined_df[col].tail(30).mean()] * horizon
                for col in exog_cols if col in combined_df.columns
            })
        
        consumption_pred = consumption_model.predict(horizon)
        production_pred = production_model.predict(horizon, exog=future_exog)
        
        # Garantir que são Series
        if not isinstance(consumption_pred, pd.Series):
            consumption_pred = pd.Series(consumption_pred)
        if not isinstance(production_pred, pd.Series):
            production_pred = pd.Series(production_pred)
        
        print(f"[OK] Previsoes geradas: {len(consumption_pred)} periodos")
    except Exception as e:
        print(f"[ERRO] Erro ao gerar previsoes: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 5. Obter PLD futuro (usar últimas observações ou média)
    print("\n[5/7] Preparando PLD para análise financeira...")
    pld_future = None
    if pld_df is not None and 'pld_brl_mwh' in pld_df.columns:
        pld_recent = pld_df['pld_brl_mwh'].tail(30).values
        if len(pld_recent) > 0:
            # Repetir média dos últimos 30 dias
            pld_avg = np.mean(pld_recent)
            pld_future = pd.Series([pld_avg] * horizon)
    
    # 6. Análise financeira
    print("\n[6/7] Calculando análise financeira...")
    try:
        finance_config = config.get('finance', {})
        calculator = ProfitCalculator(
            sell_price_brl_per_kwh=finance_config.get('sell_price_brl_per_kwh', 0.75),
            buy_price_brl_per_kwh=finance_config.get('buy_price_brl_per_kwh', 0.90),
            cost_rate=finance_config.get('cost_rate', 0.10),
            use_pld=finance_config.get('use_pld', True)
        )
        
        results_df = calculator.calculate(
            consumption_pred,
            production_pred,
            pld_brl_mwh=pld_future
        )
        print(f"[OK] Analise financeira concluida")
        
        # Integrar DecisionEngine
        decision_config = config.get('decisions', {})
        decision_engine = DecisionEngine(
            buffer_kwh=decision_config.get('buffer_kwh', 1.0),
            pld_premium_threshold_brl_mwh=decision_config.get('pld_premium_threshold_brl_mwh', 50.0),
            strategy="economic"
        )
        
        decisions = decision_engine.decide(
            consumption_pred,
            production_pred,
            pld_brl_mwh=pld_future
        )
        
        # Adicionar decisões ao DataFrame
        results_df['decision'] = decisions.values
        
        print(f"[OK] Decisoes geradas: {decisions.value_counts().to_dict()}")
    except Exception as e:
        print(f"[ERRO] Erro na analise financeira: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 7. Salvar resultados
    print("\n[7/7] Salvando resultados...")
    try:
        # Adicionar timestamps futuros
        last_timestamp = combined_df['timestamp'].max()
        future_timestamps = pd.date_range(
            start=last_timestamp + timedelta(days=1),
            periods=horizon,
            freq='D'
        )
        results_df['timestamp'] = future_timestamps
        
        # Salvar CSV
        csv_path = output_dir / "forecast_results.csv"
        results_df.to_csv(csv_path, index=False)
        print(f"[OK] CSV salvo: {csv_path}")
        
        # Salvar Parquet
        parquet_path = output_dir / "forecast_results.parquet"
        results_df.to_parquet(parquet_path, index=False)
        print(f"[OK] Parquet salvo: {parquet_path}")
        
        # Gerar gráficos
        forecast_fig = plot_forecast_comparison(
            consumption=consumption_pred,
            production=production_pred,
            save_path=output_dir / "forecast_comparison.png"
        )
        
        surplus_fig = plot_surplus_deficit(
            results_df,
            save_path=output_dir / "surplus_deficit.png"
        )
        
        profit_fig = plot_cumulative_profit(
            results_df,
            save_path=output_dir / "cumulative_profit.png"
        )
        
        if pld_df is not None and len(pld_df) > 0:
            plot_pld_timeseries(
                pld_df,
                save_path=output_dir / "pld_timeseries.png"
            )
        
        print(f"[OK] Graficos salvos em {output_dir}")
        
        # Resumo expandido
        total_profit = results_df['net_profit_brl'].sum()
        total_surplus = results_df['surplus_kwh'].sum()
        total_deficit = results_df['deficit_kwh'].sum()
        
        # Calcular eficiência energética
        total_consumption = results_df['consumption_kwh'].sum()
        total_production = results_df['production_kwh'].sum()
        efficiency = (total_production / total_consumption * 100) if total_consumption > 0 else 0
        
        # Estatísticas de lucro
        profit_mean = results_df['net_profit_brl'].mean()
        profit_std = results_df['net_profit_brl'].std()
        profit_min = results_df['net_profit_brl'].min()
        profit_max = results_df['net_profit_brl'].max()
        
        # Percentuais de decisões
        decisions_counts = results_df['decision'].value_counts()
        decisions_pct = results_df['decision'].value_counts(normalize=True) * 100
        decisions_pct_dict = {k: float(v) for k, v in dict(decisions_pct).items()}
        
        print(f"\n{'='*60}")
        print("RESUMO DOS RESULTADOS")
        print(f"{'='*60}")
        print(f"\nFINANCEIRO:")
        print(f"  Lucro líquido total: R$ {total_profit:.2f}")
        print(f"  Lucro médio por período: R$ {profit_mean:.2f}")
        print(f"  Desvio padrão: R$ {profit_std:.2f}")
        print(f"  Lucro mínimo: R$ {profit_min:.2f}")
        print(f"  Lucro máximo: R$ {profit_max:.2f}")
        print(f"\nENERGIA:")
        print(f"  Excedente total: {total_surplus:.2f} kWh")
        print(f"  Déficit total: {total_deficit:.2f} kWh")
        print(f"  Consumo médio previsto: {results_df['consumption_kwh'].mean():.2f} kWh/dia")
        print(f"  Produção média prevista: {results_df['production_kwh'].mean():.2f} kWh/dia")
        print(f"  Eficiência energética: {efficiency:.1f}% (produção/consumo)")
        print(f"\nDECISÕES:")
        print(f"  Distribuição: {decisions_counts.to_dict()}")
        print(f"  Percentuais: {decisions_pct_dict}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"[ERRO] Erro ao salvar resultados: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 8. Interface gráfica (opcional)
    if not args.no_gui:
        try:
            print("Abrindo interface gráfica...")
            from src.viz.interface import MainApplication
            app = MainApplication(results_df, output_dir)
            app.mainloop()
        except Exception as e:
            print(f"[AVISO] Erro ao abrir interface grafica: {e}")
            print("Resultados salvos em arquivos CSV/Parquet e imagens PNG.")
    
    print("[OK] Pipeline concluido com sucesso!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
