# Modelo de previsão de produção de energia
# Autor: Trabalho de Conclusão de Curso (TCC)
# Data: 2025 

import numpy as np

class ProductionForecaster:
    def __init__(self):
        self.tendencia = 110

    def train(self, df):
        valores = df["production"].values
        self.tendencia = np.mean(valores[-10:])

    def predict(self, dias):
        return [self.tendencia] * dias
