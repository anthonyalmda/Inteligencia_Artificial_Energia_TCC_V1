# profit.py

import pandas as pd

class ProfitCalculator:
    def __init__(self, sell_price=0.75, buy_price=0.90, cost_rate=0.10):
        """
        Calculadora de lucro líquido considerando venda de excedentes
        e compra de energia quando há déficit.

        :param sell_price: preço de venda da energia excedente (R$/kWh)
        :param buy_price: preço de compra da energia quando há déficit (R$/kWh)
        :param cost_rate: percentual de custo fixo sobre a receita
        """
        self.sell_price = sell_price
        self.buy_price = buy_price
        self.cost_rate = cost_rate

    def calculate(self, consumption, production):
        """
        Calcula lucro líquido considerando excedente e déficit.

        :param consumption: série ou lista de consumo previsto
        :param production: série ou lista de produção prevista
        :return: DataFrame com resultados financeiros
        """
        results = []

        for c, p in zip(consumption, production):
            if p > c:
                # Excedente -> venda
                excedente = p - c
                receita = excedente * self.sell_price
                custo_fixo = receita * self.cost_rate
                lucro_liquido = receita - custo_fixo

                results.append({
                    "Consumo": c,
                    "Produção": p,
                    "Excedente": excedente,
                    "Deficit": 0,
                    "Receita Venda": receita,
                    "Custo Compra": 0,
                    "Lucro Liquido": lucro_liquido,
                    "Decisão": "Vender"
                })

            else:
                # Déficit -> compra
                deficit = c - p
                custo_compra = deficit * self.buy_price
                custo_fixo = custo_compra * self.cost_rate
                lucro_liquido = -(custo_compra + custo_fixo)

                results.append({
                    "consumo": c,
                    "producao": p,
                    "excedente": 0,
                    "deficit": deficit,
                    "receita_venda": 0,
                    "custo_compra": custo_compra,
                    "lucro_liquido": lucro_liquido,
                    "decisao": "Comprar"
                })

        return pd.DataFrame(results)

