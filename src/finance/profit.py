"""Análise financeira e cálculo de lucro com PLD."""
import pandas as pd
import numpy as np
from typing import Optional

class ProfitCalculator:
    """
    Calculadora de lucro considerando PLD e preços fixos.
    """
    
    def __init__(
        self,
        sell_price_brl_per_kwh: float = 0.75,
        buy_price_brl_per_kwh: float = 0.90,
        cost_rate: float = 0.10,
        use_pld: bool = True
    ):
        """
        Args:
            sell_price_brl_per_kwh: Preço de venda fixo (R$/kWh)
            buy_price_brl_per_kwh: Preço de compra fixo (R$/kWh)
            cost_rate: Taxa de custo fixo (% sobre receita/custo)
            use_pld: Se True, usa PLD quando disponível
        """
        self.sell_price = sell_price_brl_per_kwh
        self.buy_price = buy_price_brl_per_kwh
        self.cost_rate = cost_rate
        self.use_pld = use_pld
    
    def calculate(
        self,
        consumption: pd.Series,
        production: pd.Series,
        pld_brl_mwh: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Calcula lucro líquido considerando excedente e déficit.
        
        Args:
            consumption: Série de consumo previsto (kWh)
            production: Série de produção prevista (kWh)
            pld_brl_mwh: Série de PLD em BRL/MWh (opcional)
        
        Returns:
            DataFrame com resultados financeiros padronizados
        """
        results = []
        
        for i in range(len(consumption)):
            c = consumption.iloc[i] if hasattr(consumption, 'iloc') else consumption[i]
            p = production.iloc[i] if hasattr(production, 'iloc') else production[i]
            
            surplus_kwh = max(0, p - c)
            deficit_kwh = max(0, c - p)
            
            # Determinar preços
            if self.use_pld and pld_brl_mwh is not None:
                pld_kwh = pld_brl_mwh.iloc[i] / 1000 if hasattr(pld_brl_mwh, 'iloc') else pld_brl_mwh[i] / 1000
                sell_price = pld_kwh * 0.9  # PLD com desconto de 10%
                buy_price = pld_kwh * 1.1   # PLD com acréscimo de 10%
            else:
                sell_price = self.sell_price
                buy_price = self.buy_price
            
            # Calcular receitas e custos
            sell_revenue_brl = surplus_kwh * sell_price
            buy_cost_brl = deficit_kwh * buy_price
            
            # Custos fixos
            fixed_cost = (sell_revenue_brl + buy_cost_brl) * self.cost_rate
            
            # Lucro líquido
            net_profit_brl = sell_revenue_brl - buy_cost_brl - fixed_cost
            
            # Decisão
            if surplus_kwh > 0:
                decision = "Vender"
            elif deficit_kwh > 0:
                decision = "Comprar"
            else:
                decision = "Neutro"
            
            results.append({
                "consumption_kwh": c,
                "production_kwh": p,
                "surplus_kwh": surplus_kwh,
                "deficit_kwh": deficit_kwh,
                "sell_revenue_brl": sell_revenue_brl,
                "buy_cost_brl": buy_cost_brl,
                "fixed_cost_brl": fixed_cost,
                "net_profit_brl": net_profit_brl,
                "decision": decision
            })
        
        return pd.DataFrame(results)

