"""Motor de decisão para compra/venda de energia."""
import pandas as pd
import numpy as np
from typing import Optional

class DecisionEngine:
    """
    Motor de decisão que determina estratégia de compra/venda baseado em
    previsões, PLD e regras econômicas.
    """
    
    def __init__(
        self,
        buffer_kwh: float = 1.0,
        pld_premium_threshold_brl_mwh: float = 50.0,
        strategy: str = "economic"
    ):
        """
        Args:
            buffer_kwh: Buffer de segurança (kWh)
            pld_premium_threshold_brl_mwh: Limiar de prêmio PLD (BRL/MWh)
            strategy: Estratégia ("simple", "economic")
        """
        self.buffer_kwh = buffer_kwh
        self.pld_threshold = pld_premium_threshold_brl_mwh / 1000  # Converter para R$/kWh
        self.strategy = strategy
    
    def decide(
        self,
        consumption: pd.Series,
        production: pd.Series,
        pld_brl_mwh: Optional[pd.Series] = None,
        current_pld: Optional[float] = None
    ) -> pd.Series:
        """
        Decide ação (Comprar/Vender/Neutro) para cada período.
        
        Args:
            consumption: Série de consumo previsto
            production: Série de produção prevista
            pld_brl_mwh: Série de PLD (opcional)
            current_pld: PLD atual (opcional)
        
        Returns:
            Série com decisões
        """
        decisions = []
        
        for i in range(len(consumption)):
            c = consumption.iloc[i] if hasattr(consumption, 'iloc') else consumption[i]
            p = production.iloc[i] if hasattr(production, 'iloc') else production[i]
            
            if self.strategy == "simple":
                # Regra simples: produção > consumo → vender
                if p > c + self.buffer_kwh:
                    decision = "Vender"
                elif c > p + self.buffer_kwh:
                    decision = "Comprar"
                else:
                    decision = "Neutro"
            
            elif self.strategy == "economic":
                # Regra econômica: considerar PLD
                surplus = p - c
                
                # Obter PLD atual
                pld = None
                if pld_brl_mwh is not None:
                    pld = pld_brl_mwh.iloc[i] / 1000 if hasattr(pld_brl_mwh, 'iloc') else pld_brl_mwh[i] / 1000
                elif current_pld:
                    pld = current_pld / 1000
                
                if surplus > self.buffer_kwh:
                    # Há excedente
                    if pld and pld > self.pld_threshold:
                        # PLD alto: vender
                        decision = "Vender"
                    else:
                        # PLD baixo: considerar armazenar ou vender
                        decision = "Vender"  # Simplificado
                elif surplus < -self.buffer_kwh:
                    # Há déficit
                    if pld and pld < self.pld_threshold:
                        # PLD baixo: comprar
                        decision = "Comprar"
                    else:
                        # PLD alto: considerar esperar ou comprar
                        decision = "Comprar"  # Simplificado
                else:
                    decision = "Neutro"
            else:
                decision = "Neutro"
            
            decisions.append(decision)
        
        return pd.Series(decisions)

